from typing import Callable, Dict

import requests

from ..commons.error_handling import handle_status_code


@handle_status_code
def request_token(token_endpoint, username, password):
    """ Request invoice extractor token """
    response = requests.post(
        url=token_endpoint,
        data={
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": "extractionapi",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response.raise_for_status()
    return response.json()["access_token"]


@handle_status_code
def extract_invoice(
    file,
    extractor_endpoint,
    content_type,
    get_token: Callable[[], str] = None,
    params: Dict = {},
    timeout: int = 1800,
):
    """ Request invoice extractor """
    params.setdefault("ingnoreNull", "false")
    response = requests.post(
        url=extractor_endpoint,
        data=file,
        params=params,
        timeout=timeout,
        headers={
            "Content-type": content_type,
            "Authorization": f"Bearer {get_token()}",
        },
    )

    response.raise_for_status()
    return response.json()
