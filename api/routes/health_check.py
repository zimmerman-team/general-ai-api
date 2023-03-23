from flask import Blueprint, Response

bp = Blueprint('health_check', __name__, url_prefix='/health-check')


@bp.route('/', methods=['GET'])
def health_check():
    # Return a 200 OK response as JSON
    return Response('OK', status=200, mimetype='application/json')
