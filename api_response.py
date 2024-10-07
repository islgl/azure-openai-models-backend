from typing import Optional, Any

from pydantic import BaseModel


class ApiResponse(BaseModel):
    status: str
    code: int
    message: Optional[str] = None
    data: Optional[Any] = None

    @classmethod
    def success(cls, code: int, data: Optional[Any] = None, message: Optional[str] = None):
        return cls(status="success", code=code, data=data, message=message)

    @classmethod
    def failure(cls, code: int, data: Optional[Any], message: str):
        return cls(status="failure", code=code, message=message, data=data)
