# Grano Images

[grano](http://grano.cc/) is a toolkit for building journalistic social network analysis applications on the web. This package adds simple image hosting and manipulation functionality
to grano.


## Installation

``grano-images`` requires that you have installed and configured [grano](http://grano.cc/). Please refer to [grano's documentation](http://docs.grano.cc/) for further instructions. _Before_ installing ``grano-images`` you also need to install the following external dependencies:

* libjpeg (for JPEG support)
* zlib (for PNG support)

To install the package from GitHub, you need to follow these steps from within the virtual environment in which ``grano`` has been installed:


```bash
git clone https://github.com/Rizziepit/grano-images.git
cd grano-images
python setup.py develop
```


After installing the package, you will still need to enable this plugin. Add the entry ``images`` to the ``PLUGINS`` variable in your grano settings file. If you have no other plugins installed, try this:

```python
PLUGINS = ['images']
```


## Configuration

The ``IMAGE_DIR`` and ``IMAGE_CONFIG`` variables need to be set before using ``grano-images``. Setting ``IMAGE_DIR`` to this will store images in `static/images` in your grano directory:

```python
IMAGE_DIR = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'static/images'
)
```

This setting will enable the endpoint ``/api/1/files/_image/<file_name>-<id>-thumbnail.png`` which generates and serves a 64 by 64 pixel image:

```python
IMAGE_CONFIG = {
    'thumbnail': {
        'width': 64,
        'height': 64
    }
}
```
