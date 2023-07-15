from data_model import GetPositionsResponse
from pydantic import ValidationError
r = {
    'jsonrpc': '2.0', 
    'result': [
        {'total_profit_loss': -0.045641171, 'size_currency': 1.770329437, 'size': 53680.0, 'settlement_price': 30333.93, 'realized_profit_loss': 0.0, 'realized_funding': 0.0, 'open_orders_margin': 0.0, 'mark_price': 30322.04, 'maintenance_margin': 0.017859998, 'leverage': 50, 'kind': 'future', 'interest_value': 0.0, 'instrument_name': 'BTC-PERPETUAL', 'initial_margin': 0.035563291, 'index_price': 30320.3, 'floating_profit_loss': -0.000693917, 'estimated_liquidation_price': None, 'direction': 'buy', 'delta': 1.770329437, 'average_price': 31124.47}, {'total_profit_loss': 0.027708943, 'size_currency': -1.000484954, 'size': -30430.0, 'settlement_price': 30437.24, 'realized_profit_loss': 0.0, 'open_orders_margin': 0.0, 'mark_price': 30415.25, 'maintenance_margin': 0.010054898, 'leverage': 50, 'kind': 'future', 'instrument_name': 'BTC-28JUL23', 'initial_margin': 0.020059747, 'index_price': 30320.3, 'floating_profit_loss': 0.000722821, 'estimated_liquidation_price': None, 'direction': 'sell', 'delta': -1.000484954, 'average_price': 31281.61}, {'total_profit_loss': 0.019458387, 'size_currency': -0.755599971, 'size': -23250.0, 'settlement_price': 30782.06, 'realized_profit_loss': 0.0, 'open_orders_margin': 0.0, 'mark_price': 30770.25, 'maintenance_margin': 0.007584546, 'leverage': 50, 'kind': 'future', 'instrument_name': 'BTC-29SEP23', 'initial_margin': 0.015140546, 'index_price': 30320.3, 'floating_profit_loss': 0.000289898, 'estimated_liquidation_price': None, 'direction': 'sell', 'delta': -0.755599971, 'average_price': 31583.6}], 'usIn': 1689454568790526, 'usOut': 1689454568791009, 'usDiff': 483, 'testnet': False}

try:
    
    GetPositionsResponse.model_validate(r)

except ValidationError as ex:

    print(repr(ex))