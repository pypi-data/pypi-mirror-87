import click

from .settings import Settings


class Context:
    def __init__(self, app_name, settings={"filesystem": ""}):
        self.app_name = app_name
        if not self.app_name:
            raise ValueError("app_name must not be empty")
        self.config_dir = click.get_app_dir(self.app_name)
        self.settings = Settings(**settings)
