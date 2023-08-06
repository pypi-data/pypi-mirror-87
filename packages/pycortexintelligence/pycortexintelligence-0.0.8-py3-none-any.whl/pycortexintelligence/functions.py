import requests

LOADMANAGER = "https://api.cortex-intelligence.com"


def _get_sid_bearer_token(auth_endpoint, credentials):
    """
    :param auth_endpoint:
    :param credentials:
    :return:
    """
    response = requests.post(auth_endpoint, json=credentials)
    response_json = response.json()
    return {"Authorization": "Bearer " + response_json["key"]}


def _get_data_input(content, loadmanager, headers):
    """
    :param content:
    :param loadmanager:
    :param headers:
    :return:
    """
    endpoint = loadmanager + "/datainput"
    response = requests.post(endpoint, headers=headers, json=content)
    data_input_id = response.json()["id"]
    return data_input_id


def _get_execution_id(data_input_id, content, loadmanager, headers):
    """
    :param data_input_id:
    :param content:
    :param loadmanager:
    :param headers:
    :return:
    """
    endpoint = "{}/datainput/{}/execution".format(loadmanager, data_input_id)
    response = requests.post(endpoint, headers=headers, json=content)
    execution_id = response.json()["executionId"]
    return execution_id


def _start_process(execution_id, loadmanager, headers):
    """
    :param execution_id:
    :param loadmanager:
    :param headers:
    :return:
    """
    endpoint = loadmanager + "/execution/" + execution_id + "/start"
    response = requests.put(endpoint, headers=headers)
    return response


def _execution_history(execution_id, loadmanager, headers):
    """
    :param execution_id:
    :param loadmanager:
    :param headers:
    :return:
    """
    endpoint = loadmanager + "/execution/" + execution_id  # + '/history'
    response = requests.get(endpoint, headers=headers)
    return response


def upload_local_2_cube(cubo_id, file_path, auth_endpoint, credentials,
                        loadmanager="https://api.cortex-intelligence.com",
                        data_format={
                            "charset": "UTF-8",
                            "quote": "\"",
                            "escape": "\/\/",
                            "delimiter": ",",
                            "fileType": "CSV"},
                        ):
    """
    :param cubo_id:
    :param file_path:
    :param auth_endpoint:
    :param credentials:
    :param loadmanager:
    :param data_format:
    :return:
    """

    # ================ Get Bearer Token ===================
    headers = _get_sid_bearer_token(auth_endpoint, credentials)

    # ================ Content ============================
    content = {
        "destinationId": cubo_id,
        "fileProcessingTimeout": 600000,
        "executionTimeout": 1200000,
    }

    # ================ Get Data Input Id ======================
    data_input_id = _get_data_input(content, loadmanager, headers)

    # ================ Get Execution Id =======================
    execution_id = _get_execution_id(data_input_id, content, loadmanager, headers)

    # ================ Send files =============================
    endpoint = loadmanager + "/execution/" + execution_id + "/file"
    response = requests.post(
        endpoint,
        headers=headers,
        data=data_format,
        files={"file": open(file_path, "rb")},
    )

    # ================ Start Data Input Process ===========================
    _start_process(execution_id, loadmanager, headers)

    return execution_id, headers


def upload_to_cortex(**kwargs):
    """
    :param cubo_id:
    :param file_path:
    :param plataform_url:
    :param username:
    :param password:
    :param data_format: data_format={
                            "charset": "UTF-8",
                            "quote": "\"",
                            "escape": "\/\/",
                            "delimiter": ",",
                            "fileType": "CSV"
                            }
    :return:
    """
    # Read Kwargs
    cubo_id = kwargs.get('cubo_id')
    file_path = kwargs.get('file_path')
    plataform_url = kwargs.get('plataform_url')
    username = kwargs.get('username')
    password = kwargs.get('password')
    data_format = kwargs.get('data_format', {"charset": "UTF-8",
                                             "quote": "\"",
                                             "escape": "\/\/",
                                             "delimiter": ",",
                                             "fileType": "CSV"})

    # Verify Kwargs
    if cubo_id and file_path and plataform_url and username and password:
        auth_endpoint = "https://{}/service/integration-authorization-service.login".format(plataform_url)
        credentials = {"login": str(username), "password": str(password)}
        execution_id, headers = upload_local_2_cube(
            cubo_id=cubo_id,
            file_path=file_path,
            auth_endpoint=auth_endpoint,
            credentials=credentials,
            data_format=data_format
        )
        response = _execution_history(execution_id, LOADMANAGER, headers)
        return response
    else:
        raise ValueError('Error validating arguments.')
