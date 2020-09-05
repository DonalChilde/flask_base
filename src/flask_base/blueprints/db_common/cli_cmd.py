import click
from flask import current_app
from flask.cli import with_appcontext

from flask_base.blueprints.cli_base.cli_cmd import app_group, pass_environment
from flask_base.extensions import db as flask_db


@app_group.group("db")
def db():
    pass


@db.command("reset")
@with_appcontext
@pass_environment
def reset(ctx):
    flask_db.drop_all(app=current_app)
    flask_db.create_all(app=current_app)


@db.command("seed_data")
@click.option("-t", "--test_data", is_flag=True, help="Seed test data.")
@with_appcontext
@pass_environment
def seed_data(ctx, test_data=False):
    pass
