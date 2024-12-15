
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import yfinance as yf
from datetime import datetime, timedelta

# Setup Selenium with Chrome driver and custom headers
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# URL of Nifty50 stocks page
url = 'https://www.screener.in/company/NIFTY/'
driver.get(url)
time.sleep(10)  # Wait for the page to load completely

# Fetch the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Locate the table containing the stock data
list_items=soup.findAll('th')
list_headings=[e.get_text(strip=True) for e in list_items]
unique_headings = []
for heading in list_headings:
    if heading not in unique_headings:
        unique_headings.append(heading)
data=[]
data.append(unique_headings)
rows=soup.find_all('tr')
for row in rows:
    cols = row.find_all('td')  # Find all <td> within the row
    cols = [col.get_text(strip=True) for col in cols]  # Extract text and strip whitespace
    if cols:  # Only append non-empty rows
        data.append(cols)

url='https://www.screener.in/company/NIFTY/?page=2'
driver.get(url)
time.sleep(10)  # Wait for the page to load completely

# Fetch the page source and parse it with BeautifulSoup
soup2 = BeautifulSoup(driver.page_source, 'html.parser')
rows=soup2.find_all('tr')
for row in rows:
    cols = row.find_all('td')  # Find all <td> within the row
    cols = [col.get_text(strip=True) for col in cols]  # Extract text and strip whitespace
    if cols:  # Only append non-empty rows
        data.append(cols)
df=pd.DataFrame(data)
df.columns = df.iloc[0]
df = df.drop(columns='S.No.')
df = df.iloc[1:]
df=df[df['Name']!='Median: 50 Co.']
print(df)








