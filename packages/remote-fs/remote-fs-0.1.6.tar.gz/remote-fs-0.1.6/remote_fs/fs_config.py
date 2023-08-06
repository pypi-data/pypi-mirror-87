import errno
import json
import os

from pathvalidate import sanitize_filename


class FilesystemConfig:
    def __init__(
        self,
        filesystem="",
        mount_point="",
        remote="",
        hostname="",
        user="",
        dir="",
        option=[],
    ):
        self.filesystem = filesystem
        self.mount_point = mount_point
        self.remote = remote
        self.hostname = hostname
        self.user = user
        self.dir = dir
        # NOTE: missing s on purpose
        self.options = option

    def args(self):
        return (
            self.hostname,
            self.mount_point,
            {"user": self.user, "dir": self.dir, "options": self.options},
        )

    def save(self, name, config_dir):
        self.name = name
        basename = sanitize_filename(f"{name}.json")
        filename = os.path.join(config_dir, basename)
        os.makedirs(config_dir, exist_ok=True)
        json.dump(self.__dict__, open(filename, "w"))

    def load(self, name, config_dir):
        basename = f"{name}.json"
        filename = os.path.join(config_dir, basename)
        self.__dict__.update(json.load(open(filename, "r")))

    @classmethod
    def from_file(cls, filename):
        fs_config = cls()
        fs_config.__dict__.update(json.load(open(filename, "r")))
        return fs_config

    @staticmethod
    def ls_configs(config_dir) -> list[tuple[str, str]]:
        names = []
        for file in os.listdir(config_dir):
            if file.endswith(".json"):
                config_filename = os.path.join(config_dir, file)
                config_json = json.load(open(config_filename, "r"))
                names.append((config_json["name"], config_filename))
        return names

    @staticmethod
    def ls_files(config_dir) -> list[str]:
        files = []
        for file in os.listdir(config_dir):
            if file.endswith(".json"):
                files.append(os.path.join(config_dir, file))
        return files
