import os


def json_return(code, data=None, error=None, error_message=None):
    """
    Return a jsonify-d flask object with the provided error code. Defaults to 204.

    :param code: the HTTP status code
    :param data: the data to return, can be an object, or a string
    """
    if error:
        return {'code': code, 'error': error, 'error_message': error_message}, code
    if data:
        return {'code': code, 'result': data}, code
    else:
        return {'code': 204, 'result': 'We were unable to process, please contact your system administrator.'}, 204


def check_file(request, filetype):
    """
    Check whether or not a file was uploaded in the correct filetype with a name.

    :param request: the request object
    :param filetype: the filetype to check for
    :return: an error message if not, otherwise return the csv file continue the process
    """
    if 'file' not in request.files:
        return False, json_return(400, 'No file uploaded')

    request_file = request.files['file']
    if request_file.filename == '':
        return False, json_return(400, 'Empty filename')

    if not request_file.filename.endswith(filetype):
        return False, json_return(400, f'Uploaded file was not recognized as a {filetype} file')

    return True, request_file


def save_file(request_file, base_path):
    # save the dataset in DATASET_PATH
    filepath = os.path.join(base_path, request_file.filename)

    # Check if a file exists at filepath
    if os.path.isfile(filepath):
        return False, json_return(400, "file with this name already exists")
    request_file.save(filepath)

    return True, filepath
