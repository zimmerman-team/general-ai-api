from flask import Blueprint, request

from api.routes import util
from api.services.openai.prompt import prompt_with_storage, prompt_with_storage_completion

PREVIOUS_SUGGESTIONS_FILE = './api/services/prompts/data/prompts.json'
STABLE_PREVIOUS_SUGGESTIONS_FILE = './api/services/prompts/data/stablelm_prompts.json'
LLAMA_PREVIOUS_SUGGESTIONS_FILE = './api/services/prompts/data/llama_prompts.json'

bp = Blueprint('prompts', __name__, url_prefix='/prompts')


@bp.route('/general', methods=['post'])
def general():
    """
    The input is a prompt string which we will directly pass to the LLM.
    """
    # ret can be a json return object or the content of the provided csv file
    prompt = request.form['prompt']
    code, res = prompt_with_storage(prompt, PREVIOUS_SUGGESTIONS_FILE, prompt)

    return util.json_return(code, res)


@bp.route('/extract-search-term', methods=['post'])
def extract_search_term():
    """
    The input is a prompt string which we will directly pass to the LLM.
    """
    # ret can be a json return object or the content of the provided csv file
    prompt = request.form['prompt']
    enriched_prompt = f"""First, I will give you some context, then I will ask you a question about a given topic.
        The context: Your job is to convert the given topic with one search term which will lead to functional results on the Kaggle datasets page.
        Keep it as concise as possible. Do not include the words: 'data', 'dataset', 'Dataset', 'Report' or 'report' in your answer.
        We are looking for as few words as possible, to broaden the search.
        The Topic is: '{prompt}'. The search term is:"""
    code, res = prompt_with_storage_completion(
        enriched_prompt,
        PREVIOUS_SUGGESTIONS_FILE,
        enriched_prompt,
        temperature=0.1
    )

    return util.json_return(code, res)
