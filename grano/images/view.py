import os

from flask import Blueprint
from flask import make_response, url_for

from grano.core import app


IMAGE_CONFIG = app.config.get('IMAGE_CONFIG', {})

blueprint = Blueprint('images', __name__)

