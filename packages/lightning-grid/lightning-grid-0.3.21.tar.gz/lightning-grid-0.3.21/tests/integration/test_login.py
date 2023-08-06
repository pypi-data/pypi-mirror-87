from click.testing import CliRunner
from tests.utilities import (create_test_credentials, monkey_patch_client,
                             monkeypatched)
from tests.mock_backend import resolvers
from requests.exceptions import HTTPError

from grid import cli
from grid.cli.grid_login import click, env
import grid.client as grid
import grid.commands.credentials as credentials

RUNNER = CliRunner()


class TestCredentials:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        credentials.gql = lambda x: x
        grid.gql = lambda x: x

        create_test_credentials()

    def test_login_without_username_and_api_key(self):
        """
        grid login without username and API key creates a prompt for username
        """
        def mp_launch(*args, **kwargs):
            return True

        with monkeypatched(click, 'launch', mp_launch):
            result = RUNNER.invoke(cli.login, [], input='testuser\n apikey\n')
            assert result.exit_code == 0
            assert not result.exception
            assert 'username' in result.output
            assert 'Login successful' in result.output

    def test_login_with_username_skips_prompt(self):
        """
        grid login with --username skips prompt
        """
        def mp_launch(*args, **kwargs):
            return True

        with monkeypatched(click, 'launch', mp_launch):
            result = RUNNER.invoke(cli.login, ['--username', 'testuser'],
                                   input='apikey\n')
            assert result.exit_code == 0
            assert not result.exception
            assert 'username' not in result.output
            assert 'Login successful' in result.output

    def test_login_fails_with_auth_error(self):
        """
        grid login raises error when auth is wrong
        """
        def mp_launch(*args, **kwargs):
            return True

        # Not authorized headers.
        def mp_init_client(self, *args, **kwargs):
            class A:
                @staticmethod
                def execute(*args, **kwargs):
                    raise HTTPError('not authorized')

            self.client = A

        with monkeypatched(grid.Grid, '_init_client', mp_init_client):
            with monkeypatched(click, 'launch', mp_launch):
                result = RUNNER.invoke(cli.login, ['--username', 'testuser'],
                                       input='apikey\n')
                assert result.exit_code == 1
                assert result.exception
                assert 'Failed to login' in result.output

        # API error.
        def mp_cli_login(*args, **kwargs):
            raise Exception('failed to make query')

        with monkeypatched(resolvers, 'cli_login', mp_cli_login):
            with monkeypatched(click, 'launch', mp_launch):
                env.DEBUG = True
                result = RUNNER.invoke(cli.login, ['--username', 'testuser'],
                                       input='apikey\n')
                assert result.exit_code == 1
                assert result.exception
                assert 'API error' in result.output
