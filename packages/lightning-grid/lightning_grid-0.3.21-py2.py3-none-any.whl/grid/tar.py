"""
Create tar file from folder
"""

import os
import subprocess


def get_dir_size(source_dir: str) -> int:
    """
    Get size of a directory

    Parameters
    ----------
    source_dir: str
        Directory path

    Returns
    -------
    int
        Size in bytes
    """
    size = 0
    for root, _, files in os.walk(source_dir, topdown=True):
        for f in files:
            full_path = os.path.join(root, f)
            size += os.path.getsize(full_path)

    return size


def tar_directory_unix(source_dir: str, temp_dir: str,
                       target_file: str) -> int:
    """
    Create tar from directory using `tar`

    Parameters
    ----------
    source_dir: str
        Source directory
    temp_dir: str
        Temporary directory that holds the target file
    target_file: str
        Target tar file

    Returns
    -------
    int
        Target file size in bytes
    """
    size = get_dir_size(source_dir)

    command = f"tar -C {source_dir} --exclude='{temp_dir}' -zcvf {target_file} ./"
    subprocess.check_call(command, stderr=subprocess.DEVNULL, shell=True)
    return size
