from typing import Tuple

import click
from shell import Shell

from .fs_abc import FilesystemAbstract


class SSHFS(FilesystemAbstract):
    def parse_remote(self) -> Tuple[str, str, str]:
        remote_str = self.config.remote
        user, hostname, dir = "", "", ""
        if "@" in remote_str:
            user, hostname = remote_str.split("@")
        else:
            hostname = remote_str

        if ":" in hostname:
            hostname, dir, *rest = hostname.split(":")

            if len(rest):
                dirlist = [dir]
                dirlist = dirlist + rest
                dir = ":".join(dirlist)

        return user, hostname, dir

    def format_remote(self) -> str:
        remote_str = ""
        if self.user:
            remote_str = f"{self.user}@"

        if not self.hostname:
            raise ValueError("host must not be None")
        remote_str = f"{remote_str}{self.hostname}:"

        if self.dir:
            remote_str = f"{remote_str}{self.dir}"
        return remote_str

    def format_cmd(self):
        remote_str = self.format_remote()

        if not self.mount_point:
            raise ValueError("mount_point must not be None")

        sshfs_cmd = f"sshfs {remote_str} {self.mount_point}"
        return sshfs_cmd

    def validate(self):
        mount_cmd = self.format_cmd()
        if mount_cmd:
            return True
        else:
            return False

    def mount(self):
        mount_cmd = self.format_cmd()
        sh = Shell()
        sh.run(mount_cmd)
