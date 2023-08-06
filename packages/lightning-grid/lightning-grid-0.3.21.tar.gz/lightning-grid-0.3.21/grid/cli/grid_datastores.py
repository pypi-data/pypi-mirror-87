import click

from typing import Optional
from grid import Grid
from grid.cli.grid_train import get_credentials


@click.group(invoke_without_command=True)
@click.pass_context
def datastores(ctx) -> None:
    """Manages datastore workflows in Grid"""
    return


@datastores.command()
@click.option('--source_dir',
              type=click.Path(exists=True, file_okay=True, dir_okay=True),
              required=True,
              help='Source directory to upload datastore files')
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--grid_credential',
              type=str,
              required=False,
              help='Grid credential ID')
@click.option('--version',
              type=str,
              required=True,
              help='Version of the datastore')
@click.option(
    '--staging_dir',
    type=str,
    default="",
    required=False,
    help='Staging directory to hold the temporary compressed datastore')
@click.pass_context
def create(ctx,
           source_dir: str,
           name: str,
           version: str,
           staging_dir: str,
           grid_credential: Optional[str] = None) -> None:
    """Creates datastores"""
    client = Grid()

    credential = get_credentials(client=client,
                                 grid_credential=grid_credential)

    client.upload_datastore(source_dir=source_dir,
                            staging_dir=staging_dir,
                            credential_id=credential['credentialId'],
                            name=name,
                            version=version)


@datastores.command()
@click.pass_context
def list(ctx) -> None:
    """Lists datastores"""
    client = Grid()
    client.list_datastores()


@datastores.command()
@click.option('--name', type=str, required=True, help='Name of the datastore')
@click.option('--version',
              type=str,
              required=True,
              help='Version of the datastore')
@click.pass_context
def delete(ctx, name: str, version: str) -> None:
    """Lists datastores"""
    client = Grid()
    client.delete_datastore(name=name, version=version)
