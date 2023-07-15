import json
import logging
from websockets.client import WebSocketClientProtocol
from data_model import AccountSummaryResponse, ErrorResponse
from pydantic import ValidationError

log = logging.getLogger(__name__)


async def get_account_summary(websocket: WebSocketClientProtocol, currency: str):

    log.debug(f"requesting {currency} account summary")

    msg = {
        "jsonrpc" : "2.0",
        "method": "private/get_account_summary",
        "params": {
            "currency": currency
        }
    }

    msg = json.dumps(msg)

    await websocket.send(msg)

    response = await websocket.recv()

    response = json.loads(response)

    try:

        response = AccountSummaryResponse.model_validate(response)

    except ValidationError:

        try:

            error_response = ErrorResponse.model_validate(response)

            error = error_response.error

            log.critical((
                f"failed to parse and validate get_account_summary response for {currency} "
                f"{error.message} : {error.code}"
            ))

            log.exception("validation error", exc_info=True, stack_info=True)

        except ValidationError as ex:

            log.exception(
                "unknown api response received for get_account_summary",
                exc_info=True,
                stack_info=True
            )

            raise ex
