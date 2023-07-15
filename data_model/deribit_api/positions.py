from pydantic import BaseModel
from typing import Optional


class Position(BaseModel):

    vega: Optional[float] = None
    total_profit_loss: float
    theta: Optional[float] = None
    size: float
    settlement_price: float
    realized_profit_loss: float
    open_orders_margin:float
    mark_price: float
    maintenance_margin: float
    kind: str
    instrument_name: str
    initial_margin: float
    index_price: float
    gamma: Optional[float] = None
    floating_profit_loss_usd: Optional[float] = None
    floating_profit_loss:float
    direction: str
    delta: float
    average_price_usd: Optional[float] = None
    average_price: float


class GetPositionsResponse(BaseModel):

    jsonrpc: str
    result: list[Position]
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool
