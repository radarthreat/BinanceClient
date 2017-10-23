import requests
import json
import time
import hmac
import hashlib
from urllib.parse import urlencode


class BinanceClient(object):

    def __init__(self, api_key, api_secret, recv_window=5000):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://binance.com/"
        self.recv_window = recv_window

    @staticmethod
    def sign_transaction(secret, request_body):
        signature = hmac.new(secret, request_body, digestmod=hashlib.sha256)
        return signature.hexdigest()

    def test_connection(self):
        """
        Tests connection to Binance server
        :return: <bool> Connection status ok
        """
        r = requests.get(self.api_url+'api/v1/ping')
        if r.status_code == 200:
            return True
        else:
            return False

    def all_prices(self):
        """
        Gets all prices for all tickers
        :return: <list> list of dictionaries of tickers and latest prices
        """
        r = requests.get(self.api_url + 'api/v1/ticker/allPrices')
        all_prices = json.loads(r.content)
        return all_prices

    def latest_price(self, symbol):
        """
        Get the latest reported price for a symbol
        :param symbol: <str> Instrument for which price is desired
        :return: <dict> dict of symbol and price
        """
        all_prices = self.all_prices()
        for d in all_prices:
            if d.get('symbol') == symbol:
                return d

    def order(self, symbol, side, trade_type, quantity, price, new_client_order_id=None, stop_price=None, iceberg_qty=None):
        """
        Place buy or sell order for symbol

        :param symbol: <str> Base asset to trade
        :param side: <str> Side of trade (BUY or SELL)
        :param trade_type: <str> LIMIT or MARKET
        :param quantity: <float> quantity to buy or sell
        :param price: <float> Price
        :param new_client_order_id: <str> A unique id for the order. Automatically generated if not sent.
        :param stop_price: <float> Used with stop orders
        :param iceberg_qty: <float> Used with iceberg orders
        :return: JSON response
        """
        headers = {"X-MBX-APIKEY": self.api_key}
        payload = {"symbol": symbol,
                   "side": side,
                   "type": trade_type,
                   "quantity": quantity,
                   "price": price,
                   "newClientOrderId": new_client_order_id,
                   "stopPrice": stop_price,
                   "icebergQty": iceberg_qty,
                   "timestamp": int(time.time() * 1000)}

        request = requests.Request('POST',
                                   self.api_url+'api/v3/order',
                                   params=payload,
                                   headers=headers)

        prepared_request = request.prepare()
        query_string = prepared_request.url.split('?')[1].encode()
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(prepared_request)

        return response.content

    def order_status(self, symbol, order_id=None, orig_client_order_id=None):
        """
        Get status of order

        :param symbol: <str> Base asset to trade
        :param order_id: <int> Order ID
        :param orig_client_order_id: <str> Use if order_id not given
        :return: JSON response
        """
        headers = {"X-MBX-APIKEY": self.api_key}
        payload = {"symbol": symbol,
                   "orderId": order_id,
                   "origClientOrderId": orig_client_order_id,
                   "recvWindow": self.recv_window,
                   "timestamp": int(time.time() * 1000)}

        request = requests.Request('POST',
                                   self.api_url+'api/v3/order',
                                   params=payload,
                                   headers=headers)

        prepared_request = request.prepare()
        query_string = prepared_request.url.split('?')[1]
        signature = self.sign_transaction(self.api_secret.encode(), query_string.encode())
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(prepared_request)

        return response

    def cancel_order(self, symbol, order_id=None, orig_client_order_id=None):
        """
        Cancel an open order

        :param symbol: <str> Base asset to trade
        :param order_id: <int> Order ID to cancel
        :param orig_client_order_id: <str> Use if order_id not given
        :return: JSON response
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key}
        payload = {"symbol": symbol,
                   "orderId": order_id,
                   "origClientOrderId": orig_client_order_id,
                   "recvWindow": self.recv_window,
                   "timestamp": int(time.time() * 1000)}

        request = requests.Request('DELETE',
                                   self.api_url + 'api/v3/order',
                                   params=payload,
                                   headers=headers)

        query_string = urlencode(payload, doseq=True)
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(request)

        return response

    def open_orders(self, symbol):
        """
        Get list of open orders for the given symbol

        :param symbol: <str> Asset name
        :return: JSON response
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key
                   }
        payload = {"symbol": symbol,
                   "timestamp": int(time.time() * 1000)
                   }

        request = requests.Request('GET',
                                   self.api_url+'api/v3/openOrders',
                                   params=payload,
                                   headers=headers)

        prepared_request = request.prepare()
        query_string = prepared_request.url.split('?')[1].encode()
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(prepared_request)

        return response

    def current_positions(self):
        """
        Get current positions for user account
        :return:
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key}
        payload = {"timestamp": int(time.time() * 1000)}

        request = requests.Request('GET',
                                   self.api_url + 'api/v3/account',
                                   params=payload,
                                   headers=headers)

        prepared_request = request.prepare()
        query_string = prepared_request.url.split('?')[1].encode()
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(prepared_request)

        return response

    def withdraw_history(self, asset=None, status=None, start_time=None, end_time=None):
        """
        Get withdrawal history for account

        :param asset: <str>
        :param status: <int> (0:Email Sent,1:Cancelled 2:Awaiting Approval 3:Rejected 4:Processing 5:Failure 6Completed)
        :param start_time: <int>
        :param end_time: <int>
        :return: JSON response
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key}
        payload = {"asset": asset,
                   "status": status,
                   "startTime": start_time,
                   "endTime": end_time,
                   "recvWindow": self.recv_window,
                   "timestamp": int(time.time() * 1000)
                   }

        request = requests.Request('POST',
                                   self.api_url + 'wapi/v1/getWithdrawHistory.html',
                                   params=payload,
                                   headers=headers
                                   )

        query_string = urlencode(payload, doseq=True)
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(request)

        return response

    def deposit_history(self, asset=None, status=None, start_time=None, end_time=None):
        """
        Get deposit history for account

        :param asset: <str>
        :param status: <int> (0:pending,1:success)
        :param start_time: <int>
        :param end_time: <int>
        :return: JSON response
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key}
        payload = {"asset": asset,
                   "status": status,
                   "startTime": start_time,
                   "endTime": end_time,
                   "recvWindow": self.recv_window,
                   "timestamp": int(time.time() * 1000)
                   }

        request = requests.Request('POST',
                                   self.api_url + 'wapi/v1/getDepositHistory.html',
                                   params=payload,
                                   headers=headers
                                   )

        query_string = urlencode(payload, doseq=True)
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(request)

        return response

    def withdraw(self, asset, address, amount, name=None):
        """
        Withdraw funds from account

        :param asset: <str>
        :param address: <str>
        :param amount: <float>
        :param name:
        :return: JSON response
        {
            "msg": "success",
            "success": true
        }
        """
        headers = {"content-type": "application/x-www-form-urlencoded",
                   "X-MBX-APIKEY": self.api_key}
        payload = {"asset": asset,
                   "address": address,
                   "amount": amount,
                   "name": name,
                   "recvWindow": self.recv_window,
                   "timestamp": int(time.time() * 1000)
                   }

        request = requests.Request('POST',
                                   self.api_url + 'wapi/v1/withdraw.html',
                                   params=payload,
                                   headers=headers
                                   )

        query_string = urlencode(payload, doseq=True)
        signature = self.sign_transaction(self.api_secret, query_string)
        request.params['signature'] = signature
        with requests.Session() as session:
            response = session.send(request)

        return response
