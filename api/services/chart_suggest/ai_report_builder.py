from api.services.openai.assistants import cb_assistant_prompt_with_storage

PREVIOUS_SUGGESTIONS_FILE = './api/services/chart_suggest/data/ai_report_builder_previous_suggestions.json'
DX_CHART_DEFINITIONS = './api/services/chart_suggest/data/dx_charts.json'


def ai_report_builder_chart_selector(df):
    """
    Use openAI to suggest a chart type for the given columns and some example rows.

    :param df: pandas dataframe containing the content of the uploaded CSV file
    """
    df_head = _sample_df(df)

    prompt = f"""Given your known chart descriptions, and given the following sample dataframe:\n{df_head}\n
        What are 3 chart types you would use to visualize this data?
        Please return a json list, containing strings of the chart types in lower case and no spaces.
        If there is no fitting chart, please return an empty json list. Only return the actual json content, no additional text."""  # NOQA: E501
    return cb_assistant_prompt_with_storage(df_head, PREVIOUS_SUGGESTIONS_FILE, prompt)


def _sample_df(df):
    """
    Sample size should be more than 4 rows, but not too large as to not overwhelm the LLM with too much information.

    :param df: pandas dataframe
    """
    n_rows_df = df.shape[0]
    n_head = n_rows_df
    if n_rows_df > 50:
        n_head = 50
    head = df.head(n_head).to_string()
    while len(head) > 100000:  # We can send up to 128k tokens, this limits the dataset size.
        n_head = n_head // 2
        if n_head == 0:
            n_head = 1
            break
        head = df.head(n_head).to_string()
    return head
