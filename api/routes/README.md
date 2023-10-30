# Routes

## Expansion
To add aditional routes, create a new file in this routes directory.

```
from flask import Blueprint

bp = Blueprint('<NAME>', __name__, <url_prefix='<NAME>')

@bp.route('/', methods=['GET'])
def <NAME>():
    # Any execution steps
    return '<RESULT>'
```

## Available endpoints
- `/`: GET: The central route registered in the app.
- `/health-check`: GET: available to check liveness of the API.
- `/chart-suggest/csv-dataset`: POST: submit form-data with `file` as a CSV file, returns recommendations for charts to use on that dataset.
- `/chart-suggest/csv-dataset-with-context`: POST: submit form-data with `file` as a CSV file, returns recommendations for charts to use on that dataset, based on the charts that are provided in [the dx charts description](../services/chart_suggest/dx_charts.json).
- `/chart-suggest/chart-from-data`: POST: submit form-data with `file` as a CSV file, and `chart` as a string type of chart ([current supported charts](../services/chart_suggest/dx_charts.json)), returns a recommendation which fields to use for the provided chart and data.
- `/chart-suggest/ai-report-builder`: POST: submit form-data with `file` as a CSV file. This then creates a list of suggested charts.
- `/chart-suggest/ai-report-builder-from-existing`: POST: submit query params `id` as a DX dataset ID. This then creates a list of suggested charts for the specified dataset.
- `/semantic-search/upload-dataset`: POST: provide a dataset in csv form. This generates and stores embeddings for this dataset.
- `/semantic-search/semantic-search-in-dataset`: POST: provide a dataset in csv form. This generates and stores embeddings for this dataset.
- `/semantic-search/voice-based-semantic-search-in-dataset`: POST: provide a dataset id and the audio file, we search the query after transpiling the audio to a text query.
