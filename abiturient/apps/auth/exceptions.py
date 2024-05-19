from fastapi import HTTPException


class BaseApplicationException(HTTPException):
    detail = ('application error')
    status_code = 400

    def __init__(self, detail: str = detail):
        self.detail = detail


class UserAlreadyExists(BaseApplicationException):
    detail = ('User already exists')

    def __init__(self, detail: str = detail):
        super().__init__(detail=detail)
