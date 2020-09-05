from flask import Blueprint

bp = Blueprint(
    "db_common", __name__, url_prefix="/db_common", template_folder="templates"
)
