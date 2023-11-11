import ccxt
import time
from datetime import datetime
from exchangeClass import Coinex, BingX

license_expire_date = 20240101
# Get the current date
current_date = datetime.now()
# Format the date as "YYYYMMDD"
formatted_current_date = current_date.strftime("%Y%m%d")
print(f'now {formatted_current_date} and license expire date {license_expire_date}')

symbol = 'TRX/USDT'
saf_number = 1
create_order = False  # set True to create just one order in saf_number_price
order_info = 'buy coinEx'  # or 'buy' and after a white space 'coinEx' or 'hitBTC' or 'kucoin' or 'bingX'
amount_of_order = 5
time_delay = 1  # second

# CoinEx -----------------------------
coinex_obj = Coinex(
    '3F16972A5CA348C9919B80D61E87BA9E',
    '73BF7AEA580473B535BCD28A767D358A589440FCDC3E6F32')

# HitBTC -----------------------------
hitBTC_obj = ccxt.hitbtc({
    'apiKey': 'VGnIjD1SEf_V1UiJynHHRrAdoIatW30w',
    'secret': 'eqYhk3J4jz7MlFuwWTNpoVzwi6W1SdgP'
})
# BingX -----------------------------
bingX_obj = BingX(
    'DxseTlg1n5dXh10PvDlBCQuel8KGRPgaN4LpuTphTaarLYRwWVJuAO9wl5szpXNUI5jHbstBcyaB4Niw',
    'CpUoGgyNFkMheijHHyQp45wWcjYoT1eBZx37hEefdfUULLaGQt4GyqkWpCyPd242FxVEM2Pjm0N6c4xlauyYA'
)

last_trade_dict = {'BingX': {}, 'hitBTC': {}, 'Coinex': {}}
try:
    hitBTC_last_trade = hitBTC_obj.fetch_closed_orders(symbol=symbol)[-1]

    hitBTC_last_trade_cost = float(hitBTC_last_trade['price']) * float(hitBTC_last_trade['info']['quantity'])
    last_trade_dict['hitBTC'] = {'symbol': hitBTC_last_trade['symbol'],
                                 'order_type': hitBTC_last_trade['side'],
                                 'money': hitBTC_last_trade_cost,
                                 'amount_of_order': hitBTC_last_trade['info']['quantity'],
                                 'money_fee': hitBTC_last_trade['cost'] - hitBTC_last_trade_cost
                                 }
except:
    pass
try:
    coinex_last_trade = coinex_obj.trade_history(symbol)['data'][0]
    last_trade_dict['Coinex'] = {'symbol': coinex_last_trade['market'],
                                 'order_type': coinex_last_trade['type'],
                                 'money': coinex_last_trade['deal_money'],
                                 'amount_of_order': coinex_last_trade['amount'],
                                 'money_fee': coinex_last_trade['money_fee']
                                 }
except:
    pass
try:
    bingX_last_trade = bingX_obj.trade_history(symbol)[0]
    last_trade_dict['BingX'] = {'symbol': bingX_last_trade['symbol'],
                                'order_type': bingX_last_trade['side'],
                                'money': bingX_last_trade['cummulativeQuoteQty'],
                                'amount_of_order': bingX_last_trade['executedQty'],
                                'money_fee': bingX_last_trade['fee']
                                }
except:
    pass

print(last_trade_dict)

while True:
    # coinEx
    coinex_orderbook = coinex_obj.fetch_order_book(symbol)
    bids_coinex = coinex_orderbook['bids'][saf_number - 1]
    asks_coinex = coinex_orderbook['asks'][saf_number - 1]
    # hitBTC
    hitBTC_orderbook = hitBTC_obj.fetch_order_book(symbol)
    bids_hitBTC = hitBTC_orderbook['bids'][saf_number - 1]
    asks_hitBTC = hitBTC_orderbook['asks'][saf_number - 1]
    # bingX
    bingX_orderbook = bingX_obj.fetch_order_book(symbol)
    bids_bingx = bingX_orderbook['bids'][saf_number - 1]
    asks_bingx = bingX_orderbook['asks'][saf_number - 1]

    bids_asks_list = [
        {'sarafi': 'CoinEx', 'PrBuy': asks_coinex[0], 'PrSell': bids_coinex[0], 'HajmBuy': asks_coinex[1],
         'HajmSell': bids_coinex[1]},
        {'sarafi': 'hitBTC', 'PrSell': asks_hitBTC[0], 'PrBuy': bids_hitBTC[0], 'HajmSell': asks_hitBTC[1],
         'HajmBuy': bids_hitBTC[1]},
        {'sarafi': 'bingX', 'PrSell': asks_bingx[0], 'PrBuy': asks_bingx[0], 'HajmSell': asks_bingx[1],
         'HajmBuy': asks_bingx[1]}
    ]
    print('\n----------bids asks list----------\n', bids_asks_list)

    # balance of wallet -------------
    balance_info = f'''
$$$$$$$$$ balance info $$$$$$$$$
BingX balance: {bingX_obj.fetch_balance()}
CoinEx balance: {coinex_obj.fetch_balance()}
HitBTC balance: {hitBTC_obj.fetch_balance()}
    '''
    print(balance_info)

    # create order      -------------
    if create_order:
        order = ''
        order_type, sarafi = order_info.split()
        if sarafi == 'coinEx':
            order = coinex_obj.create_market_order(symbol, order_type, amount_of_order)
        elif sarafi == 'hitBTC':
            order = hitBTC_obj.create_market_order(symbol, order_type, amount_of_order)
        elif sarafi == 'bingX':
            order = bingX_obj.create_market_order(symbol, order_type, amount_of_order)
        else:
            print(f"code isn't configured for '{sarafi}' to create order")

        create_order = False
        print('-------///////',order,'///////----------')

    time.sleep(0.5)
