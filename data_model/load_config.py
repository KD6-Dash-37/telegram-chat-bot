from pydantic import BaseModel


class ChatConfig(BaseModel):

    chat_id: str
    message_thread_id: str

class TelegramAuth(BaseModel):

    token: str
    users: list[int]


class DeribitAuth(BaseModel):

    account_name: str

class AuthConfig(BaseModel):

    telegram: TelegramAuth
    deribit: DeribitAuth


class MessageType(BaseModel):

    name: str
    currency: str


class BotConfig(BaseModel):
    
    name: str
    auth: AuthConfig
    chat: ChatConfig
    message_type: MessageType
