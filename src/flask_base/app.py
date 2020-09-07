"""Entry point for flask app.

derived from 
     https://github.com/karec/cookiecutter-flask-restful/blob/master/%7B%7Bcookiecutter.project_name%7D%7D/%7B%7Bcookiecutter.app_name%7D%7D/app.py

    """

from flask import Flask

from flask_base.blueprints import cli_base, db_common, hello_world, users
from flask_base.blueprints.cli_base.cli_cmd import app_group
from flask_base.config import (
    Config,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    get_env_variable,
)
from flask_base.extensions import db


def create_app(config_class=None):
    """Application factory, used to create application

    if config_class is passed in, use an instance.
    """
    app = Flask(__name__)
    if config_class is None:
        flask_env = get_env_variable("FLASK_ENV")
        if flask_env == "development":
            config_class = DevelopmentConfig()
        elif flask_env == "production":
            config_class = ProductionConfig()
        else:
            raise Exception("FLASK_ENV is not set to a known value.")
    app.config.from_object(config_class)
    app.config.update({"CONFIG_OBJECT": str(type(config_class))})

    # TODO handle secrets for different env senarios. option - same file or separate files?
    if isinstance(config_class, DevelopmentConfig):
        app.config.from_envvar("SECRETS_CFG")
    elif isinstance(config_class, TestingConfig):
        pass
    elif isinstance(config_class, ProductionConfig):
        app.config.from_envvar("SECRETS_CFG")
    elif isinstance(config_class, Config):
        pass
    else:
        message = "Object %s is not a Config object." % config_class.__name__
        raise Exception(message)

    configure_extensions(app)
    configure_apispec(app)
    register_blueprints(app)
    register_cli(app)

    return app


def configure_extensions(app):
    """configure flask extensions
    """
    db.init_app(app)


def configure_apispec(app):
    """Configure APISpec for swagger support
    """
    pass


def register_blueprints(app):
    """register all blueprints for application
    """
    app.register_blueprint(hello_world.bp_config.bp)
    app.register_blueprint(cli_base.bp_config.bp)


def register_cli(app):
    app.cli.add_command(app_group)
