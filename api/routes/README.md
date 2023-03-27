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
- `/`: GET: The central route registered in the app.
- `/health-check`: GET: available to check liveness of the API.
- `/chart-suggest/csv-dataset`: POST: submit form-data with `file` as a CSV file, returns recommendations for charts to use on that dataset.
- `/chart-suggest/csv-dataset`: POST: submit form-data with `file` as a CSV file, and `chart` as a string type of chart ([current supported charts](../services/chart_suggest/dx_charts.json)), returns a recommendation which fields to use for the provided chart and data.
