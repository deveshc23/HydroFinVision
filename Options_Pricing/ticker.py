import datetime
import yfinance as yf
import requests_cache
import matplotlib.pyplot as plt


def get_historic_data(ticker, start_date=None, end_date=None, cache_data=True, cache_days=1):
    """Fetch historical data for a ticker using yfinance with optional caching."""
    try:
        # Configure cache settings
        expire_after = datetime.timedelta(days=cache_days)
        session = requests_cache.CachedSession(
            cache_name='cache',
            backend='sqlite',
            expire_after=expire_after
        )
        session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Accept': 'application/json;charset=utf-8'
        }

        # Fetch data using yfinance
        if start_date and end_date:
            data = yf.download(ticker, start=start_date, end=end_date, session=session)
        else:
            data = yf.download(ticker, session=session)

        if data.empty:
            return None

        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None


def get_columns(data):
    if data is None:
        return None
    return list(data.columns.get_level_values(0))


def get_last_price(data, column_name):
    if data is None or column_name not in get_columns(data):
        return None
    return data[column_name].iloc[-1]


def plot_data(data, ticker):
    try:
        if data is None:
            print("Invalid data provided.")
            return

        # Filter out 'Adj Close' and ensure valid columns
        columns_to_plot = [col for col in list(data.columns.get_level_values(0)) if col != 'Volume' and col != 'Adj Close']

        if not columns_to_plot:
            print("No valid columns to plot.")
            return

        # Plot all valid columns on the same graph
        data[columns_to_plot].plot(figsize=(12, 8))
        plt.ylabel('Values')
        plt.xlabel('Date')
        plt.title(f'Historical data for {ticker} (Excluding Adj Close)')
        plt.legend(loc='best')
        plt.show()
    except Exception as e:
        print(f"Error plotting data: {e}")
        return