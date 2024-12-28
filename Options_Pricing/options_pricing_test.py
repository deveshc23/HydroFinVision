from Options_Pricing import ticker,MonteCarloSimulation,BinomialTreemodel,Black_Scholes_Model
import numpy as np
symbol='AAPL'
data=ticker.get_historic_data(symbol,start_date='2020-01-01',end_date='2024-12-25')
print(ticker.get_columns(data))
current_price = ticker.get_last_price(data, 'Close')
data['Returns'] = data['Close'].pct_change()
volatility = np.std(data['Returns'].dropna()) * np.sqrt(252)

# print(ticker.get_last_price(data,'Close'))
# ticker.plot_data(data,symbol)

print(current_price)
BSM=Black_Scholes_Model.BlackScholesModel(current_price,260,8,0.04,volatility)
print(BSM.calculate_option_price('Call Option'))
