from pydantic import BaseModel


class Error(BaseModel):
    message: str
    code: int


class ErrorResponse(BaseModel):
    jsonrpc: str
    error: Error
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool
