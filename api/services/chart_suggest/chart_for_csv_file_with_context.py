import json

from api.services.openai.prompt import prompt_with_storage

PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/data/chart_csv_context_previous_suggestions.json'
DX_CHART_DEFINITIONS = './api/services/chart_suggest/data/dx_charts.json'


def suggest_chart_for_csv_file_with_context(df):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    :param df: pandas dataframe containing the content of the uploaded CSV file
    """
    df_head = df.head().to_string()
    chart_descriptions = get_all_charts_semantic_context()

    prompt = f"""Given the following sample dataframe:\n{df_head}\n
        and given the following chart descriptions:\n{chart_descriptions}\n
        What are 5 chart types you would use to visualize this data?
        And which columns would you use in which dimension of the charts?
        If there is no fitting chart, please state so."""

    return prompt_with_storage(df_head, PREVIOUS_SUGGESTIONS_FILE, prompt)


def get_all_charts_semantic_context():
    """
    Get the semantic context for a given chart type.

    :param chart: the chart type
    :return: the semantic context
    """
    with open(DX_CHART_DEFINITIONS, 'r') as f:
        chart_definitions = json.load(f)
        semantic_chart_definitions = []
        for chart in chart_definitions:
            semantic_chart_definitions.append(chart_definitions[chart]['semantic'])
        semantic_chart_definitions = '\n'.join(semantic_chart_definitions)
        return semantic_chart_definitions
