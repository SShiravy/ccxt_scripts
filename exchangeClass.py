import hmac
import requests
import hashlib
import time


class Coinex:
    def __init__(self, access_id, secret_key):
        self.access_id = access_id
        self.__secret_key = secret_key
        self.base_url = "https://api.coinex.com/v1"
        self.headers = {
            'Content-Type': "application/json",
            'authorization': ''
        }

    def __create_signature(self, params):
        sign_str = '&'.join(f'{k}={params.get(k)}' for k in sorted(params)) \
                   + f'&secret_key={self.__secret_key}'
        signature = hashlib.md5(sign_str.encode()).hexdigest().upper()
        return signature

    def fetch_order_book(self, symbol):
        endpoint = '/market/depth'
        params = {'market': symbol.replace('/', ''), 'merge': 1}
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()['data']

    def fetch_balance(self):
        endpoint = '/balance/info'
        params = {'access_id': self.access_id, 'tonce': int(time.time() * 1000)}
        self.headers['authorization'] = self.__create_signature(params)
        response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()['data']

    def create_market_order(self, symbol, order_type, amount_of_order):
        endpoint = '/order/market'
        params = {'access_id': self.access_id,
                  'tonce': int(time.time() * 1000),
                  "amount": amount_of_order,
                  "market": symbol.replace('/', ''),
                  "type": order_type,
                  }

        self.headers['authorization'] = self.__create_signature(params)
        response = requests.post(self.base_url + endpoint, json=params, headers=self.headers)
        return response.json()

    # TODO: add other methods like create_limit order



class BingX:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.__api_secret = api_secret
        self.base_url = "https://open-api.bingx.com"
        self.headers = {
            'X-BX-APIKEY': self.api_key,
        }

    def __add_signature(self, params):
        sign_str = '&'.join(f'{k}={params.get(k)}' for k in sorted(params))
        sign = hmac.new(self.__api_secret.encode(), sign_str.encode(), 'sha256').hexdigest()
        params['signature'] = sign
        return sign,sign_str

    def fetch_order_book(self, symbol):
        endpoint = '/openApi/spot/v1/market/depth'
        params = {'symbol': symbol.replace('/', '-'), 'limit': 1}
        self.__add_signature(params)
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()['data']

    def fetch_balance(self):
        endpoint = '/openApi/contract/v1/balance'
        params = {'timestamp': round(time.time() * 1000)}
        self.__add_signature(params)
        response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()

    def create_market_order(self, symbol, order_type, amount_of_order):
        endpoint = '/openApi/spot/v1/trade/order'
        params = {
            'symbol': symbol.replace('/','-'),
            'side': order_type.upper(),
            'type': 'MARKET',
            'quantity': amount_of_order,
            'quoteOrderQty': amount_of_order,
            'timestamp': round(time.time() * 1000)
        }
        sign,params_str = self.__add_signature(params)
        response = requests.post(self.base_url + endpoint + f'?{params_str}&signature={sign}', headers=self.headers)
        # response = requests.post(self.base_url+endpoint, json=params ,headers=self.headers,)
        return response.json()


# ------------------------------------------------------------------------------
#
bingx_obj = BingX(api_key='DxseTlg1n5dXh10PvDlBCQuel8KGRPgaN4LpuTphTaarLYRwWVJuAO9wl5szpXNUI5jHbstBcyaB4Niw',
             api_secret='CpUoGgyNFkMheijHHyQp45wWcjYoT1eBZx37hEefdfUULLaGQt4GyqkWpCyPd242FxVEM2Pjm0N6c4xlauyYA')

print(bingx_obj.fetch_balance())
print(bingx_obj.create_market_order('BTC/USDT','sell',0.1))


# while True:
#     bingX_orderbook = bingx_obj.fetch_order_book('BTC/USDT')
#     bids_bingx = bingX_orderbook['bids'][0]
#     asks_bingx = bingX_orderbook['asks'][0]
#     # print(bids_bingx,'\n\n',asks_bingx,'\n------------------------\n')
#     print({'PrBuy': asks_bingx[0], 'PrSell': bids_bingx[0], 'HajmBuy': asks_bingx[1],
#            'HajmSell': bids_bingx[1]}, )
#     # time.sleep(0.5)
# # -----------------------------------------------------------------------------
#
#
# coinex_obj = Coinex(
#     'FE24639298B04CAD9B59DCB47DC26BC6',
#     '9CCED9FB5B897A7161C0025E4FBF0272EB85C6CDD3C19C05')
# while True:
#     coinex_orderbook = coinex_obj.fetch_order_book('BTCUSDT')
#     bids_coinex = coinex_orderbook['bids'][0]
#     asks_coinex = coinex_orderbook['asks'][0]
#     print({'PrBuy': asks_coinex[0], 'PrSell': bids_coinex[0], 'HajmBuy': asks_coinex[1],
#            'HajmSell': bids_coinex[1]}, )
#     time.sleep(0.5)
