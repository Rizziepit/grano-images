import os

from flask import Blueprint, abort, send_file

from grano import authz
from grano.core import app
from grano.model import File
from grano.images import logic
from grano.lib.args import object_or_404


IMAGE_CONFIG = app.config.get('IMAGE_CONFIG', {})
IMAGE_CONFIG = logic.validate_config(IMAGE_CONFIG)

blueprint = Blueprint('images', __name__)


@blueprint.route('/api/1/files/_image/<file_name>-<id>-<config_name>.png', methods=['GET'])
def generate(id, file_name, config_name):
    filepath = logic.get_file_location(file_name, id, config_name)
    if not os.path.exists(filepath):
        file = object_or_404(File.by_id(id))
        if config_name not in IMAGE_CONFIG:
            abort(404)
        try:
            logic.validate_file(file)
        except ValueError:
            return abort(400, "File is not a supported image format")
        config = IMAGE_CONFIG.get(config_name)
        new_file = logic.transform(file, (config['width'], config['height']))
        logic.store_file(new_file, filepath)

    return send_file(filepath)
