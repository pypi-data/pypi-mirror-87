from threedi_api_client.threedi_api_client import ThreediApiClient


def test_init_threedi_api_client_from_env_file(tmpdir):
    env_file = tmpdir / 'env_file'
    with open(str(env_file), 'w') as f:
        f.write("API_HOST=localhost:8000/v3.0\n")
        f.write("API_USERNAME=username\n")
        f.write("API_PASSWORD=password\n")
    ThreediApiClient(env_file=str(env_file))


def test_init_threedi_api_client_from_env_vars(monkeypatch):
    monkeypatch.setenv('API_HOST', 'localhost:8000/v3.0')
    monkeypatch.setenv('API_USERNAME', 'username')
    monkeypatch.setenv('API_PASSWORD', 'password')
    ThreediApiClient()


def test_init_threedi_api_client_from_config():
    config = {
        "API_HOST": "localhost:8000/v3.0",
        "API_USERNAME": "username",
        "API_PASSWORD": "password"
    }
    ThreediApiClient(config=config)
