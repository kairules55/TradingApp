import requests
import time
import logging
import hmac
import hashlib
from typing import Dict, Tuple
from utils.helpers import format_price_quantity

class BinanceClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://testnet.binance.vision"
        logging.debug('Binance initialized')


    def get_ticker_price(self, symbol: str) -> float:
        """
        Retrieves the current market price for the given symbol on Binance.
        """
        try:
            url = f"{self.base_url}/api/v3/ticker/price"
            params = {"symbol": symbol}
            response = requests.get(url, params=params)
            response.raise_for_status()
            logging.info("Price for binance : %s", response.json())
            return float(response.json()["price"])
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error fetching price from Binance: {e}")

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """
        Places a market order on Binance for the given symbol, side, and quantity.
        """
        try:
            url = f"{self.base_url}/api/v3/order"
            params = {
                "symbol": symbol,
                "side": side.upper(),
                "type": "MARKET",
                "quantity": str(quantity),
                'timestamp': int(time.time() * 1000),
            }
            headers = {
                "X-MBX-APIKEY": self.api_key,
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            params['signature'] = self.generate_binance_signature(params)
            response = requests.post(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error placing order on Binance: {e}")
        
    def generate_binance_signature(self, params):
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        return signature    