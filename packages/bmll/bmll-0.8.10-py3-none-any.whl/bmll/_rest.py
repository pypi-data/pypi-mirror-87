import base64
import datetime
import hashlib
import os
import pathlib
import warnings
from http import HTTPStatus

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from requests import request

from bmll.exceptions import AuthenticationError, LoginError


__all__ = ('Session', 'DEFAULT_SESSION', 'login', 'logout')


class Session:
    """
    The Session class handles low level communication and authentication with the BMLL Services.

    .. warning::

        It is only intended for *advanced* users who require a thread-safe interface.

    .. note::

        See :meth:`Session.login` for Parameters

    """

    def __init__(self, *args, **kwargs):
        self.SERVICE_URLS = {
            'reference': os.environ.get('BMLL_REFERENCE_URL', 'https://reference.data.bmlltech.com'),
            'time-series': os.environ.get('BMLL_TIME_SERIES_URL', 'https://time-series.data.bmlltech.com'),
            'auth': os.environ.get('BMLL_AUTH_URL', 'http://auth.data.bmlltech.com')
        }
        self._USERNAME = os.environ.get('BMLL_USERNAME')
        self._KEY_PATH = os.environ.get('BMLL_KEY_PATH')
        self._KEY_PASSPHRASE = os.environ.get('BMLL_KEY_PASSPHRASE')

        self._TOKEN = None
        self._API_KEY = None

        self._attempt = 0

        if args or kwargs:
            self.login(*args, **kwargs)

    def execute(self, method, service, url, *, headers=None, **kw):
        """execute a request against a service."""
        base_url = self.SERVICE_URLS[service]

        headers = headers if headers is not None else self.get_headers()

        try:
            while self._attempt <= 2:
                self._attempt += 1
                resp = request(method, base_url+url, headers=headers, **kw)

                if resp.status_code == HTTPStatus.OK:
                    return resp.json()
                elif resp.status_code == HTTPStatus.UNAUTHORIZED:
                    # try to get a new token
                    if self._attempt == 1:
                        self.login()
                        continue
                    else:
                        raise AuthenticationError('Unauthorised to access service.')
                else:
                    raise Exception((resp.status_code, resp.json()))

        finally:
            self._attempt = 0

    def get_headers(self):
        """return the authenticated headers."""
        if self._TOKEN is None:
            self.login()

        headers = {
            "Authorization": "Bearer {}".format(self._TOKEN),
        }

        if self._API_KEY:
            headers['x-api-key'] = self._API_KEY

        return headers

    def login(self, username=None, key_path=None, passphrase=None):
        """
        Login to the BMLL Remote API.

        Notes
        -----
        To login to the BMLL Remote API you must have registered at https://data.bmlltech.com and generated a key-pair.

        Note: Both key files must exist in the same directory.

        Parameters
        ----------
        username: str, optional
            `api username <https://data.bmlltech.com/#app/sftp>`_.
            if not provided, then attempt to retrieve the username from the comment section of the public key-file.
        key_path: str, optional
            the path of your private key.
        passphrase: str, optional
            the passphrase for your key if exists.

        """
        if key_path:
            self._KEY_PATH = key_path
        elif self._KEY_PATH is None:
            raise LoginError('Unable to locate private key.\n'
                             '\n'
                             'You must either:\n'
                             '\n'
                             '- provide the key_path argument to bmll.login\n'
                             '- set the BMLL_KEY_PATH environment variable prior to import of bmll.')

        if passphrase:
            self._KEY_PASSPHRASE = passphrase

        if username:
            self._USERNAME = username
        elif self._USERNAME is None:
            self._USERNAME = self._try_get_username()

        if self._USERNAME is None:
            raise LoginError('Unable to locate username.\n'
                             '\n'
                             'You must either:\n'
                             '\n'
                             '- provide the username argument to bmll.login\n'
                             '- set the BMLL_USERNAME environment variable prior to import of bmll.\n'
                             '- set the username as the comment field of your public key.')

        self._TOKEN, self._API_KEY = self._get_token()
        print('Logged in successfully.')

    def logout(self):
        """Logout of the BMLL Remote API."""
        self._TOKEN = None
        self._API_KEY = None
        print('Logged out.')

    def __enter__(self, *args, **kwargs):
        self.login(*args, **kwargs)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def _get_private_key_path(self):
        return pathlib.Path(self._KEY_PATH).expanduser()

    def _get_public_key_path(self):
        return self._get_private_key_path().with_suffix('.pub')

    def _ssh_key_fingerprint(self):
        """ Return the ssh key fingerprint
        """
        # NOTE: the return value can also be obtained from the
        # command
        # ssh-keygen -v -l -f path/to/public_key.pub
        path = self._get_public_key_path()
        key = path.read_text()
        return self._key_to_fingerprint(key)

    def _key_to_fingerprint(self, key):
        """
        Helper function to convert ssh key to fingerprint
        Parameters
        ----------
        key: str
            ssh key
        Returns
        -------
        fingerprint : str
        """
        key = base64.b64decode(key.strip().split()[1].encode('ascii'))
        fp_plain = hashlib.md5(key).hexdigest()
        return ':'.join(f'{first}{second}' for first, second in zip(fp_plain[::2], fp_plain[1::2]))

    def _get_key_comment(self, key):
        """return the comment from public key."""
        key_parts = key.split()
        if len(key_parts) == 3:
            return key_parts[-1]
        else:
            return None

    def _try_get_username(self):
        """Attempt to retrieve the username from the comment section of the public key."""
        path = self._get_public_key_path()
        key = path.read_text()
        username = self._get_key_comment(key)
        return username

    def _get_session_id(self):
        data = {
            'iss': self._USERNAME
        }
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        resp = self.execute('post', 'auth', '/auth/identity', json=data, headers=headers)

        return resp['sid']

    def _get_token(self):
        """ Call the /auth endpoint
        """
        # Initial "log in" step, 1st part of handshake
        # We send in the JSON body the "claims" we
        # want
        print("Starting log-in process...")

        json_body = {
            "iss": self._USERNAME,
            "aud": "dd-services",
            "kid": self._ssh_key_fingerprint(),  # ssh key id
            "exp": (
                datetime.timedelta(days=1) + datetime.datetime.utcnow()
            ).timestamp(),
            "sid": self._get_session_id()
        }
        # Get the token, 2nd part of handshake
        # Here we create a JWT signed with our private SSH key
        # The server has the public counterpart and can verify
        # that the JWT was signed by our private SSH key.
        secret_key_path = self._get_private_key_path()
        password = self._KEY_PASSPHRASE.encode() if self._KEY_PASSPHRASE else None
        priv_rsakey = load_pem_private_key(
            secret_key_path.read_bytes(), password=password,
            backend=default_backend(),
        )
        jws_encoded = jwt.encode(
            json_body, key=priv_rsakey, algorithm="RS256",
            headers={"kid": json_body["kid"]},
        )
        jws = jws_encoded.decode()
        json_body["jws"] = jws

        response = self.execute(
            'post',
            'auth',
            '/auth/token',
            json=json_body,
            headers={}
        )

        # The (successful) response contains a JWT signed with a
        # secret that only the server knows. The server will
        # validate tokens with this secret on each endpoint
        # invocation

        return response['token'], response.get('api-key')

    def _set_environment(self, env):
        """Developer Mode: set the environment to `local`, `dev` or `staging`."""
        if env in ['local', 'docker']:
            if env == 'local':
                self.SERVICE_URLS['auth'] = 'https://localhost:64005'
                self.SERVICE_URLS['reference'] = 'https://localhost:64001'
                self.SERVICE_URLS['time-series'] = 'https://localhost:64002'
            else:
                self.SERVICE_URLS['auth'] = 'https://ddserv_auth-service_1:64000'
                self.SERVICE_URLS['reference'] = 'https://ddserv_reference-service_1:64000'
                self.SERVICE_URLS['time-series'] = 'https://ddserv_time-series-service_1:64000'

            # patch headers
            self.get_headers = lambda: None
            # disable verify
            os.environ['REQUESTS_CA_BUNDLE'] = ''
            os.environ['CURL_CA_BUNDLE'] = ''
            warnings.filterwarnings('ignore', message='Unverified HTTPS request')
        else:
            self.SERVICE_URLS['auth'] = self.SERVICE_URLS['auth'].replace(
                'data.bmlltech.com', f'data.{env}.bmll.io'
            )
            self.SERVICE_URLS['reference'] = self.SERVICE_URLS['reference'].replace(
                'data.bmlltech.com', f'data.{env}.bmll.io'
            )
            self.SERVICE_URLS['time-series'] = self.SERVICE_URLS['time-series'].replace(
                'data.bmlltech.com', f'data.{env}.bmll.io'
            )


DEFAULT_SESSION = Session()

login = DEFAULT_SESSION.login
logout = DEFAULT_SESSION.logout
