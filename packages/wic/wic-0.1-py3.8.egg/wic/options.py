import click
import isystem.connect as ic


@click.group()
@click.pass_context
def options(ctx):
    global cmgr
    global ideCtrl
    cmgr = ctx.obj.cmgr
    ideCtrl = ic.CIDEController(cmgr)
    pass


def raise_is_option_dynamic(ctx, option):
    raise_option_exists(ctx, option)
    if is_option_dynamic(option):
        return option
    else:
        raise click.BadParameter(f"Option {option} is not dynamic.")


def raise_option_exists(ctx, option):
    if option_exists(option):
        return option
    else:
        raise click.BadParameter(f"Option {option} not valid option.")


@options.command(help="Set option")
@click.option("--option", "-o", callback=raise_option_exists, required=True, help="Option")
@click.option("--value", "-v", required=True, help="New value")
def set(option, value):
    ideCtrl.setOption(option, value)
    click.echo(f"{get_option_str(option)}")


@options.command(help="Get option")
@click.option("--option", "-o", callback=raise_option_exists, required=True, help="Option")
def get(option):
    click.echo(f"{get_option_str(option)}")


@options.command(help="Add entry to option list")
@click.option("--option", "-o", callback=raise_is_option_dynamic, required=True, help="Otion list")
def add(option):
    ideCtrl.addDynamicOption(option)
    click.echo(f"{get_option_int(option)-1}")


@options.command(help="Clear option list")
@click.option("--option", "-o", callback=raise_is_option_dynamic, required=True, help="Clear all option entries")
def clear(option):
    ideCtrl.removeDynamicOption(option, -1)
    click.echo("All entries removed")


def option_exists(option):
    return ideCtrl.optionExists(option)


def is_option_dynamic(option):
    try:
        ideCtrl.getDynamicOptionSize(option)
        return True
    except:
        return False


def get_option_str(option):
    return ideCtrl.getOptionStr(option)


def get_option_int(option):
    return ideCtrl.getOptionInt(option)


def get_option_json(option):
    return ideCtrl.getOptionJSON(option)
