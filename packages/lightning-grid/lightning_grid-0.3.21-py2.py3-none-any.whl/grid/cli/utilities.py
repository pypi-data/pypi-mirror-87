import click
import yaml

from typing import Dict, Any
from grid.tracking import tracker, TrackingEvents

DISK_SIZE_ERROR_MSG = "Invalid disk size, should be greater than 100Gb"


def validate_config(cfg: Dict[str, Any]) -> None:
    """
    Validates Grid config.

    Parameters
    ----------
    cfg: Dict[str, Any]
        Dictionary representing a Grid config
    """
    disk_size = cfg['compute']['train']['disk_size']
    if disk_size is not None and disk_size < 100:
        raise click.ClickException(DISK_SIZE_ERROR_MSG)

    tracker.send_event(TrackingEvents.CONFIG_PARSED,
                       properties={'config': cfg})


def overwrite_config(ctx, param, value):
    """
    Click callback that replaces values from a passed config
    YML with the values passed from the CLI context.
    """
    patched_grid_config = None
    grid_config = value
    if grid_config:

        #  Loads the YML file as passed by the
        #  user.
        try:
            grid_config = yaml.safe_load(value.read())
            if not isinstance(grid_config, dict):
                raise Exception("Unexpected file structure")
        except Exception as e:
            raise click.BadParameter(
                f'Could not load your YAML config file: {e}')

        #  Adds required structure to the base
        #  YML file, if that structure isn't there.
        if 'compute' not in grid_config:
            grid_config['compute'] = {}
        if 'train' not in grid_config['compute']:
            grid_config['compute']['train'] = {}

        #  Generate a YML in-memory representation of
        #  the edited config file.
        patched_grid_config = yaml.dump(grid_config)

    return grid_config or patched_grid_config


def validate_disk_size_callback(ctx, param, value: int) -> int:
    """
    Validates the disk size upon user input.

    Parameters
    ----------
    ctx
        Click context
    param
        Click parameter
    value: int

    Returns
    --------
    value: int
        Unmodified value if valid
    """
    if value < 100:
        raise click.BadParameter(DISK_SIZE_ERROR_MSG)

    return value
