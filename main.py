import ccxt
import time
from exchangeClass import Coinex,BingX

symbol = 'BTC/USDT'
saf_number = 1
create_order = False  # set True to create just one order in saf_number_price
order_info = 'buy kucoin'  # or 'buy' and after a white space 'coinEx' or 'hitBTC' or 'kucoin' or 'bingX'
amount_of_order = 0.00001
time_delay = 1 # second

# CoinEx -----------------------------
coinex_obj = Coinex(
    'FE24639298B04CAD9B59DCB47DC26BC6',
    '9CCED9FB5B897A7161C0025E4FBF0272EB85C6CDD3C19C05')

# Kucoin -----------------------------
kucoin_obj = ccxt.kucoin({
    'password': '16181920',
    'apiKey': '64c7a00253f38d000101038f',
    'secret': '666f9c5d-be0a-4cfa-94ae-50eceffaf5f5',
})
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

while True:
    # coinEx
    coinex_orderbook = coinex_obj.fetch_order_book(symbol)
    bids_coinex = coinex_orderbook['bids'][saf_number - 1]
    asks_coinex = coinex_orderbook['asks'][saf_number - 1]
    # kucoin
    kucoin_orderbook = kucoin_obj.fetch_order_book(symbol)
    bids_kucoin = kucoin_orderbook['bids'][saf_number - 1]
    asks_kucoin = kucoin_orderbook['asks'][saf_number - 1]
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
        {'sarafi': 'Kucoin', 'PrSell': asks_kucoin[0], 'PrBuy': bids_kucoin[0], 'HajmSell': asks_kucoin[1],
         'HajmBuy': bids_kucoin[1]},
        {'sarafi': 'hitBTC', 'PrSell': asks_hitBTC[0], 'PrBuy': bids_hitBTC[0], 'HajmSell': asks_hitBTC[1],
         'HajmBuy': bids_hitBTC[1]},
        {'sarafi': 'bingX', 'PrSell': asks_bingx[0], 'PrBuy': asks_bingx[0], 'HajmSell': asks_bingx[1],
         'HajmBuy': asks_bingx[1]}
    ]
    print('\n----------bids asks list----------\n',bids_asks_list)

    # balance of wallet -------------
    balance_info = f'''
$$$$$$$$$ balance info $$$$$$$$$
BingX balance: {bingX_obj.fetch_balance()}
CoinEx balance: {coinex_obj.fetch_balance()}
Kucoin balance: {kucoin_obj.fetch_balance()}
HitBTC balance: {hitBTC_obj.fetch_balance()}
    '''
    print(balance_info)

    # create order      -------------
    if create_order:
        order_type, sarafi = order_info.split()
        if sarafi == 'coinEx':
            order = coinex_obj.create_market_order(symbol, order_type, amount_of_order)
        elif sarafi == 'kucoin':
            order = kucoin_obj.create_market_order(symbol, order_type, amount_of_order)
        elif sarafi == 'hitBTC':
            order = hitBTC_obj.create_market_order(symbol, order_type, amount_of_order)
        elif sarafi == 'bingX':
            order = bingX_obj.create_market_order(symbol, order_type, amount_of_order)
        else:
            print(f"code isn't configured for '{sarafi}' to create order")

        create_order = False

    time.sleep(0.5)
