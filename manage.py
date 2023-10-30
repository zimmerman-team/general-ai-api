from os import environ

from flask import abort, request
from flask.cli import FlaskGroup

from api import create_app

# Initialise app
app = create_app()

# set up auth key for requests
authorized_keys = [environ.get('AIAPI_API_KEY', 'ZIMMERMAN')]

@app.before_request
def check_api_key():
    api_key = request.headers.get('Authorization')

    if api_key not in authorized_keys:
        abort(401)  # Unauthorized

# Enable flask group
cli = FlaskGroup(app)

# Start app
if __name__ == "__main__":
    cli()
