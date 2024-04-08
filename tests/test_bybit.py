import unittest
from unittest.mock import patch
from trading_app.exchanges.bybit import BybitClient

class TestBybitClient(unittest.TestCase):
    def setUp(self):
        self.client = BybitClient("api_key", "api_secret")

    @patch("requests.get")
    def test_get_ticker_price(self, mock_get):
        mock_get.return_value.json.return_value = {"result": [{"last_price": "50000.00"}]}
        mock_get.return_value.raise_for_status.return_value = None
        price = self.client.get_ticker_price("BTCUSDT")
        self.assertEqual(price, 50000.00)

    @patch("requests.post")
    def test_place_market_order(self, mock_post):
        mock_post.return_value.json.return_value = {"result": {"order_id": "123456"}}
        mock_post.return_value.raise_for_status.return_value = None
        order_details = self.client.place_market_order("BTCUSDT", "buy", 0.001)
        self.assertEqual(order_details["result"]["order_id"], "123456")