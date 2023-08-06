import sys

import click
from shell import CommandError

import remote_fs.fs as fs
from .ctx import Context
from remote_fs.fs_config import FilesystemConfig


@click.group()
@click.pass_context
@click.option(
    "--smbfs",
    "filesystem",
    flag_value="smbfs",
    default=False,
    help="mounts via mount_smbfs (darwin only)",
)
@click.option(
    "--sshfs", "filesystem", flag_value="sshfs", default=False, help="mounts via sshfs"
)
def cli(click_ctx, filesystem):
    click_ctx.obj = Context("remote-fs", settings={"filesystem": filesystem})


@cli.command()
@click.pass_context
@click.argument("mount_point", required=True)
@click.option("--load", is_flag=True, default=False)
@click.option("--name", required=False)
@click.option(
    "--remote", required=False, help="full hostname string, e.g. user@hostname:dir"
)
@click.option("--hostname", required=False)
@click.option("--user", required=False)
@click.option("--dir", required=False)
@click.option(
    "--option",
    "-o",
    multiple=True,
    default=["reconnect,ServerAliveInterval=15,ServerAliveCountMax=3"],
)
def mount(click_ctx, mount_point, load, name, **kwargs):
    ctx: Context = click_ctx.obj

    config = FilesystemConfig(
        filesystem=ctx.settings.filesystem, mount_point=mount_point, **kwargs
    )

    if name is not None:
        config.save(name, ctx.config_dir)
    elif load:
        config.load(mount_point, ctx.config_dir)
    else:
        raise ValueError("Name must be passed if not loading a config")

    filesystem = fs.create_fs(config)

    try:
        filesystem.mount()
        click.echo(f"mounted {config.mount_point}")
    except CommandError as e:
        click.echo(f"failed to mount {config.mount_point}: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
@click.argument("name")
def unmount(click_ctx, name):
    ctx: Context = click_ctx.obj
    configs = FilesystemConfig.ls_configs(ctx.config_dir)
    target_config: tuple[str, str] = None
    for config in configs:
        if config[0] == name:
            target_config = config

    if not target_config:
        raise ValueError(f"{name} is not a saved config")

    config = FilesystemConfig.from_file(target_config[1])
    try:
        fs.FilesystemAbstract.unmount(config.mount_point)
        click.echo(f"unmounted {config.mount_point}")
    except CommandError as e:
        click.echo(f"failed to unmount {config.mount_point}: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
@click.argument("resource", help="either configs or mounts")
def list(click_ctx, resource):
    ctx: Context = click_ctx.obj
    if resource == "configs":
        for name, filename in FilesystemConfig.ls_configs(ctx.config_dir):
            click.echo(f'{name}\t"{filename}"')
    if resource == "mounts":
        fs.ls_mounts(ctx.config_dir)
