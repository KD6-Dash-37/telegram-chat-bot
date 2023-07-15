import logging
import json
import os
# from validators import validate_authentication
from pydantic import ValidationError
from websockets.client import WebSocketClientProtocol
from data_model import AuthResponse, ErrorResponse


log = logging.getLogger(__name__)


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

async def authenticate_websocket(websocket: WebSocketClientProtocol):

    creds = {
            "jsonrpc": "2.0",
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": os.environ.get("SPREAD_ID"),
                "client_secret": os.environ.get("SPREAD_SECRET")
            }
        }

    creds = json.dumps(creds)

    await websocket.send(creds)

    auth_response = await websocket.recv()

    # validate_authentication(auth_response=auth_response)
