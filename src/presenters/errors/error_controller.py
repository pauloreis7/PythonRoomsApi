from typing import Type, Dict

from src.errors.http_request_error import HttpRequestError


def handle_errors(error: Type[Exception]) -> Dict:
    """
    Handle Exception cases
    @param: error - Exception
    @returns: Dict with data and status_code
    """

    if isinstance(error, HttpRequestError):
        return {
            "status_code": error.status_code,
            "data": {"error": error.detail},
        }

    return {"status_code": 500, "data": {"error": str(error)}}
