import click
import unittest

import grid.globals as env
from grid import cli
from grid.client import Grid

from click.testing import CliRunner
from _pytest.monkeypatch import MonkeyPatch
from tests.utilities import create_local_schema_client


class StatusTestCase(unittest.TestCase):
    """Test case for the status command"""
    @classmethod
    def setUpClass(cls):
        cls.runner = CliRunner()
        cls.monkeypatch = MonkeyPatch()

        cls.credentials_path = 'tests/data/credentials.json'
        cls.test_run = 'manual-test-run'

        # Setup the global DEBUG flag to True.
        env.DEBUG = True

        #  Monkey patches the GraphQL client to read from a local schema.
        def monkey_patch_client(self):
            self.client = create_local_schema_client()

        #  skipcq: PYL-W0212
        Grid._init_client = monkey_patch_client

    def monkey_patched_method(self, *args, **kwargs):
        return True

    def monkey_patch_exception(self, *args, **kwargs):
        raise click.ClickException('test')

    def test_status_works(self):
        """grid status does not raise an exception"""
        old_status = Grid.status
        self.monkeypatch.setattr(Grid, 'status', self.monkey_patched_method)

        result = self.runner.invoke(cli.status, [self.test_run])
        assert result.exit_code == 0
        assert not result.exception

        # Set attribute again.
        self.monkeypatch.setattr(Grid, 'status', old_status)

    def test_status_accepts_export_parameters(self):
        """grid status accepts export parameters"""
        old_status = Grid.status
        self.monkeypatch.setattr(Grid, 'status', self.monkey_patched_method)

        for t in ['csv', 'json']:
            result = self.runner.invoke(cli.status,
                                        [self.test_run, '--export', t])
            assert result.exit_code == 0
            assert not result.exception

        # Set attribute again.
        self.monkeypatch.setattr(Grid, 'status', old_status)

    def test_status_raises_exception(self):
        """grid status raises exception when experiment is passed"""
        old_status = Grid.status
        self.monkeypatch.setattr(Grid, 'status', self.monkey_patched_method)

        result = self.runner.invoke(cli.status, [f'{self.test_run}-exp1'])
        assert result.exit_code == 2
        assert result.exception

        # Set attribute again.
        self.monkeypatch.setattr(Grid, 'status', old_status)

    def test_status_run(self):
        """grid status interactive nodes output toggles with the run param"""
        old_status = Grid.status
        self.monkeypatch.setattr(Grid, 'status', self.monkey_patched_method)

        for r in [self.test_run, '']:
            result = self.runner.invoke(cli.status, ['--follow', r])
            assert result.exit_code == 0
            assert not result.exception

        # Set attribute again.
        self.monkeypatch.setattr(Grid, 'status', old_status)
