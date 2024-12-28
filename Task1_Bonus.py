import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller, kpss
from scipy.stats import norm

class StockAnalysis:
    def __init__(self, ticker, start_date, end_date):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.stock_data = yf.download(self.ticker, start=self.start_date, end=self.end_date)
        self.stock_data['Daily Returns'] = self.stock_data['Close'].pct_change()

    def plot_distributions(self):
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))
        axes[0].hist(self.stock_data['Volume'], bins=50, density=True, alpha=0.6, color='g')
        axes[0].set_title('Daily Volume Distribution')
        axes[0].set_xlabel('Volume')
        axes[0].set_ylabel('Density')
        axes[1].hist(self.stock_data['Close'], bins=50, density=True, alpha=0.6, color='b')
        axes[1].set_title('Daily Close Price Distribution')
        axes[1].set_xlabel('Close Price')
        axes[1].set_ylabel('Density')
        axes[2].hist(self.stock_data['Daily Returns'].dropna(), bins=50, density=True, alpha=0.6, color='r')
        axes[2].set_title('Daily Returns Distribution')
        axes[2].set_xlabel('Daily Returns')
        axes[2].set_ylabel('Density')
        plt.tight_layout()
        plt.show()

    def adf_test(self, series):
        result = adfuller(series.dropna(), maxlag=12)
        print("ADF Test for Series: ")
        print("ADF Statistic:", result[0])
        print("p-value:", result[1])
        print("Critical Values:")
        for key, value in result[4].items():
            print(f'\t{key}: {value}')

    def kpss_test(self, series):
        result = kpss(series.dropna(), regression='c')
        print("\nKPSS Test for Series: ")
        print("KPSS Statistic:", result[0])
        print("p-value:", result[1])
        print("Critical Values:", result[3])

    def perform_tests(self):
        print("\nStationarity Tests for Close Price")
        self.adf_test(self.stock_data['Close'])
        self.kpss_test(self.stock_data['Close'])
        print("\nStationarity Tests for Daily Returns")
        self.adf_test(self.stock_data['Daily Returns'])
        self.kpss_test(self.stock_data['Daily Returns'])

    def analyze_other_stock(self, other_ticker):
        stock_data_other = yf.download(other_ticker, start=self.start_date, end=self.end_date)
        stock_data_other['Daily Returns'] = stock_data_other['Close'].pct_change()
        print(f"\nStationarity Tests for {other_ticker} Close Price")
        self.adf_test(stock_data_other['Close'])
        self.kpss_test(stock_data_other['Close'])
        print(f"\nStationarity Tests for {other_ticker} Daily Returns")
        self.adf_test(stock_data_other['Daily Returns'])
        self.kpss_test(stock_data_other['Daily Returns'])

stock_analysis = StockAnalysis('AAPL', '2023-01-01', '2024-01-01')
stock_analysis.plot_distributions()
stock_analysis.perform_tests()
stock_analysis.analyze_other_stock('MSFT')
