from api.services.openai.prompt import prompt_with_storage

PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/chart_for_csv_file_previous_suggestions.json'


def suggest_chart_for_csv_file(df):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    :param df: pandas dataframe containing the content of the uploaded CSV file
    """
    df_head = df.head().to_string()
    prompt = f"""Given the following sample dataframe:\n{df_head}\n
        What are 5 chart types you would use to visualize this data?
        And which columns would you use in which dimension of the charts?
        If there is no fitting chart, please state so."""

    return prompt_with_storage(df_head, PREVIOUS_SUGGESTIONS_FILE, prompt)
