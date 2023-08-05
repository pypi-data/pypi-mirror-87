"""
Authentication
~~~~~~~~~~~~~~

You will need to configure the following environment variables prior to importing `bmll`:

- `BMLL_KEY_PATH`: api private key path
- `BMLL_KEY_PASSPHASE`: (optional) the passphrase for the key if exists.
- `BMLL_USERNAME`: (optional) `api username <https://data.bmlltech.com/#app/sftp>`_.
                   will attempt to read this from the public key comment unless provided.

or call:

>>> bmll.login(username, key_path, passphrase)

Examples
--------

>>> bmll.reference.query(Ticker='VOD')

>>> bmll.reference.query(MIC='XLON')

>>> bmll.time_series.query(Ticker='VOD',
...                        MIC='XLON',
...                        metric='TradeCount',
...                        freq='D',
...                        start_date='2019-06-24',
...                        end_date='2019-12-31')

>>> bmll.time_series.query(Ticker=['VOD', 'RDSA'],
...                        MIC='XLON',
...                        metric={
...                            'metric': 'TradeCount',
...                            'tags.Classification': 'LitAddressable'
...                        },
...                        freq='D',
...                        start_date='2019-06-24',
...                        end_date='2019-12-31')

"""
from bmll import reference
from bmll import time_series
from bmll._rest import login, logout, Session

__all__ = (
    "__author__",
    "__contact__",
    "__homepage__",
    "__version__",
    "reference",
    "time_series",
    "login",
    "logout",
    "Session"
)


def __get_meta():
    import json
    import pathlib
    f = pathlib.Path(__file__).parent / "_metadata.json"
    return json.loads(f.read_text())


_meta = __get_meta()


__author__ = _meta["author"]
__contact__ = __author__
__homepage__ = _meta["url"]
__version__ = _meta["version"]
