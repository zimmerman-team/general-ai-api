from flask import Flask

from api.routes import base_route, health_check


def create_app():
    # create and configure the app
    app = Flask(__name__)
    # load additional settings
    app.config.from_pyfile('settings.py')

    # Register all blueprints from the api.routes package.
    app.register_blueprint(base_route.bp)
    app.register_blueprint(health_check.bp)

    return app
