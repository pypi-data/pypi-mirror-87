from click.testing import CliRunner
from tests.utilities import (monkey_patch_client,
                             monkeypatched)
from tests.mock_backend import resolvers

from grid import cli
import grid.client as grid
import grid.commands.credentials as credentials

RUNNER = CliRunner()


class TestInteractive:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        credentials.gql = lambda x: x
        grid.gql = lambda x: x

        cls.mp_status = lambda *args, **kwargs: True
        cls.CREDENTIAL_ID = 'test-credential'

    def test_interactive_succeeds_with_no_args(self):
        """
        grid interactive succeeds with no args
        """
        with monkeypatched(grid.Grid, 'status', self.mp_status):
            result = RUNNER.invoke(cli.interactive, [])
            assert result.exit_code == 0
            assert not result.exception

    def test_interactive_create_succeeds(self):
        """
        grid interactive create succeeds
        """
        def mp_create_interactive_node(*args, **kwargs):
            return {'success': True, 'message': ''}

        with monkeypatched(grid.Grid, 'status', self.mp_status):
            with monkeypatched(resolvers, 'create_interactive_node',
                               mp_create_interactive_node):
                result = RUNNER.invoke(cli.interactive, ["create"])
                assert result.exit_code == 0
                assert not result.exception
                assert 'Interactive node created!' in result.output

    def test_interactive_create_fails_multiple_creds(self):
        """
        grid interactive create fails with multiple non-default creds
        """
        creds = self.CREDENTIAL_ID

        def mp_get_credentials_multiple_no_default(self):
            return {
                'getUserCredentials': [{
                    'credentialId': creds,
                    'provider': 'aws',
                    'defaultCredential': False,
                    'createdAt': '2020-11-11',
                    'lastUsedAt': '2020-11-11',
                    'alias': None
                }, {
                    'credentialId': "Another",
                    'provider': 'aws',
                    'defaultCredential': False,
                    'createdAt': '2020-11-11',
                    'lastUsedAt': '2020-11-11',
                    'alias': None
                }]
            }

        with monkeypatched(grid.Grid, 'get_credentials',
                           mp_get_credentials_multiple_no_default):
            result = RUNNER.invoke(cli.interactive, ["create"])
            assert result.exit_code == 1
            assert result.exception
            assert 'Detected multiple credentials. Which would you like to use?' in result.output

    def test_interactive_create_fails_with_wrong_creds(self):
        """
        grid interactive create fails with wrong credentials
        """
        def mp_no_default_creds(self):
            return {
                'getUserCredentials': [{
                    'credentialId': 'wrong-creds',
                    'provider': 'aws',
                    'defaultCredential': True
                }]
            }

        with monkeypatched(grid.Grid, 'get_credentials', mp_no_default_creds):
            result = RUNNER.invoke(
                cli.interactive,
                ["create", '--grid_credential', self.CREDENTIAL_ID])
            assert result.exit_code == 1
            assert result.exception
            assert f'Credential ID {self.CREDENTIAL_ID} does not exist.' in result.output

    def test_interactive_create_fails_with_no_creds(self):
        """
        grid interactive create fails with no credentials
        """
        def mp_no_creds(self):
            return {'getUserCredentials': []}

        with monkeypatched(grid.Grid, 'get_credentials', mp_no_creds):
            result = RUNNER.invoke(cli.interactive, ["create"])
            assert result.exit_code == 1
            assert result.exception
            assert ' No cloud credentials available' in result.output

    def test_interactive_create_succeeds_with_default_creds(self):
        """
        grid interactive create succeeds with default creds
        """
        creds = self.CREDENTIAL_ID

        def mp_default_creds(self):
            return {
                'getUserCredentials': [{
                    'credentialId': creds,
                    'provider': 'aws',
                    'defaultCredential': True
                }]
            }

        with monkeypatched(grid.Grid, 'get_credentials', mp_default_creds):
            result = RUNNER.invoke(cli.interactive, ["create"])
            assert result.exit_code == 0
            assert not result.exception
            assert 'Interactive node created!' in result.output

    def test_interactive_create_fails_if_config_not_found(self):
        """grid interactive create fails if config not found"""

        result = RUNNER.invoke(cli.interactive,
                               ["create", "--grid_config", "no-file"])

        assert result.exit_code == 2
        assert result.exception
        assert 'Could not open file' in result.output

    def test_interactive_create_succeeds_with_config(self, tmp_path):
        """grid interactive create succeeds with config"""

        content = """
        compute:
            provider:
                credentials: cc-kmz2f
                region: us-east-1
                vendor: aws
            train:
                disk_size: 200
                gpus: 0
                instance: g4dn.xlarge
                max_nodes: 10
                nodes: 0
                scale_down_seconds: 30
                memory: 100Mi
                cpus: 2
        """

        config = tmp_path / "config.yaml"
        config.write_text(content)

        with monkeypatched(grid.Grid, 'status', self.mp_status):
            result = RUNNER.invoke(
                cli.interactive,
                ["create", "--grid_config",
                 config.as_posix()])

            assert result.exit_code == 0
            assert not result.exception
            assert 'Interactive node created' in result.output

    def test_interactive_delete_succeeds(self):
        """grid interactive delete succeeds"""
        def mp_delete_interactive_node(*args, **kwargs):
            return {'success': True, 'message': ''}

        with monkeypatched(resolvers, 'delete_interactive_node',
                           mp_delete_interactive_node):
            result = RUNNER.invoke(cli.interactive,
                                   ["delete", "node-to-delete"])

            assert result.exit_code == 0
            assert not result.exception
            assert 'has been deleted successfully' in result.output

    def test_interactive_delete_fails(self):
        """grid interactive delete fails"""
        def mp_delete_interactive_node(*args, **kwargs):
            return {'success': False, 'message': ''}

        with monkeypatched(resolvers, 'delete_interactive_node',
                           mp_delete_interactive_node):
            result = RUNNER.invoke(cli.interactive,
                                   ["delete", "node-to-delete"])

            assert result.exit_code == 1
            assert result.exception
            assert 'Failed to delete interactive node' in result.output
