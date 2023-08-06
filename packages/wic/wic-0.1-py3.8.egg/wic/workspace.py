import click
import isystem.connect as ic


@click.group()
@click.pass_context
def ws(ctx):
    global wsCtrl
    wsCtrl = ic.CWorkspaceController(ctx.obj.cmgr)
    pass


@ws.command(help="Save workspace")
def save():
    wsCtrl.save()
    click.echo("Workspace saved")


@ws.command(help="Close workspace")
def close():
    wsCtrl.close()
    click.echo("Workspace closed")
