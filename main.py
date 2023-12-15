import pandas as pd
import talib as ta

# Load historical price data into a pandas DataFrame
# Replace 'your_data.csv' with your actual data source
df = pd.read_csv("BTCUSDT-1h-2023-07-02.csv")
close = df['close']
high = df['high']

# Strategy Parameters
smaLength = 200
rsiLength = 10
entryRSIRetracement = 50
exitRSIHigh = 70
exitRSILow = 40
trailingStopPercent = 1.0

# Calculate indicators
sma200 = ta.SMA(close, smaLength)
rsi = ta.RSI(close, rsiLength)

# Initialize strategy variables
position = 0
stopLossLevel = 0

# Strategy loop
position = 0  # Initialize position

for i in range(1, len(df)):  # Start the loop from index 1
    # Entry condition
    isAboveSMA = close[i] > sma200[i]
    isOversold = rsi[i] < 30
    entryCondition = isAboveSMA and (rsi[i] > 30 and rsi[i-1] <= 30)
    entryConditionRSIRetracement = (rsi[i] > entryRSIRetracement) and (rsi[i-1] <= entryRSIRetracement) and rsi[i] > 70

    # Additional Filters
    previousRSI = rsi[i-1]
    isRSIIncreasing = rsi[i] > previousRSI
    isCloseAbovePreviousClose = close[i] > close[i-1]

    entryConditionFiltered = entryCondition and isRSIIncreasing and isCloseAbovePreviousClose and entryConditionRSIRetracement

    # Trend Filter - Check if price is above the 200 SMA
    isUptrend = close[i] > sma200[i]

    # Exit condition
    exitCondition = (rsi[i] < exitRSILow) or (rsi[i] > exitRSIHigh)

    # Placing orders
    if entryConditionFiltered and isUptrend and position == 0:
        position = 1  # Enter long position

    # Dynamic Stop Loss - Place stop loss below recent swing high
    if position == 1:
        swingHighs = max(high[:i+1][-10:])
        stopLossLevel = swingHighs

    # Exit strategy
    if exitCondition:
        position = 0  # Exit position

    # Trailing Stop - Use a percentage-based trailing stop
    if position == 1 and close[i] > stopLossLevel:
        stopLossLevel = close[i] * (1 - trailingStopPercent / 100)




# Print the trading signals
for i in range(len(df)):
    print(f"Close: {df['close'][i]}, Signal: {position}")



