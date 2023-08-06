from click.testing import CliRunner
from tests.utilities import (create_test_credentials, monkey_patch_client,
                             monkeypatched)
from tests.mock_backend import resolvers

from grid import cli
import grid.client as grid
import grid.commands.credentials as credentials
import grid.uploader as uploader

RUNNER = CliRunner()


class TestDatastores:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x
        credentials.gql = lambda x: x

        create_test_credentials()

    def test_create_without_grid_credential_works(self):
        """grid datastores create without passing credentials works"""
        def mp_get_credentials(*args, **kwargs):
            return [{
                'credentialId': 'test-cred-0',
                'provider': 'aws',
                'alias': 'my credential name',
                'createdAt': resolvers.now,
                'lastUsedAt': resolvers.now,
                'defaultCredential': True
            }]

        def mp_upload(*args, **kwargs):
            return {'key': 'value'}

        with monkeypatched(uploader.S3DatastoreUploader, 'upload', mp_upload):
            with monkeypatched(resolvers, 'get_user_credentials',
                               mp_get_credentials):
                result = RUNNER.invoke(cli.datastores, [
                    'create', '--source_dir', 'tests/data', '--name', 'test',
                    '--version', 'v0'
                ])
                assert result.exit_code == 0
                assert not result.exception
                assert 'Finished uploading datastore' in result.output

                result = RUNNER.invoke(cli.datastores, [
                    'create', '--source_dir', 'tests/data', '--name', 'test',
                    '--version', 'v0', '--staging_dir', 'tests/datastore'
                ])
                assert result.exit_code == 0
                assert not result.exception
                assert 'Finished uploading datastore' in result.output

    def test_list_prints_table_of_datastores(self):
        """grid datastores list prints table of datstores"""
        result = RUNNER.invoke(cli.datastores, ['list'])
        assert result.exit_code == 0
        assert not result.exception
        assert 'Name' in result.output
        assert 'Version' in result.output
        assert 'Size' in result.output
        assert 'Created' in result.output
        assert 'test datastore' in result.output

    def test_deletes_a_datastore(self):
        """grid datastores delete deletes a datastore"""
        result = RUNNER.invoke(cli.datastores,
                               ['delete', '--name', 'test', '--version', 'v0'])
        assert result.exit_code == 0
        assert not result.exception

    def test_deletes_a_datastore_fails(self):
        """grid datastores delete fails to delete a datastore"""
        def delete_datastore(*args, **kwargs):
            return {"success": False}

        with monkeypatched(resolvers, 'delete_datastore', delete_datastore):
            result = RUNNER.invoke(
                cli.datastores,
                ['delete', '--name', 'test', '--version', 'v0'])
            assert result.exit_code == 0
            assert not result.exception
            assert 'Failed to delete datastore' in result.output

    def test_deletes_a_datstore_fails_with_ex(self):
        """grid datastores delete fails to delete a datastore with exception"""
        def delete_datastore(*args, **kwargs):
            raise Exception()

        with monkeypatched(resolvers, 'delete_datastore', delete_datastore):
            result = RUNNER.invoke(
                cli.datastores,
                ['delete', '--name', 'test', '--version', 'v0'])
            assert result.exit_code == 1
            assert result.exception
            assert 'Failed to delete datastore' in result.output
