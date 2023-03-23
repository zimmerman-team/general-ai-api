# Routes

## Expansion
To add aditional routes, create a new file in this routes directory.

```
from flask import Blueprint

bp = Blueprint('<NAME>', __name__, <url_prefix='<NAME> if desired>')

@bp.route('/', methods=['GET'])
def <NAME>():
    # Any execution steps
    return '<RESULT>'
```

## Available endpoints
- `/`: The central route registered in the app.
- `/health-check`: available to check liveness of the API.
