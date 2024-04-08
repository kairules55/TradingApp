from typing import List, Tuple


def get_best_price(prices: List[Tuple[str, float]], order_type: str) -> Tuple[str, float]:
    """
    Returns the exchange name and the best price for the given order type.
    """
    if order_type == "buy":
        # For a buy order, the best price is the lowest one
        best_price = min(prices, key=lambda x: x[1])
    elif order_type == "sell":
        # For a sell order, the best price is the highest one
        best_price = max(prices, key=lambda x: x[1])
    else:
        raise ValueError("Invalid order type. Must be 'buy' or 'sell'.")

    return best_price


def format_price_quantity(value: float, symbol: str) -> str:
    """
    Formats the price and quantity for the exchange API calls.
    """
    if symbol == "BTCUSDT":
        return f"{value:.8f}"
    else:
        return f"{value:.2f}"