from typing import Any
from fastapi import status


def success_response(status_code=status.HTTP_200_OK, detail: str = '', data: Any = []):
    """
    For the success response
    :param status_code: status code
    :param detail: message
    :param data: data
    :return: response
    """
    response = {"status_code": status_code,
                "detail": detail,
                'data': data}
    return response
