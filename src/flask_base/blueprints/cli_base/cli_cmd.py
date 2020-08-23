import sys
from itertools import chain

import click
from flask import current_app
from flask.cli import with_appcontext


class Environment:
    def __init__(self):
        self.verbose = False

    def log(self, msg, *args):
        """Logs a message to stderr."""
        output = msg
        if args:
            msg_iter = chain((msg,), map(str, args))
            output = "\n\t".join(msg_iter)
        click.echo(output, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_environment = click.make_pass_decorator(Environment, ensure=True)


@click.group(
    "app", help="a top level group for app commands.",
)
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode.")
@pass_environment
def app_group(ctx, verbose):
    ctx.verbose = verbose


@app_group.command("info", help="display info about the app.")
@with_appcontext
@pass_environment
def info(ctx):
    data = {"current_app":current_app,"environment":current_app.config.get('ENV')}
    display_data = [f"{k}: {v}" for k,v in data.items()]
    ctx.log("App info:", *display_data)



