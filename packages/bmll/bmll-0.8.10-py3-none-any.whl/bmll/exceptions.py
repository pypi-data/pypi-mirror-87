

class AuthenticationError(Exception):
    """The service was unable to authenticate."""
    pass


class LoginError(Exception):
    """A Error has occurred when attempting to login to the BMLL Services."""
    pass
