import os
import logging
from dotenv import load_dotenv
from exchanges.binance import BinanceClient
from exchanges.bybit import BybitClient
from utils.helpers import get_best_price

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingApp:
    def __init__(self):
        load_dotenv()
        self.clients = {
            "binance": BinanceClient(
                api_key=os.getenv("BINANCE_API_KEY"),
                api_secret=os.getenv("BINANCE_API_SECRET")
            ),
            "bybit": BybitClient(
                api_key=os.getenv("BYBIT_API_KEY"),
                api_secret=os.getenv("BYBIT_API_SECRET")
            )
        }

    def trade(self, order_type: str, quantity: float) -> None:
        """
        Executes a market order for the BTC/USDT pair on the exchange with the best price.
        """
        try:
            prices = [(name, client.get_ticker_price("BTCUSDT")) for name, client in self.clients.items()]
        
            exchange, price = get_best_price(prices, order_type)

            logging.info(f"Best price for a {order_type.upper()} order: {price:.2f} USDT on {exchange.upper()} exchange.")

            order_details = self.clients[exchange].place_market_order("BTCUSDT", order_type, quantity)

            logging.info(f"Placed a {order_type.upper()} order for {quantity} BTC at {price} USDT on {exchange.upper()} exchange.")
        except KeyError as e:
            logging.error(f"Error executing the trade: KeyError - {str(e)}. Check if the exchange is correctly set up.")
        except ConnectionError as e:
            logging.error(f"Error executing the trade: ConnectionError - {str(e)}. Check your network connection.")
        except Exception as e:
            logging.error(f"Error executing the trade: {type(e).__name__} - {str(e)}")
            

if __name__ == "__main__":
    app = TradingApp()
    app.trade("buy", 0.001)
    app.trade("sell", 0.001)