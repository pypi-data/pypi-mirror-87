from click.testing import CliRunner
from tests.utilities import (create_test_credentials, monkey_patch_client,
                             monkeypatched)
from tests.mock_backend import resolvers

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestCancel:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_logs_without_arguments(self):
        """grid logs without arguments fails"""
        result = RUNNER.invoke(cli.logs, [])
        assert result.exit_code == 2
        assert result.exception

    def test_logs_empty_fails(self):
        """grid logs for an empty run fails"""
        result = RUNNER.invoke(cli.logs, ["test-run"])
        assert result.exit_code == 1
        assert result.exception
        assert 'Total available log pages: None' in result.output

    def test_logs_fails_with_ex(self):
        """grid logs fails with exception"""
        def get_archive_experiment_logs(*args, **kwargs):
            raise Exception()

        with monkeypatched(resolvers, 'get_archive_experiment_logs',
                           get_archive_experiment_logs):
            result = RUNNER.invoke(cli.logs, ["test-run"])
            assert result.exit_code == 1
            assert result.exception
            assert 'Failed to make query' in result.output
