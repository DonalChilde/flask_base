from flask import render_template
from .bp_config import bp


@bp.route("/")
@bp.route("/<name>")
def hello_world(name=None):
    if name is None:
        from_name = "Bob"
    else:
        from_name = name
    return render_template("hello_world.html", name=from_name)
