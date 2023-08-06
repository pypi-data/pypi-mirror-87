import jwt

from openapi_client import ApiClient
from openapi_client import Configuration
from openapi_client import AuthApi
from openapi_client.models import Authenticate

from threedi_api_client.config import Config, EnvironConfig

# Token expires at:
# jwt_token.exp + EXPIRE_LEEWAY seconds
# (thus EXPIRE_LEEWAY seconds before it really expires)
EXPIRE_LEEWAY = -300


def get_auth_token(username: str, password: str, api_host: str):
    api_client = ApiClient(
        Configuration(
            username=username,
            password=password,
            host=api_host
        )
    )
    auth = AuthApi(api_client)
    return auth.auth_token_create(Authenticate(username, password))


def is_token_usable(token: str) -> bool:
    if token is None:
        return False

    # Check if not expired...
    try:
        jwt.decode(
            token,
            options={"verify_signature": False},
            leeway=EXPIRE_LEEWAY,
        )
    except Exception:
        return False

    return True


def refresh_api_key(config: Configuration):
    """Refreshes the access key if its expired"""
    api_key = config.api_key.get("Authorization")
    if is_token_usable(api_key):
        return

    refresh_key = config.api_key['refresh']
    if is_token_usable(refresh_key):
        api_client = ApiClient(Configuration(config.host))
        auth = AuthApi(api_client)
        token = auth.auth_refresh_token_create(
            {"refresh": config.api_key['refresh']}
        )
    else:
        token = get_auth_token(config.username, config.password, config.host)
    config.api_key = {
        'Authorization': token.access,
        'refresh': token.refresh
    }


class ThreediApiClient:
    def __new__(cls, env_file=None, config=None):
        if env_file is not None:
            user_config = Config(env_file)
        elif config is not None:
            user_config = config
        else:
            user_config = EnvironConfig()

        configuration = Configuration(
            host=user_config.get("API_HOST"),
            username=user_config.get("API_USERNAME"),
            password=user_config.get("API_PASSWORD"),
            api_key={"Authorization": '', "refresh": ''},
            api_key_prefix={"Authorization": "Bearer"}
        )
        configuration.refresh_api_key_hook = refresh_api_key
        api_client = ApiClient(configuration)
        return api_client
