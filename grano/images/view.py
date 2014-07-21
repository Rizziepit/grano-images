from flask import Blueprint, abort

from grano import authz
from grano.core import app, celery, db
from grano.model import File
from grano.images import logic
from grano.lib.serialisation import jsonify
from grano.lib.args import object_or_404


IMAGE_CONFIG = app.config.get('IMAGE_CONFIG', {})
IMAGE_CONFIG = logic.validate_config(IMAGE_CONFIG)

blueprint = Blueprint('images', __name__)


@celery.task
def _update_image(file_id, config_name):
    file = File.by_id(file_id)
    if file is None:
        return
    config = IMAGE_CONFIG.get(config_name)
    new_file = logic.transform(file, (config['width'], config['height']))
    url = logic.make_url(file, config_name)
    logic.upload(new_file, url)
    # TODO: decide how we want to store url, if at all
    #file.properties.update({'value_string': url})
    db.session.commit()


@blueprint.route('/api/1/files/<id>/_image/<config>', methods=['GET'])
def generate(id, config):
    file = object_or_404(File.by_id(id))
    authz.require(authz.project_edit(file.project))
    if config not in IMAGE_CONFIG:
        abort(404)
    try:
        logic.validate_file(file)
    except ValueError:
        return abort(400, "File is not a supported image format")
    _update_image.delay(id, config)
    return jsonify(file)
