from pydantic import BaseModel


class AuthResult(BaseModel):
    token_type: str
    scope: str
    refresh_token: str
    expires_in: int
    access_token: str


class AuthResponse(BaseModel):
    jsonrpc: str
    result: AuthResult
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool
