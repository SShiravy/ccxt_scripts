import hmac
import requests
import hashlib
import time
from datetime import datetime, timedelta


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
        params = {'market': symbol.replace('/', ''), 'merge': 0}
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

    def account_info(self):
        endpoint = '/balance/info'
        params = {'access_id': self.access_id, 'tonce': int(time.time() * 1000)}
        self.headers['authorization'] = self.__create_signature(params)
        response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()['data']

    def trade_history(self,symbol):
        endpoint = '/order/finished'
        start_time = int((datetime.now() - timedelta(days=364)).timestamp())
        end_time = int(time.time())
        params = {'access_id': self.access_id, 'tonce': int(time.time() * 1000),
                  'start_time': start_time, 'end_time': end_time, 'page': 1, 'limit': 5, 'market':symbol.replace('/', '')}
        self.headers['authorization'] = self.__create_signature(params)
        response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()['data']


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
        return sign, sign_str

    def fetch_order_book(self, symbol):
        endpoint = '/openApi/spot/v1/market/depth'
        params = {'symbol': symbol.replace('/', '-'), 'limit': 1}
        self.__add_signature(params)
        response = requests.get(self.base_url + endpoint, params=params)
        return response.json()['data']

    def fetch_balance(self):
        endpoint = '/openApi/spot/v1/account/balance'
        params = {'timestamp': round(time.time() * 1000)}
        self.__add_signature(params)
        response = requests.get(self.base_url + endpoint, params=params, headers=self.headers)
        return response.json()

    def create_market_order(self, symbol, order_type, amount_of_order):
        endpoint = '/openApi/spot/v1/trade/order'
        params = {
            'symbol': symbol.replace('/', '-'),
            'side': order_type.upper(),
            'type': 'MARKET',
            'quantity': amount_of_order,
            'quoteOrderQty': amount_of_order,
            'timestamp': round(time.time() * 1000)
        }
        sign, params_str = self.__add_signature(params)
        response = requests.post(self.base_url + endpoint + f'?{params_str}&signature={sign}', headers=self.headers)
        # response = requests.post(self.base_url+endpoint, json=params ,headers=self.headers,)
        return response.json()['data']

    def trade_history(self,symbol):
        endpoint = '/openApi/spot/v1/trade/historyOrders'
        params = {'symbol': symbol.replace('/', '-'),
                  'pageIndex': 1,'pageSize':5,
                  'timestamp': round(time.time() * 1000)}
        sign, params_str = self.__add_signature(params)
        response = requests.get(self.base_url + endpoint + f'?{params_str}&signature={sign}', headers=self.headers)
        return response.json()['data']['orders']
