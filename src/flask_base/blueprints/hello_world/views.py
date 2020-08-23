from flask import request, jsonify, Blueprint, current_app as app
from .bp_config import bp


@bp.route("/")
def hello_world():
    return "Hello, World!"

