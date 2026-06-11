from flask import Blueprint
solutions_bp = Blueprint('solutions', __name__)
from . import routes
