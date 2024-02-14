import requests
import time

# Kraken Public API Endpoint for Ticker Information
TICKER_URL = 'https://api.kraken.com/0/public/Ticker'
def get_eth_price():
    """Fetch the current price of ETH in EUR from Kraken."""
    response = requests.get(TICKER_URL, params={'pair': 'ETHEUR'})
    result = response.json()
    price_str = result['result']['XETHZEUR']['c'][0]  # Last trade price
    return float(price_str)

# Starting balances
balance_eur = 1000
balance_eth = 1
original_value = 1000+get_eth_price()
original_eth_value = get_eth_price()
# Simple strategy parameters
upper_threshold = 1.0001  # Buy if price is 0.1% above the last buy price
lower_threshold = 0.9999  # Sell if price is 0.1% below the last buy price
last_trade_price = None  # Track the price of the last trade


def trade_decision(current_price):
    """Decide whether to buy, sell, or hold based on the current price and simple strategy."""
    global last_trade_price, balance_eur, balance_eth

    if last_trade_price is None:
        last_trade_price = current_price
        return 'INITIAL HOLD'  # Initial state, no trade history

    if current_price >= last_trade_price * upper_threshold and balance_eur > current_price*0.0001:
        # Buy 1 ETH, ensuring EUR balance won't go to 0
        balance_eur -= current_price*0.0001
        balance_eth += 0.0001
        last_trade_price = current_price
        return 'BUY'

    elif current_price <= last_trade_price * lower_threshold and balance_eth > 0.0001:
        # Sell 1 ETH, ensuring ETH balance won't go to 0
        balance_eur += current_price*0.0001
        balance_eth -= 0.0001
        last_trade_price = current_price
        return 'SELL'

    return 'HOLD'


def main():
    try:
        while True:
            current_price = get_eth_price()
            decision = trade_decision(current_price)
            print(f"Current ETH Price: €{current_price:.2f}")
            print(f"Trade Decision: {decision}")
            print(f"Updated Balances: {balance_eth} ETH, €{balance_eur:.2f}")
            print(f"Current Total value: {((balance_eth*current_price) + balance_eur):.2f}")
            print(f"Current Profit, no trades: {((balance_eth*current_price) + balance_eur - (1000+current_price)):.2f}\n")
            # Wait for 10 minutes before checking again
            time.sleep(600)  # 600 seconds = 10 minutes
    except KeyboardInterrupt:
        print("Script stopped by user.")
        print(f"Final Balances: {balance_eth} ETH, €{balance_eur:.2f}")
        print(f"Final Total value: {balance_eth * current_price + balance_eur:.2f}")
        print(f"Final Profit, no trades, original price: {((balance_eth * current_price) + balance_eur - (1000 + original_eth_value)):.2f}")
        print(f"Final Profit, no trades, current price: {((balance_eth*current_price) + balance_eur - (1000+current_price)):.2f}")

if __name__ == "__main__":
    main()