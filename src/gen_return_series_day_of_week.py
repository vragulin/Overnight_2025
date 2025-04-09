"""  Generate return series for the given stocks
V. Ragulin - 2025-02-28
"""
import pandas as pd

# Define the day of the week to filter by
DAY_OF_WEEK = "Friday"  # 'Friday'  # Change this to the desired day of the week, or None for no filtering

# Load the data
data = pd.read_csv('../data/meme_stocks_5y.csv', header=[0, 1], index_col=0, parse_dates=True).sort_index(axis=1)

# Initialize dictionaries to store the returns
overnight_returns = {}
intraday_returns = {}
full_daily_returns = {}

# Calculate the returns for each stock
for ticker in data.columns.levels[0]:
    stock_data = data[ticker]

    # Calculate overnight return (previous close to open)
    overnight_returns[ticker] = (stock_data['Open'] / stock_data['Close'].shift(1)) - 1

    # Calculate intraday return (open to close)
    intraday_returns[ticker] = (stock_data['Close'] / stock_data['Open']) - 1

    # Calculate full daily return (previous close to close)
    full_daily_returns[ticker] = (stock_data['Close'] / stock_data['Close'].shift(1)) - 1

# Convert dictionaries to DataFrames
overnight_returns_df = pd.DataFrame(overnight_returns)
intraday_returns_df = pd.DataFrame(intraday_returns)
full_daily_returns_df = pd.DataFrame(full_daily_returns)

# Add a column to each DataFrame for the equal-weighted basket return
overnight_returns_df['Equal_Weighted'] = overnight_returns_df.mean(axis=1, skipna=True)
intraday_returns_df['Equal_Weighted'] = intraday_returns_df.mean(axis=1, skipna=True)
full_daily_returns_df['Equal_Weighted'] = full_daily_returns_df.mean(axis=1, skipna=True)

# Specify the day of the week for filtering (e.g., 'Monday', 'Tuesday', etc.)
day_of_week = DAY_OF_WEEK  # Change this to the desired day of the week

# Apply the day-of-week filter to the calculated DataFrames
if day_of_week in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
    overnight_returns_df = overnight_returns_df[overnight_returns_df.index.day_name() == day_of_week]
    intraday_returns_df = intraday_returns_df[intraday_returns_df.index.day_name() == day_of_week]
    full_daily_returns_df = full_daily_returns_df[full_daily_returns_df.index.day_name() == day_of_week]

# Calculate cumulative returns
cumulative_overnight_returns = (1 + overnight_returns_df).cumprod() - 1
cumulative_intraday_returns = (1 + intraday_returns_df).cumprod() - 1
cumulative_full_daily_returns = (1 + full_daily_returns_df).cumprod() - 1

# Aggregate cumulative returns into a single DataFrame
cumulative_returns = pd.DataFrame({
    'Overnight': cumulative_overnight_returns.iloc[-1],
    'Intraday': cumulative_intraday_returns.iloc[-1],
    'Full_Day': cumulative_full_daily_returns.iloc[-1]
})

# Print the cumulative returns
print(f"Cumulative Returns for {day_of_week}:")
print(cumulative_returns)
# Save the cumulative returns to a CSV file
cumulative_returns.to_csv(f'../data/cumulative_returns_{day_of_week}.csv')
cumulative_returns.to_clipboard(index=True, header=True)
