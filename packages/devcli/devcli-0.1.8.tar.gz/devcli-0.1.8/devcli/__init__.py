__version__ = '0.1.0'

import importlib
import logging
import pkgutil

from devcli.context import DevCliContext
from devcli.devcli import cli

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


def load_plugins():
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in pkgutil.iter_modules()
        if name.startswith('devcli')
    }


plugins = load_plugins()


def run():

    cli(obj={})