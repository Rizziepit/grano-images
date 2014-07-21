import os
import re
import shutil
from StringIO import StringIO
from urlparse import urlparse

import colander
from PIL import Image

from grano.images.constants import ACCEPTED_MIMETYPES


def aspect_ratio(width, height):
    return float(width) / float(height)


def calculate_crop_box((config_w, config_h), (w, h)):
    """ Returns the largest crop box such that w / h == config_w / config_h.
        The crop origin is the center. """
    other_ratio = aspect_ratio(w, h)
    config_ratio = aspect_ratio(config_w, config_h)
    if config_ratio == other_ratio:
        return (0, 0, w, h)
    elif config_ratio > other_ratio:
        # need to decrease height
        new_h = other_ratio / config_ratio * h
        origin_y = (h - new_h) / 2.0
        return (0, int(round(origin_y)), w, int(round(origin_y + new_h)))
    else:
        # need to decrease width
        new_w = config_ratio / other_ratio * w
        origin_x = (w - new_w) / 2.0
        return (int(round(origin_x)), 0, int(round(origin_x + new_w)), h)


def make_url(file, config_name, file_name=None):
    # TODO: base URL on some image upload setting
    return 'file://%s' % os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../images',
        '%s-%s-%s.png' % (
            file_name or os.path.splitext(os.path.basename(file.file_name))[0],
            file.id,
            config_name
        )
    ))


def upload(file, url):
    """ Copy file to specified url (only local file system supported for now) """
    result = urlparse(url)
    if result.scheme == 'file':
        assert result.netloc == ''
        dir = os.path.dirname(result.path)
        if not os.path.exists(dir):
            os.makedirs(dir)
        with open(result.path, 'wb') as f:
            file.seek(0)
            shutil.copyfileobj(file, f)
    else:
        raise ValueError("Only 'file' protocol supported at the moment")


def transform(file, size=None):
    sio = StringIO(file.data)
    image = Image.open(sio)
    image.load()
    sio.close()
    if size is not None:
        # crop and scale ourselves since Image.thumbnail
        # doesn't change the aspect ratio
        crop_box = calculate_crop_box(size, image.size)
        image = image.crop(crop_box)
        image = image.resize(size, Image.ANTIALIAS)
    out = StringIO()
    image.save(out, 'PNG')
    return out


def validate_file(file):
    """ Simply checks that we accept the file mimetype """
    if file.mime_type not in ACCEPTED_MIMETYPES:
        raise ValueError("Invalid image MIME type '%s'" % file.mime_type)


class ImageConfigError(Exception):
    pass


def validate_config(config_dict):
    class ConfigValidator(colander.MappingSchema):
        height = colander.SchemaNode(
            colander.Integer(),
            validator=colander.Range(min=1)
        )
        width = colander.SchemaNode(
            colander.Integer(),
            validator=colander.Range(min=1)
        )

    class ItemValidator(colander.TupleSchema):
        name = colander.SchemaNode(
            colander.String(),
            validator=colander.Regex(
                re.compile(r'\w+$'),
                msg='Image config name may only contain alphanumeric characters'
            )
        )
        config = ConfigValidator()

    class ConfigsValidator(colander.SequenceSchema):
        configs = ItemValidator()

    try:
        config_list = config_dict.items()
        sane = ConfigsValidator().deserialize(config_list)
        return dict(sane)
    except colander.Invalid as e:
        raise ImageConfigError(str(e))
