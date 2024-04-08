# Trading App

This is a Python-based trading application that integrates with the Binance and Bybit cryptocurrency exchanges. The application allows you to place market orders on the exchange with the best available price.


# Requirements:

Python 3.9+
pip
virtualenv (optional)


### Installation and Setup:

```bash
python -m venv venv
source venv/bin/activate
```


### Install the required dependencies:

```bash
pip install -r requirements.txt

Environment Variables:
BINANCE_API_KEY
BINANCE_API_SECRET
BYBIT_API_KEY
BYBIT_API_SECRET

Run Command:
python3 trading_app/main.py
```

## Exchanges Integration:

The integration with Binance and Bybit exchanges is implemented in the trading_app/exchanges directory.

### binance.py:

Implements the BinanceClient class, which provides methods to interact with the Binance exchange API.
Includes methods to get the current market price, place market orders, and handle various error cases.

## bybit.py:

Implements the BybitClient class, which provides methods to interact with the Bybit exchange API.
Includes methods to get the current market price, place market orders, and handle various error cases.
Main Application Logic:

## main.py

The main application logic is implemented in the trading_app/main.py file.

The TradingApp class is the entry point of the application.
The trade method is responsible for executing the trading logic:
It retrieves the current market prices from both Binance and Bybit exchanges.
It selects the exchange with the best price for the given order type (buy or sell).
It places the market order on the selected exchange.
It handles various error cases that may occur during the order execution.