import requests
import logging
from typing import Dict, Tuple
from utils.helpers import format_price_quantity

class BybitClient:
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = "https://api-testnet.bybit.com"
        logging.debug('BybitClient initialized')

    def get_ticker_price(self, symbol: str) -> float:
        """
        Retrieves the current market price for the given symbol on Bybit.
        """
        try:
            url = f"{self.base_url}/spot/v3/public/quote/ticker/24hr"
            params = {"symbol": symbol}
            response = requests.get(url, params=params)
            response.raise_for_status()
            logging.info("Price for bybit : %s", response.json())
            return float(response.json()["result"]["lp"])
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching price from Bybit: %s", e)
            raise

    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict:
        """
        Places a market order on Bybit for the given symbol, side, and quantity.
        """
        logging.info("Placing order on Bybit : %s", symbol)
        try:
            url = f"{self.base_url}/spot/v3/private/order"
            params = {
                "orderType": "MARKET",
                "orderQty": format_price_quantity(quantity, symbol),
                "side": side.upper(),
                "symbol": symbol,
            }
            headers = {
                'X-BAPI-API-KEY': self.api_key,
                'X-BAPI-TIMESTAMP': str(self.get_timestamp()),
                'X-BAPI-SIGN': self.generate_signature(symbol, side.upper(), quantity),
                'X-BAPI-RECV-WINDOW': '5000'
            }
            response = requests.post(url, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
            if data["retCode"] == 0 and "result" in data and "orderId" in data["result"]:
                return data
            else:
                logging.error("Error placing order on Bybit: %s", data['retMsg'])
                raise Exception(f"Error placing order on Bybit: {data['retMsg']}")
        except requests.exceptions.RequestException as e:
            logging.error("Error placing order on Bybit: %s", e)
            raise

    def get_timestamp(self) -> int:
        """
        Retrieves the current timestamp in milliseconds.
        """
        return int(requests.get(f"{self.base_url}/v3/public/time").json()["result"]["timeSecond"]) * 1000

    def generate_signature(self, symbol: str, side: str, quantity: float) -> str:
        """
        Generates the signature for the Bybit API request.
        """
        params = {
            "orderType": "MARKET",
            "orderQty": format_price_quantity(quantity, symbol),
            "side": side,
            "symbol": symbol
        }
        signature = "&".join([f"{key}={value}" for key, value in params.items()])
        signature = f"{signature}&api_secret={self.api_secret}"
        return requests.utils.quote(signature)