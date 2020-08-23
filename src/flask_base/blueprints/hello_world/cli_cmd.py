from flask_base.blueprints.cli_base.cli_cmd import pass_environment, app_group
import click


@app_group.group("hello_world", help="A collection of commands related to hello_world")
@pass_environment
def hello_world(ctx):
    pass


@hello_world.command("greet")
@click.argument("name")
@pass_environment
def greet(ctx, name):
    ctx.log(f"Hello World! --from {name}")
