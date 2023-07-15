from pydantic import BaseModel


class ChatConfig(BaseModel):

    chat_id: str
    message_thread_id: str


class AuthConfig(BaseModel):
    token: str
    users: list[int]


class BotConfig(BaseModel):
    name: str
    auth: AuthConfig
    chat: ChatConfig
