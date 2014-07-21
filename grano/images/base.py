from grano.core import app
from grano.interface import Startup
from grano.images.view import blueprint


class Installer(Startup):

    def configure(self, manager):
        app.register_blueprint(blueprint)
