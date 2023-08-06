import isystem.connect as ic
import click

from wic.Config import Config
from wic.files import files
from wic.options import options
from wic.workspace import ws


@click.group(help="Command line interface for winIDEA v0.1")
@click.option("--workspace", "-ws", type=click.File('r', lazy=True), help="Path to winIDEA workspace")
@click.version_option(ic.getModuleVersion(), prog_name="WinIDEA SDK")
@click.help_option('-h', '--help')
@click.pass_context
def cli(ctx, workspace):
    global cmgr
    cmgr = ic.ConnectionMgr()
    ctx.obj = Config(cmgr)
    # cmgr.initLogger("wic", "wic.log", ic.CLogger.PYTHON)
    if workspace is not None:
        click.echo(f"Using workspace: {workspace.name}")
        cmgr.connectMRU(workspace.name)
    else:
        cmgr.connectMRU('')
    pass


@click.command(help="Download files to target")
def download():
    loader = ic.CLoaderController(cmgr)
    click.echo("Start downloading...")
    res = loader.download()
    click.echo(f"Download finished: {res}")


cli.add_command(files)
cli.add_command(options)
cli.add_command(ws)
cli.add_command(download)

if __name__ == '__main__':
    cli()

