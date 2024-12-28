import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

class BlackScholesModel:
    def __init__(self, S, K, T, r, sigma, option_type="call"):
        self.S = S  # Current stock price (spot price on the day of the option)
        self.K = K  # Option strike price
        self.T = T  # Time to expiration in years
        self.r = r  # Risk-free rate (annualized)
        self.sigma = sigma  # Volatility (annualized)
        self.option_type = option_type  # 'call' or 'put'

    def calculate(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        
        if self.option_type == "call":
            price = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == "put":
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        return price

    def delta(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        
        if self.option_type == "call":
            return norm.cdf(d1)
        elif self.option_type == "put":
            return norm.cdf(d1) - 1

    def gamma(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def theta(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)
        
        if self.option_type == "call":
            theta = (-self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == "put":
            theta = (-self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
        
        return theta

    def vega(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T))
        return self.S * norm.pdf(d1) * np.sqrt(self.T)

    def rho(self):
        d2 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T) / (self.sigma * np.sqrt(self.T)) - self.sigma * np.sqrt(self.T)
        
        if self.option_type == "call":
            return self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        elif self.option_type == "put":
            return -self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)

ticker = "SPY"
df = yf.download(ticker, period="6mo")

spy = yf.Ticker(ticker)
expiration_dates = spy.options
print(f"Available Expiration Dates: {expiration_dates}")

strike_price_to_check = 580

# Prepare lists to store data
expiration_dates_list = []
call_theoretical_prices = []
put_theoretical_prices = []
call_actual_prices = []
put_actual_prices = []

call_deltas = []
put_deltas = []
call_gammas = []
put_gammas = []
call_thetas = []
put_thetas = []
call_vegas = []
put_vegas = []
call_rhos = []
put_rhos = []

r = 0.04 

for expiration_date in expiration_dates:
    option_chain = spy.option_chain(expiration_date)
    
    calls = option_chain.calls[option_chain.calls['strike'] == strike_price_to_check]
    puts = option_chain.puts[option_chain.puts['strike'] == strike_price_to_check]
    
    if not calls.empty and not puts.empty:
        spot_price = df.loc[df.index <= pd.to_datetime(expiration_date)].iloc[-1]['Close']  # Last close before expiration
        
        implied_volatility = calls.iloc[0]['impliedVolatility']
        
        T = (pd.to_datetime(expiration_date) - pd.to_datetime(df.index[-1])).days / 365  # Time to expiration
        
        call_bs = BlackScholesModel(spot_price, strike_price_to_check, T, r, implied_volatility, option_type="call")
        put_bs = BlackScholesModel(spot_price, strike_price_to_check, T, r, implied_volatility, option_type="put")
        
        call_actual = calls.iloc[0]['lastPrice']  
        put_actual = puts.iloc[0]['lastPrice']    
        
        call_deltas.append(call_bs.delta())
        put_deltas.append(put_bs.delta())
        call_gammas.append(call_bs.gamma())
        put_gammas.append(put_bs.gamma())
        call_thetas.append(call_bs.theta())
        put_thetas.append(put_bs.theta())
        call_vegas.append(call_bs.vega())
        put_vegas.append(put_bs.vega())
        call_rhos.append(call_bs.rho())
        put_rhos.append(put_bs.rho())

        expiration_dates_list.append(expiration_date)
        call_theoretical_prices.append(call_bs.calculate())
        put_theoretical_prices.append(put_bs.calculate())
        call_actual_prices.append(call_actual)
        put_actual_prices.append(put_actual)

plt.figure(figsize=(10, 6))
plt.plot(expiration_dates_list, call_theoretical_prices, label='Call Option Theoretical Price', color='blue', marker='o')
plt.plot(expiration_dates_list, call_actual_prices, label='Call Option Actual Price', color='green', marker='x')
plt.xlabel('Expiration Date')
plt.ylabel('Price')
plt.title(f"Theoretical vs Actual Call Option Prices for SPY at Strike {strike_price_to_check}")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.plot(expiration_dates_list, put_theoretical_prices, label='Put Option Theoretical Price', color='red', marker='o')
plt.plot(expiration_dates_list, put_actual_prices, label='Put Option Actual Price', color='orange', marker='x')
plt.xlabel('Expiration Date')
plt.ylabel('Price')
plt.title(f"Theoretical vs Actual Put Option Prices for SPY at Strike {strike_price_to_check}")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 8))
plt.plot(expiration_dates_list, call_deltas, label="Call Delta", color='blue')
plt.plot(expiration_dates_list, call_gammas, label="Call Gamma", color='green')
plt.plot(expiration_dates_list, call_thetas, label="Call Theta", color='red')
plt.plot(expiration_dates_list, call_vegas, label="Call Vega", color='purple')
plt.plot(expiration_dates_list, call_rhos, label="Call Rho", color='orange')
plt.xlabel('Expiration Date')
plt.ylabel('Greek Value')
plt.title(f"Greeks for Call Option at Strike {strike_price_to_check}")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(12, 8))
plt.plot(expiration_dates_list, put_deltas, label="Put Delta", color='blue')
plt.plot(expiration_dates_list, put_gammas, label="Put Gamma", color='green')
plt.plot(expiration_dates_list, put_thetas, label="Put Theta", color='red')
plt.plot(expiration_dates_list, put_vegas, label="Put Vega", color='purple')
plt.plot(expiration_dates_list, put_rhos, label="Put Rho", color='orange')
plt.xlabel('Expiration Date')
plt.ylabel('Greek Value')
plt.title(f"Greeks for Put Option at Strike {strike_price_to_check}")
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()
