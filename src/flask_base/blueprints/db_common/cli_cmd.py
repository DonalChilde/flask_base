import click
from flask import current_app
from flask.cli import with_appcontext

from flask_base.blueprints.cli_base.cli_cmd import app_group
from flask_base.extensions import db as flask_db


@app_group.group("db")
def db():
    pass


@db.command("reset")
@with_appcontext
@click.pass_context
def reset(ctx):
    flask_db.drop_all(app=current_app)
    flask_db.create_all(app=current_app)
