import requests
import time

# Kraken Public API Endpoint for Ticker Information and OHLC Data
TICKER_URL = 'https://api.kraken.com/0/public/Ticker'
OHLC_URL = 'https://api.kraken.com/0/public/OHLC'

# Starting balances
balance_eur = 1000
balance_eth = 1

# Trading fees and minimum profit
TAKER_FEE = 0.0026  # 0.26%
MAKER_FEE = 0.0016  # 0.16%
MIN_PROFIT_PERCENT = 0.01  # 1% minimum profit


def get_eth_price():
    """Fetch the current price of ETH in EUR from Kraken."""
    response = requests.get(TICKER_URL, params={'pair': 'ETHEUR'})
    result = response.json()
    price_str = result['result']['XETHZEUR']['c'][0]  # Last trade price
    return float(price_str)


def get_recent_high_low():
    """Fetch the high and low prices of ETH in EUR over the past 24 hours from Kraken."""
    response = requests.get(OHLC_URL, params={'pair': 'ETHEUR', 'interval': 1440})  # 1440 minutes = 24 hours
    result = response.json()
    last_complete_day = result['result']['XETHZEUR'][-2]  # Use second to last item for completeness
    high_price = float(last_complete_day[2])
    low_price = float(last_complete_day[3])
    return high_price, low_price


def calculate_fib_levels(high_price, low_price):
    """Calculate Fibonacci Retracement Levels."""
    return {
        '0.236': high_price - (high_price - low_price) * 0.236,
        '0.382': high_price - (high_price - low_price) * 0.382,
        '0.5': high_price - (high_price - low_price) * 0.5,
        '0.618': high_price - (high_price - low_price) * 0.618,
        '0.786': high_price - (high_price - low_price) * 0.786
    }


def trade_decision(current_price, fib_levels, last_buy_price=None):
    """Make trade decisions based on profitability including fees."""
    global balance_eur, balance_eth

    trade_size_eth = 0.001
    cost_to_buy = (trade_size_eth * current_price) * (1 + TAKER_FEE)
    proceeds_from_sell = (trade_size_eth * current_price) * (1 - TAKER_FEE)

    # Define profitability check
    def is_trade_profitable(buy_price, sell_price):
        return sell_price > buy_price * (1 + MIN_PROFIT_PERCENT + TAKER_FEE)

    for buy_level in ['0.236', '0.382', '0.5', '0.618']:
        price = fib_levels[buy_level]
        if current_price <= price * 1.01 and current_price >= price * 0.99 and balance_eur >= cost_to_buy:
            # For buy decision, ensure we don't already hold ETH bought at a lower price unless selling is profitable
            if not last_buy_price or is_trade_profitable(last_buy_price, current_price):
                balance_eur -= cost_to_buy
                balance_eth += trade_size_eth
                return f'BUY 0.001 ETH near Fibonacci level {buy_level}', current_price

    if last_buy_price and balance_eth >= trade_size_eth:
        if is_trade_profitable(last_buy_price, current_price):
            balance_eur += proceeds_from_sell
            balance_eth -= trade_size_eth
            return 'SELL 0.001 ETH based on profitability', None

    return 'HOLD', last_buy_price


def main():
    last_buy_price = None
    try:
        while True:
            high_price, low_price = get_recent_high_low()
            fib_levels = calculate_fib_levels(high_price, low_price)
            current_price = get_eth_price()
            decision, last_buy_price = trade_decision(current_price, fib_levels, last_buy_price)
            print(f"Current ETH Price: €{current_price:.2f}")
            print(f"Trade Decision: {decision}")
            print(f"Balances: {balance_eth:.3f} ETH, €{balance_eur:.2f}, Total Value {((balance_eth*current_price) + balance_eur):.2f}")
            print(f"Current Profit, no trades: {((balance_eth*current_price) + balance_eur - (1000+current_price)):.2f}\n")
            # Wait for 10 minutes before checking again
            time.sleep(60)  # 600 seconds = 10 minutes
    except KeyboardInterrupt:
        print("Script stopped by user.")
        print(f"Original Value, no trades: {((balance_eth * current_price) + balance_eur - (1000 + current_price)):.2f}")
        print(f"Final Balances: {balance_eth:.3f} ETH, €{balance_eur:.2f}, Total Value {((balance_eth*current_price) + balance_eur):.2f}\n")

if __name__ == "__main__":
    main()