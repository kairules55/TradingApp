import unittest
from unittest.mock import patch
from trading_app.exchanges.binance import BinanceClient

class TestBinanceClient(unittest.TestCase):
    def setUp(self):
        self.client = BinanceClient("api_key", "api_secret")

    @patch("requests.get")
    def test_get_ticker_price(self, mock_get):
        mock_get.return_value.json.return_value = {"price": "50000.00"}
        mock_get.return_value.raise_for_status.return_value = None
        price = self.client.get_ticker_price("BTCUSDT")
        self.assertEqual(price, 50000.00)

    @patch("requests.post")
    def test_place_market_order(self, mock_post):
        mock_post.return_value.json.return_value = {"orderId": 123456}
        mock_post.return_value.raise_for_status.return_value = None
        order_details = self.client.place_market_order("BTCUSDT", "buy", 0.001)
        self.assertEqual(order_details["orderId"], 123456)