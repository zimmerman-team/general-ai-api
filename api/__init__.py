from flask import Flask

from api.routes import base_route, chart_suggest, health_check, prompts


def create_app():
    # create and configure the app
    app = Flask(__name__)
    # load additional settings
    app.config.from_pyfile('settings.py')

    # Register all blueprints from the api.routes package.
    app.register_blueprint(base_route.bp)
    app.register_blueprint(health_check.bp)
    app.register_blueprint(chart_suggest.bp)
    app.register_blueprint(prompts.bp)

    return app
