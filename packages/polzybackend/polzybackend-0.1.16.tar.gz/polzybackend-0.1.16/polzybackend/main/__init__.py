from flask import Blueprint

bp = Blueprint('main', __name__)

from polzybackend.main import routes