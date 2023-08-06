import isystem.connect as ic
import click

from wic.Config import Config
from wic.files import files
from wic.options import options
from wic.workspace import ws


@click.group(help="Command line interface for winIDEA v0.2")
@click.option("--workspace", "-ws", type=click.File('r', lazy=True), help="Path to winIDEA workspace")
@click.option("-id", help="Connect to winIDEA instance ID")
@click.version_option(ic.getModuleVersion(), prog_name="winIDEA SDK")
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx, workspace, id):
    global cmgr
    cmgr = ic.ConnectionMgr()
    global config
    config = Config(cmgr, workspace, id)
    ctx.obj = config
    pass


@click.command(help="Start winIDEA")
def start():
    config.connect()
    pass


@click.command(help="List winIDEA instances")
def list():
    connection_config = ic.CConnectionConfig()
    instances = ic.VectorWinIDEAInstanceInfo()
    address = ''
    cmgr.enumerateWinIDEAInstances(address, connection_config, instances)

    for instance in instances:
        click.echo(f"Workspace: '{instance.getWorkspace()}")
        click.echo(f"Inst. Id : '{instance.getInstanceId()}")
        click.echo(f"TCP port : '{instance.getTcpPort()}'\n")


@click.command(help="Download files to target")
def download():
    config.connect()
    loader = ic.CLoaderController(cmgr)
    click.echo("Start downloading...")
    res = loader.download()
    click.echo(f"Download finished: {res}")


cli.add_command(files)
cli.add_command(options)
cli.add_command(ws)
cli.add_command(download)
cli.add_command(start)
cli.add_command(list)

if __name__ == '__main__':
    cli()

