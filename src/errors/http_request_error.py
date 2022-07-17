from fastapi import HTTPException


class HttpRequestError(HTTPException):
    """Http error"""

    def __init__(
        self,
        status_code: int,
        detail: str,
    ) -> None:
        super().__init__(status_code, detail)

        self.status_code = status_code
        self.detail = detail
