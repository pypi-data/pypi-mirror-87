import logging

import click
from devcli.context import DevCliContext


@click.group()
@click.pass_context
@click.option('--verbose/--verbose-of', default=False)
@click.option('--profile', default=None)
def cli(ctx, verbose, profile):
    
    ctx.obj=DevCliContext.from_config_file(profile)
    print(ctx.obj)
    if verbose:
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


