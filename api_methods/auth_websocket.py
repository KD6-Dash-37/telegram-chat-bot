import logging
import json
import os
from pydantic import ValidationError
from websockets.client import WebSocketClientProtocol
from data_model import AuthResponse, ErrorResponse, BotConfig


log = logging.getLogger(__name__)


async def authenticate_websocket(websocket: WebSocketClientProtocol, cfg: BotConfig):

    client_id, client_secret = id_secret_var_names(cfg=cfg)

    creds = {
            "jsonrpc": "2.0",
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": os.environ.get(client_id),
                "client_secret": os.environ.get(client_secret)
            }
        }

    creds = json.dumps(creds)

    await websocket.send(creds)

    auth_response = await websocket.recv()

    validate_authentication(auth_response=auth_response)


def id_secret_var_names(cfg: BotConfig) -> tuple[str]:

    account_name = cfg.auth.deribit.account_name

    account_name = account_name.upper()

    client_id = "_".join([account_name, "ID"])

    client_secret = "_".join([account_name, "SECRET"])

    return client_id, client_secret


def validate_authentication(auth_response: str):

    auth_response = json.loads(auth_response)

    try:

        auth_response = AuthResponse.model_validate(auth_response)

        log.info((
            "succesfully authenticated websocket connection"
        ))

    except ValidationError:

        try:

            error_response = ErrorResponse.model_validate(auth_response)

            error = error_response.error

            log.critical((
                f"authentication failed: {error.message} "
                f"exchange error code: {error.code}"
            ))

        except ValidationError as ex:

            log.exception(
                "unknown api response received from", 
                exc_info=ex,
            )
