from typing import Tuple
import os

import click
from shell import Shell

from .fs_abc import FilesystemAbstract


class SMBFS(FilesystemAbstract):
    def parse_remote(self) -> Tuple[str, str, str]:
        remote_str = self.config.remote
        if not remote_str.startswith("//"):
            raise ValueError(f"Invalid samba path {remote_str}")

        remote_str = remote_str[2:]

        user, hostname, dir = "", "", ""

        if "@" in remote_str:
            user, hostname = remote_str.split("@")
        else:
            hostname = remote_str

        hostname, dir = hostname.split("/", 1)

        return user, hostname, dir

    def format_remote(self) -> str:
        remote_str = "//"
        if self.user:
            remote_str = f"{remote_str}{self.user}@"

        if not self.hostname:
            raise ValueError("host must not be None")
        remote_str = f"{remote_str}{self.hostname}/"

        if self.dir:
            remote_str = f"{remote_str}{self.dir}"
        return remote_str

    def format_cmd(self):
        remote_str = self.format_remote()

        if not self.mount_point:
            raise ValueError("mount_point must not be None")

        smbfs_cmd = f"mount_smbfs {remote_str} {self.mount_point}"
        return smbfs_cmd

    def validate(self):
        mount_cmd = self.format_cmd()
        if mount_cmd:
            return True
        else:
            return False

    def mount(self):
        if not os.path.exists(self.mount_point):
            os.makedirs(self.mount_point, exist_ok=True)
        mount_cmd = self.format_cmd()
        sh = Shell()
        sh.run(mount_cmd)
