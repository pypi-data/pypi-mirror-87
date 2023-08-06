from pathlib import Path

import click
import isystem.connect as ic


@click.group(help="Manage download files")
@click.pass_context
def files(ctx):
    global cmgr
    global loadCtrl
    global ideCtrl
    cmgr = ctx.obj.cmgr
    loadCtrl = ic.CLoaderController(cmgr)
    ideCtrl = ic.CIDEController(cmgr)
    pass


@files.command(help="Add a new download file")
@click.option("--file", "-f", type=click.File('r', lazy=True), help="Path to download file")
@click.option("--code/--no-code", "-c/-nc", default=True, help="Load code")
@click.option("--symbols/--no-symbols", "-s/-ns", default=True, help="Load symbols")
def add(file, code, symbols):
    click.echo(f"Add '{file.name}'")

    new_index = count_files()

    download_config = ic.CDownloadConfiguration()
    download_config \
        .setCodeOffset(0) \
        .setSymbolsOffset(0) \
        .setDownloadFileFormat(detect_type(file.name))

    loadCtrl.addToDownloadList(download_config, ic.CLoaderController.DLIST_PRIMARY, file.name, '')

    set_option_load_code(new_index, code)
    set_option_load_symbols(new_index, symbols)

    click.echo(f"Type: {get_option_type(new_index)}")


@files.command(help="Clear all download files")
def clear():
    loadCtrl.clearDownloadList(ic.CLoaderController.DLIST_PRIMARY)
    click.echo('Download list cleared')


@files.command(help="List all download files")
def list():
    """ Prints all files in the list of download files and some of their options. """

    file_count = count_files()
    click.echo(f"Number of download files: {file_count}")

    # List some of current IDE Debug DownloadFiles File Options
    for i in range(0, file_count):
        printOptionPrefix = "/IDE/Debug.DownloadFiles.File[" + str(i) + "]"
        click.echo(f"{printOptionPrefix}.Path                {ideCtrl.getOptionStr(printOptionPrefix + '.Path')}")
        click.echo(f"{printOptionPrefix}.Options.Type        {get_option_type(i)}")
        click.echo(f"{printOptionPrefix}.Load                {ideCtrl.getOptionStr(printOptionPrefix + '.Load')}")
        click.echo(f"{printOptionPrefix}.Options.LoadCode    {get_option_load_code(i)}")
        click.echo(f"{printOptionPrefix}.Options.LoadSymbols {get_option_load_symbols(i)}")


def set_option_load_code(index, load):
    click.echo(f"Set Load Code: {load}")
    ideCtrl.setOption(f"/IDE/Debug.DownloadFiles.File[{index}].Options.LoadCode", load)


def set_option_load_symbols(index, load):
    click.echo(f"Set Load Symbols: {load}")
    ideCtrl.setOption(f"/IDE/Debug.DownloadFiles.File[{index}].Options.LoadSymbols", load)


def get_option_load_code(index):
    return ideCtrl.getOptionStr(f"/IDE/Debug.DownloadFiles.File[{index}].Options.LoadCode")


def get_option_load_symbols(index):
    return ideCtrl.getOptionStr(f"/IDE/Debug.DownloadFiles.File[{index}].Options.LoadSymbols")


def get_option_type(index):
    return ideCtrl.getOptionStr(f"/IDE/Debug.DownloadFiles.File[{index}].Options.Type")


def count_files():
    return ideCtrl.getDynamicOptionSize('/IDE/Debug.DownloadFiles.File')


def detect_type(path):
    ext = Path(path).suffix.lower()
    if ext == ".elf":
        return ic.CDownloadConfiguration.ftELF
    elif ext == ".s19":
        return ic.CDownloadConfiguration.ftMotorolaS
    else:
        raise Exception(f"Type {ext} not yet mapped.")
