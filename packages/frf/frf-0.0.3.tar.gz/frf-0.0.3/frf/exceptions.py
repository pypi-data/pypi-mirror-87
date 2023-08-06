"""Declares exceptions used by the FastAPI RESt Framework."""
from fastapi import HTTPException


class MethodNotAllowed(HTTPException):
    """Raises to indicate that an unsupported HTTP method is requested."""
    status_code = 415
    default_detail = 'Method "{method}" not allowed.'
    default_code = 'method_not_allowed'

    def __init__(self, method, detail=None, code=None):
        if detail is None:
            detail = self.default_detail.format(method=method)
        super().__init__(status_code=self.status_code, detail=detail)
