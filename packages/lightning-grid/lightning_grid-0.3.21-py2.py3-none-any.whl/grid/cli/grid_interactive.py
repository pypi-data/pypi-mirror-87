import random
import sys
from typing import Optional

import click
import yaml
from coolname import generate_slug

import grid.globals as env
from grid import Grid
from grid.cli.utilities import validate_config, validate_disk_size_callback, overwrite_config
from grid.cli.grid_credentials import print_creds_table
from grid.cli.grid_train import _check_run_name_is_valid
from grid.tracking import tracker, TrackingEvents
from grid.types import ObservableType


def _print_submission_message(instance_type: str, provider: str,
                              credential_id: str, name: str,
                              datastore_name: str, datastore_version: str,
                              datastore_mount_dir: str):
    """Prints train submission message to the client."""
    message = f"""
        Interactive node created!

        `grid status` to list all runs and interactive nodes.
        `grid status {name}` to see the status fot this interactive node.

        ----------------------
        Submission summary
        ----------------------
        name:                    {name}
        instance_type:           {instance_type}
        cloud_provider:          {provider}
        cloud_credentials:       {credential_id}
        datastore_name:          {datastore_name}
        datastore_version:       {datastore_version}
        datastore_mount_dir:     {datastore_mount_dir}
        """

    click.echo(message)


def _generate_default_interactive_config(
    client: Grid,
    credential_id: str,
    instance_type: str,
    datastore_name: Optional[str] = None,
    datastore_version: Optional[str] = None,
    datastore_mount_dir: Optional[str] = None,
    disk_size: Optional[int] = None):
    """
    Generates a new default config file for user if user hasn't
    submitted one.
    """
    _default_credential = None
    creds = client.get_credentials()['getUserCredentials']
    if credential_id:
        if creds:
            #  Check if the credential passed is can
            #  be used by user. We'll raise an exception
            #  if user can't use such credential.
            for cred in creds:
                if cred['credentialId'] == credential_id:
                    _default_credential = cred
                    break

        if not _default_credential:
            raise click.ClickException(
                f'Credential ID {credential_id} does not exist. ' +
                'Use grid credentials to see available credential IDs.')
    else:
        _url = client.url.replace('/graphql', '')
        no_credentials_message = f"""
        No cloud credentials available! Visit {_url}/#/settings to
        add new cloud credentials.
        """
        if not creds:
            raise click.ClickException(no_credentials_message)

        if len(creds) == 1:
            cred = creds[0]
            _default_credential = cred

        elif len(creds) > 1:
            for credential in creds:
                if credential['defaultCredential']:
                    click.echo(
                        f"Using default cloud credentials {credential['credentialId']} "
                        f"to run on {credential['provider'].upper()}.")
                    _default_credential = credential
                    break

        #  If no credentials are available, raise an exception.
        if not _default_credential:
            m = """
            Detected multiple credentials. Which would you like to use?

                grid interactive --grid_credential [CREDENTIAL_ID]

            """
            print_creds_table(creds)
            raise click.ClickException(m)

    #  Relevant defaults for user.
    #  TODO: Pull from user profile when we have
    #  that information collected.
    defaults = {'region': 'us-east-1'}

    _grid_config = {
        'compute': {
            'provider': {
                'vendor': _default_credential['provider'],
                'credentials': _default_credential['credentialId'],
                'region': defaults['region']
            },
            'train': {
                'instance': instance_type,
                'disk_size': disk_size,
                #  These parameters are required for the
                #  training config. The max_nodes need to be a value
                #  other than 0, otherwise subsequent train operations
                #  will not work.
                'nodes': 0,  # Start with 0 compute nodes.
                'max_nodes': 10,  # Scale at most to 100 nodes.
                'gpus': 0,  # Required, but ignored.
                'datastore_name': datastore_name,
                'datastore_version': datastore_version,
                'datastore_mount_dir': datastore_mount_dir,
                'scale_down_seconds':
                30 * 60,  # How many seconds before scaling down?
            }
        }
    }

    #  Print debug message if in debug mode.
    if env.DEBUG:
        click.echo('Grid Config used:')
        click.echo(_grid_config)

    return _grid_config


@click.group(invoke_without_command=True)
@click.pass_context
def interactive(ctx) -> None:
    """Displays interactive nodes for given project."""
    client = Grid()

    if ctx.invoked_subcommand is None:
        # Get the status of the interactive observables.
        kind = ObservableType.INTERACTIVE
        client.status(kind=kind, follow=False)


@interactive.command()
@click.option('--grid_config',
              '--g_config',
              'config',
              type=click.File('r'),
              required=False,
              callback=overwrite_config,
              help='Path to Grid config YML')
@click.option('--grid_name',
              '--g_name',
              'name',
              type=str,
              required=False,
              help='Name for this run',
              callback=_check_run_name_is_valid)
@click.option('--grid_credential',
              '--g_credential',
              'credential',
              type=str,
              required=False,
              help='Cloud to run on')
@click.option('--grid_instance_type',
              '--g_instance_type',
              'instance_type',
              type=str,
              default='t2.xlarge',
              help='Instance type to start training session in')
@click.option('--grid_disk_size',
              '--g_disk_size',
              'disk_size',
              type=int,
              required=False,
              default=200,
              callback=validate_disk_size_callback,
              help='The disk size in GB to allocate to interactive node')
@click.option('--grid_datastore_name',
              '--g_datastore_name',
              'datastore_name',
              type=str,
              required=False,
              help='Datastore name to be mounted in interactive node')
@click.option('--grid_datastore_version',
              '--g_datastore_version',
              'datastore_version',
              type=str,
              required=False,
              help='Datastore version to be mounted in interactive node')
@click.option(
    '--grid_datastore_mount_dir',
    '--g_datastore_mount_dir',
    'datastore_mount_dir',
    type=str,
    required=False,
    default='/home/jovyan/datastore',
    help=
    'Absolute path to mount Datastore in interactive node. (default to ~/datastore)'
)
def create(config: Optional[click.File], name: Optional[str],
           credential: Optional[str], instance_type: str,
           datastore_name: Optional[str], datastore_version: Optional[str],
           datastore_mount_dir: Optional[str],
           disk_size: Optional[int]) -> None:
    """Creates an interactive node."""
    client = Grid()

    tracker.send_event(event=TrackingEvents.INTERACTIVE_NODE_CREATED,
                       properties={'user_input': " ".join(sys.argv)})

    # make a fun random name when user does not pass in a name
    if name is None:
        name = f'{generate_slug(2)}-{random.randint(0, 1000)}'
        click.echo(
            f'No --grid_name passed, naming your interactive node: {name}')

    #  If the user has not passed a grid config file,
    #  then generate one with a set of default options.
    #  We'll add a default instance and the user's
    #  default credentials.
    if not config:
        _grid_config = _generate_default_interactive_config(
            client=client,
            datastore_name=datastore_name,
            datastore_version=datastore_version,
            datastore_mount_dir=datastore_mount_dir,
            credential_id=credential,
            instance_type=instance_type,
            disk_size=disk_size)

    else:
        _grid_config = config

    validate_config(cfg=_grid_config)
    _grid_config_yaml = yaml.dump(_grid_config)

    #  Send to client.
    client.create_interactive_node(config=_grid_config_yaml, name=name)

    #  Shows a friendly submission message to the
    #  user.
    _print_submission_message(
        instance_type=_grid_config['compute']['train']['instance'],
        provider=_grid_config['compute']['provider']['vendor'],
        credential_id=_grid_config['compute']['provider']['credentials'],
        datastore_name=datastore_name,
        datastore_version=datastore_version,
        datastore_mount_dir=datastore_mount_dir,
        name=name)


@interactive.command()
@click.argument('interactive_node', type=str, nargs=1)
def delete(interactive_node: str) -> None:
    """Deletes an interactive node."""
    client = Grid()
    client.delete_interactive_node(interactive_node_name=interactive_node)
