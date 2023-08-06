import re

from shell import shell
import click

from .fs_abc import FilesystemAbstract
from .fs_config import FilesystemConfig
from .sshfs import SSHFS
from .smbfs import SMBFS

mount_line_pattern = re.compile(r"(.*) on (.*) \(.*\)$")


def create_fs(config: FilesystemConfig) -> FilesystemAbstract:
    if config.filesystem == "sshfs":
        return SSHFS(config)
    if config.filesystem == "smbfs":
        return SMBFS(config)
    else:
        raise ValueError(f"{config.filesystem} is not supported")


def ls_mounts(config_dir: str):
    config_files = FilesystemConfig.ls_files(config_dir)
    remotes: dict[str, str] = {}

    for file in config_files:
        filesystem = create_fs(FilesystemConfig.from_file(file))
        remotes[filesystem.format_remote()] = filesystem.mount_point
        # remotes.append(filesystem.format_remote(), filesystem.mount_point)

    mount_lines = shell("mount").output()
    for line in mount_lines:
        matches = re.findall(mount_line_pattern, line)[0]
        if not matches:
            continue
        remote, mount_point = matches
        if remote in remotes:
            click.echo(f"{remote} on {mount_point}")
