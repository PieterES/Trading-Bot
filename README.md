# Trading-Bot
Trading bot for trading crypto using fake balances

# Different Bots:

**Simple Bot:**
Keeps track of the value of Ethereum from the last trade. If the current price is higher than the previous price and some threshold, we buy. If lower than some threshold, we sell otherwise we hold.
Checks every 10 minutes. Keeps track of the price, trade decision, ethereum balance, euro balance, original value, current value and profit. Transaction fees are not included.
Loses money gradually.

**The Fibonacci bot:**
executes buy and sell orders based on Fibonacci Retracement levels, dynamically calculating high and low prices over the past 24 hours, and a profitability check that includes trading fees. Its strategy revolves around the principle that after a significant price movement, the market will often retrace or reverse a part of that movement before continuing in the original direction. The bot uses this concept to make trading decisions, aiming to buy low and sell high within these natural market fluctuations.

Several more bots will be implemented with more complicated trading decisions.
