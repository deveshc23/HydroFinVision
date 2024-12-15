import pandas as pd
import yfinance as yf


class Nifty50Returns:
    def __init__(self, ticker_list):
        self.ticker_list = ticker_list
        self.data = {}

    def fetch_data(self, start_date, end_date):
        for ticker in self.ticker_list:
            stock_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if not stock_data.empty:
                self.data[ticker] = stock_data

    def calculate_returns(self):
        results = []  # List to store data rows
        for ticker, df in self.data.items():
            # Calculate 5-year return based on start and end values
            five_year_return = self.calculate_five_year_return(df)

            # Calculate other returns
            one_year_return = self.calculate_period_return(df, 12)
            six_month_return = self.calculate_period_return(df, 6)

            # Calculate 52-week high and low
            one_year_data = df.iloc[-252:]  # Last year (approx. 252 trading days)
            highest_close = one_year_data['Adj Close'].max()
            lowest_close = one_year_data['Adj Close'].min()

            # Append the data for this ticker
            results.append([ticker, five_year_return, one_year_return, six_month_return, highest_close, lowest_close])

        # Convert the results list to DataFrame
        results_df = pd.DataFrame(results, columns=[
            'Ticker', '5_Year_Return', '1_Year_Return', '6_Month_Return', '52_Week_High', '52_Week_Low'
        ])

        return results_df

    @staticmethod
    def calculate_five_year_return(df):
        # Get the price 5 years ago and the price on the last date
        start_price = df.iloc[0]['Adj Close']  # First available price
        end_price = df['Adj Close'].iloc[-1]  # Last available price
        if start_price is not None:
            return ((end_price - start_price) / start_price) * 100
        return None

    @staticmethod
    def calculate_period_return(df, months):
        end_date = df.index[-1]
        start_date = end_date - pd.DateOffset(months=months)
        start_price = None
        if start_date in df.index:
            start_price = df.loc[start_date, 'Adj Close']
        elif not df[df.index <= start_date].empty:
            start_price = df[df.index <= start_date]['Adj Close'].iloc[-1]
        end_price = df['Adj Close'].iloc[-1]
        if start_price is not None:
            return ((end_price - start_price) / start_price) * 100
        return None


# List of Nifty50 stock tickers
nifty50_tickers = [
    'RELIANCE.NS', 'TCS.NS', 'INFY.NS', 'HDFCBANK.NS', 'ICICIBANK.NS',
    'HINDUNILVR.NS', 'SBIN.NS', 'BAJFINANCE.NS', 'KOTAKBANK.NS', 'ITC.NS',
    'LT.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 'HCLTECH.NS', 'MARUTI.NS',
    'BHARTIARTL.NS', 'ULTRACEMCO.NS', 'TITAN.NS', 'ADANIGREEN.NS', 'WIPRO.NS',
    'M&M.NS', 'ONGC.NS', 'NTPC.NS', 'SUNPHARMA.NS', 'TATASTEEL.NS',
    'POWERGRID.NS', 'COALINDIA.NS', 'BPCL.NS', 'BAJAJFINSV.NS', 'ADANIPORTS.NS',
    'HEROMOTOCO.NS', 'TECHM.NS', 'CIPLA.NS', 'DIVISLAB.NS', 'DRREDDY.NS',
    'GRASIM.NS', 'JSWSTEEL.NS', 'SHREECEM.NS', 'EICHERMOT.NS', 'BRITANNIA.NS',
    'HINDALCO.NS', 'TATAMOTORS.NS', 'UPL.NS', 'VEDL.NS', 'ADANIENT.NS',
    'ICICIGI.NS', 'ICICIPRULI.NS', 'SBICARD.NS', 'INDUSINDBK.NS', 'BAJAJHLDNG.NS'
]

# Initialize and process the data
start_date = '2019-01-01'
end_date = '2024-01-01'

nifty50_returns = Nifty50Returns(nifty50_tickers)
nifty50_returns.fetch_data(start_date, end_date)
final_df = nifty50_returns.calculate_returns()

# Display the final DataFrame
print(final_df)
