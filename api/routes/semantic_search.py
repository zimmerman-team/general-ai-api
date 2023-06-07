import os

from flask import Blueprint, request

from api.routes import util
from api.services.semantic_search.embedded_query import embedded_query, get_query_from_file
from api.services.semantic_search.embedding_features import embedded_features
from api.services.semantic_search.embedding_pipeline import embedding_pipeline

bp = Blueprint('semantic_search', __name__, url_prefix='/semantic-search')
DATASET_PATH = './api/services/semantic_search/data/'


@bp.route('/upload-dataset', methods=['post'])
def upload_dataset():
    """
    This is a post request where a dataset gets submitted, this triggers the following chain of actions:
    1. We store the dataset in services/semantic_search/data
    2. generate embeddings for the dataset
    3. store the embeddings in services/semantic_search/data postfixed with _with_embeddings
    """
    # ret can be a json return object or the content of the provided csv file
    file_ok, ret = util.check_file(request, '.csv')
    if not file_ok:
        return ret
    save_ok, filepath = util.save_file(ret, DATASET_PATH)
    if not save_ok:
        return filepath  # in this case the filepath is a jsonified return object

    # File has been saved, we now start our dataset embedding pipeline
    code, res = embedding_pipeline(filepath)

    return util.json_return(code, res)


@bp.route('/semantic-search-in-dataset', methods=['post'])
def semantic_search_in_dataset():
    """
    Get the dataset name, postfix it with _with_embeddings.csv and search for the provided query
    """
    dataset = request.form['dataset']
    dataset = dataset + '_with_embeddings.csv'
    dataset_path = os.path.join(DATASET_PATH, dataset)
    query = request.form['query']

    # Check if a file exists at filepath
    if not os.path.isfile(dataset_path):
        return util.json_return(400, "Embeddings with this name does not exist")
    # Execute the query
    code, res = embedded_query(dataset_path, query)

    return util.json_return(code, res)


@bp.route('/voice-based-semantic-search-in-dataset', methods=['post'])
def voice_based_semantic_search_in_dataset():
    """
    Get the dataset name, postfix it with _with_embeddings.csv and search for the provided query
    """
    dataset = request.form['dataset']
    dataset = dataset + '_with_embeddings.csv'
    dataset_path = os.path.join(DATASET_PATH, dataset)
    file_ok, ret = util.check_file(request, '.m4a')
    if not file_ok:
        return ret
    # Get query from file
    query = get_query_from_file(ret)

    # Check if a file exists at filepath
    if not os.path.isfile(dataset_path):
        return util.json_return(400, "Embeddings with this name does not exist")
    # Execute the query
    code, res = embedded_query(dataset_path, query)

    return util.json_return(code, res)


@bp.route('/embedding-features', methods=['post'])
def embedding_features():
    """
    tmp
    """
    dataset = request.form['dataset']
    dataset = dataset + '_with_embeddings.csv'
    dataset_path = os.path.join(DATASET_PATH, dataset)

    # Check if a file exists at filepath
    if not os.path.isfile(dataset_path):
        return util.json_return(400, "Embeddings with this name does not exist")
    # Execute the query
    code, res = embedded_features(dataset_path)

    return util.json_return(code, res)
