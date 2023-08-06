from __future__ import print_function

import click
import yaml
import os
import functools
import importlib
import sys

from idiary.version import __version__
from idiary.utils import *

install_path = os.path.dirname(os.path.abspath(__file__))

click.option = functools.partial(click.option, show_default=True)
@click.group(help="The idiary command line interface.")
@click.version_option(version=__version__)
@click.option("--local_rank", default=-1, type=int, help="The rank of this process")
def main(local_rank):
    pass


@click.command(help="Init idiary with a local path.")
@click.argument("path", required=True, type=str)
@click.option("--new", type=bool, default=False, help="Re-init with a new address.")
@click.option("--copy", type=bool, default=False, help="Copy the old files into the new address.")
def init(path, new, copy):
    log = set_logger("Init")
    savefile = os.path.join(install_path, "Diary_address.yaml")
    path = os.path.abspath(path)
    reinit = False
    
    if os.path.exists(savefile):
        reinit = True
        with open(savefile, "r") as fp:
            old_path = yaml.load(fp, Loader=yaml.FullLoader)
    
    if new is False and reinit:
        log.info("Initialize with address {} before.\nDon't initialize again.\nSet 'new' True if you want to reinit.".format(old_path))
        sys.exit()
    else:
        os.makedirs(path)
        if reinit and copy:
            copy_files(old_path, path, "Init")
        with open(savefile, "w") as fp:
            yaml.dump(path, fp)
        log.info("Initialize idiary with address:{}".format(path))

main.add_command(init)


@click.command(help="Current idiary local path.")
def PATH():
    log = set_logger("Path")
    savefile = os.path.join(install_path, "Diary_address.yaml")
    
    if os.path.exists(savefile):
        with open(savefile, "r") as fp:
            path = yaml.load(fp, Loader=yaml.FullLoader)
        log.info("Idiary Path: {}".format(path))
    else:
        log.info("Not initialized. Please first init Idiary with a local path by `idiary init`")

main.add_command(PATH)

if __name__ == "__main__":
    main()
