# summary.py
import os

import websockets
from dotenv import load_dotenv
import emoji

from api_methods import authenticate_websocket, get_account_summary, get_positions
from data_model import AccountSummaryResponse, GetPositionsResponse, BotConfig


load_dotenv()


async def account_summary(cfg: BotConfig) -> str:

    currency = cfg.message_type.currency

    account_summary_response, position_response = await get_account_data(currency=currency, cfg=cfg)

    account_msg = construct_account_message(
        account_summary_response=account_summary_response
    )

    position_msg = construct_position_message(
        position_response=position_response,
        currency=currency
    )

    msg = account_msg + "\n" + position_msg

    return msg


async def get_account_data(
        currency: str, cfg: BotConfig
) -> tuple[AccountSummaryResponse, GetPositionsResponse]:
    
    async with websockets.connect(os.environ.get("ENDPOINT")) as websocket:

        await authenticate_websocket(websocket=websocket, cfg=cfg)

        account_data = await get_account_summary(
            websocket=websocket,
            currency=currency
        )

        position_data = await get_positions(
            websocket=websocket,
            currency=currency
        )

        return account_data, position_data


def margin_ratio(margin, equity) -> str:

    try:

        ratio = (margin / equity) * 100

        ratio = round(ratio, 2)

        return f"{ratio}%"

    except ZeroDivisionError:

        return ""


def construct_account_message(account_summary_response: AccountSummaryResponse) -> str:

    account_data = account_summary_response.result

    bank_emoji = emoji.emojize(":bank:")

    initial_margin = round(account_data.initial_margin, 4)

    intitial_margin_ratio = margin_ratio(
        margin=account_data.initial_margin,
        equity=account_data.equity
    )

    maintenance_margin = round(account_data.initial_margin, 4)

    maintenance_margin_ratio = margin_ratio(
        margin=account_data.maintenance_margin,
        equity=account_data.equity
    )

    margin_balance = round(account_data.margin_balance, 4)

    title = f"{bank_emoji} Account Summary ({account_data.currency}):"

    im = f"\nInitial margin: {initial_margin} {intitial_margin_ratio}"

    mm = f"\nMaintenance margin: {maintenance_margin} {maintenance_margin_ratio}"

    balance = f"\nMargin balance: {margin_balance}"

    delta_total = f"\n Net delta: {account_data.delta_total}"

    msg = title + im + mm + balance + delta_total

    return msg


def construct_position_message(
        position_response: GetPositionsResponse, currency: str
) -> str:

    positions = position_response.result

    suit_case_emoji = emoji.emojize(":briefcase:")

    msg = f"{suit_case_emoji} {currency} Positions: "

    if len(positions) > 0:

        for position in positions:

            position_msg = (
                f"\n{position.instrument_name} {position.size} @ {position.average_price}"
            )

            msg += position_msg

        return msg

    msg += "\nNo active positions"

    return msg
