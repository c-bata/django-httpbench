from django.conf import settings


DEFAULT_USERNAME_KEY = "X-USERNAME"


def _make_header_wsgi_env_key(http_header: str) -> str:
    """Convert HTTP header to WSGI environ key format.

    HTTP_ Variables corresponding to the client-supplied HTTP request
    headers (i.e., variables whose names begin with "HTTP_").
    See https://www.python.org/dev/peps/pep-3333/ for more details

    >>> print(_make_header_wsgi_env_key("X-USERNAME"))
    HTTP_X_USERNAME
    """
    return "HTTP_" + http_header.replace("-", "_").upper()


def get_username_header_key() -> str:
    if hasattr(settings, 'LOAD_USERNAME_KEY'):
        return settings.LOAD_USERNAME_KEY
    return DEFAULT_USERNAME_KEY


def get_username_wsgi_env_key() -> str:
    return _make_header_wsgi_env_key(get_username_header_key())
