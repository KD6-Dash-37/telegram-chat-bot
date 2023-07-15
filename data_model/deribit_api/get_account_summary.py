# get_account_summary
# https://docs.deribit.com/#private-get_account_summary
from pydantic import BaseModel


class AccountSummaryResult(BaseModel):
    available_funds: float
    available_withdrawal_funds: float
    balance: float
    currency: str
    delta_total_map: dict
    delta_total: float
    equity: float
    fee_balance: float
    futures_pl: float
    futures_session_rpl: float
    futures_session_upl: float
    initial_margin: float
    limits: dict
    maintenance_margin: float
    margin_balance: float
    options_delta: float
    options_gamma: float
    options_pl: float
    options_session_rpl: float
    options_session_upl: float
    options_theta: float
    options_value: float
    options_vega: float
    portfolio_margining_enabled: bool
    projected_delta_total: float
    projected_initial_margin: float
    projected_maintenance_margin: float
    session_rpl:float
    session_upl: float
    spot_reserve: float
    total_pl: float

class AccountSummaryResponse(BaseModel):

    jsonrpc: str
    result: AccountSummaryResult
    usIn: int
    usOut: int
    usDiff: int
    testnet: bool
