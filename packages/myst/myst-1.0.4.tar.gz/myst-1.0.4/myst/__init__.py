"""The official `myst` python package owned by Myst AI, Inc."""
from myst.client import Client
from myst.constants import DEFAULT_API_HOST
from myst.constants import DEFAULT_API_VERSION
from myst.user_credentials_cache import UserCredentialsCache
from myst.utils.auth_utils import get_credentials


# Configure global API host and version.
api_host = DEFAULT_API_HOST
api_version = DEFAULT_API_VERSION

# Configure a default global client to use.
_client = Client()


def get_client():
    """Gets the default global client.

    We recommend using this method whenever using the default global client so that you have the latest version of the
    client object, rather than a stale one that was imported before additional configurations to the client were made.

    Returns:
        _client (myst.client.Client): default global client
    """
    global _client
    return _client


# Import top-level `myst` functions.
from myst.utils.auth_utils import authenticate
from myst.utils.auth_utils import clear_user_credentials_cache

# Import all resources for easy access.
from myst.resources.time_series import TimeSeries
