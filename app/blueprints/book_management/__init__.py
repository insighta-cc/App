from flask import Blueprint

book_management_bp = Blueprint('book_management', __name__)

from . import routes, models
