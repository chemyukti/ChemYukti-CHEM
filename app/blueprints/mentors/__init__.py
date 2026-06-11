from flask import Blueprint
mentors_bp = Blueprint('mentors', __name__)
from . import routes
