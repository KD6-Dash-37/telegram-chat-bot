import json
import logging
from pydantic import ValidationError
from websockets.client import WebSocketClientProtocol
from data_model import GetPositionsResponse, ErrorResponse, Position


log = logging.getLogger("delta-hedger")


async def get_positions(websocket: WebSocketClientProtocol, currency: str):

    log.debug(f"requesting all {currency} positions")

    msg = {
        "jsonrpc" : "2.0",
        "method" : "private/get_positions",
        "params" : {
            "currency" : currency,
            }
        }

    msg = json.dumps(msg)

    await websocket.send(msg)

    response = await websocket.recv()

    response = json.loads(response)

    try:

        response = GetPositionsResponse.model_validate(response)

        log.debug(f"successfully parsed and validated {currency} positions")

        return response

    except ValidationError:

        try:

            error_response = ErrorResponse.model_validate(response)

            error = error_response.error

            log.critical((
                f"failed to parse and validate get_positions response for {currency} "
                f"{error.message} : {error.code}"
            ))

            log.exception("validation error", exc_info=True, stack_info=True)

        except ValidationError as ex:

            log.exception(
                "unknown api response received for get_positions",
                exc_info=True,
                stack_info=True
            )

            raise ex
