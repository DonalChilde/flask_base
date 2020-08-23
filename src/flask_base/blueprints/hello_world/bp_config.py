from flask import Blueprint

bp = Blueprint("hello_world", __name__, url_prefix="/hello_world")
