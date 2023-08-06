from grid.client import Grid, env

from pathlib import Path
from tests.utilities import create_local_schema_client, monkeypatched

SETTINGS_PATH = 'tests/data/settings.json'
CREDENTIALS_PATH = 'tests/data/credentials.json'


def monkey_patch_client(self):
    self.client = create_local_schema_client()


def test_load_global_settings():
    """Grid() loads global settings alters globals."""

    with monkeypatched(Grid, '_init_client', monkey_patch_client):
        Grid.grid_settings_path = SETTINGS_PATH
        Grid(credential_path=CREDENTIALS_PATH, load_local_credentials=False)

        assert env.DEBUG == True


def test_global_settings_create_file_if_not_exists():
    """Grid() creates file if not exists."""

    new_path = 'tests/data/home/settings.json'
    Grid.grid_settings_path = new_path
    Grid(credential_path=CREDENTIALS_PATH, load_local_credentials=False)

    P = Path.home().joinpath(new_path)
    assert P.exists()

    # cleanup
    P.unlink()
