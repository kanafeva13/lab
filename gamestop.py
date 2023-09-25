import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import bs4 as bs
gamestop = yf.Ticker('GME')
gme_data = gamestop.history(period = 'max')
gme_data.reset_index(inplace=True)
url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
html_data = requests.get(url).text
print(html_data)
soup1 = bs.BeautifulSoup(html_data, 'lxml')
gme_revenue = pd.DataFrame(columns=['Date', 'Revenue'])
for row in soup1.find('tbody').find_all('tr'):
    col = row.find_all('td')
    Date = col[0].text
    Revenue = col[1].text.replace('$', '').replace(',', '')
    new_df = pd.DataFrame({'Date': [Date], 'Revenue': [Revenue]})
    gme_revenue = pd.concat([gme_data, new_df], ignore_index=True)
gme_data['Date'] = pd.to_datetime(gme_data['Date'])
gme_revenue['Date'] = pd.to_datetime(gme_revenue['Date'])
print(gme_revenue.tail(5))
def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing=.3)
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=stock_data_specific.Date, y=stock_data_specific.Close, name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=revenue_data_specific.Date, y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False, height=900, title=stock, xaxis_rangeslider_visible=True)
    fig.show()
make_graph(gme_data, gme_revenue, 'GameStop')