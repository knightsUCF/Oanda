import json
import requests




token = ''
account_id = ''
header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token, 'accountID': account_id,}




def get_price(symbol = 'GBP_USD'):
    params = (('instruments', symbol),)  # can request multiple quotes: 'EUR_USD,USD_CAD'
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + '/pricing?instruments=EUR_USD%2CUSD_CAD'
    response = requests.get(url, headers = header, params = params)
    broker_data = response.json()
    print(broker_data['prices'][0]['bids'][0]['price'])



def get_balance():
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + '/summary'
    response = requests.get(url, headers = header)
    broker_data = response.json()
    print(broker_data['account']['balance'])



def send_order():
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + '/orders'

    params = {
        "order": {
            "units": "1",
            "instrument": "GBP_USD",
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
        }
    }

    response = requests.post(url, headers = header, json = params)
    broker_data = response.json()
    print(broker_data)



def close_order(symbol = 'GBP_USD'):
    url = 'https://api-fxtrade.oanda.com/v3/accounts/' + account_id + '/positions/' + symbol + '/close'
    params = {
        "longUnits": "ALL"
    }

    # "https://api-fxtrade.oanda.com/v3/accounts/<ACCOUNT>/positions/EUR_USD/close"
    response = requests.put(url, headers = header, json = params)
    broker_data = response.json()
    print(broker_data)



# get_price(symbol = 'GBP_JPY')
# get_balance()


send_order()


# close_order()







import quandl
import pandas
from bokeh.plotting import figure, output_file, show



# api keys

key = ''
version = ''


# connect to quandl

quandl.ApiConfig.api_key = key
quandl.ApiConfig.api_version = version


# data settings

# symbol = 'EOD/HD'
symbol = 'ECB/EURUSD'
bars = 800
timeframe = 'daily'
# feature = 'Close'
feature = 'Value'


# pull Pandas dataframe from Quandl - symbols: https://www.quandl.com/search?query=

df = quandl.get(symbol, collapse = timeframe)
df = df.tail(bars)


# create a close price feature in the dataframe

price = df[feature]




# add a moving average

# df['sma'] = price.rolling(window=90).mean()
# sma = df['sma']

df['ema'] = price.ewm(span=90,adjust=False).mean()
ema = df['ema']





# graphing

def graph(df, df2):
    output_file('line.html')
    p = figure(plot_width = 1000, plot_height = 1000, background_fill_color = 'black')
    p.xgrid.visible = False
    p.ygrid.visible = False
    p.line(df.index, df, line_width = 2, line_color = 'blue')
    p.line(df.index, df2, line_width = 2, line_color = '#CC3399')
    show(p)



# graph(price, ema)

# graph(sma)










# http://developer.oanda.com/rest-live-v20/pricing-ep/#CurrentPrices


# in case string conversion is incorrect: response = requests.get('https://api-fxtrade.oanda.com/v3/accounts/<ACCOUNT>/pricing?instruments=EUR_USD%2CUSD_CAD', headers=headers)


# print(r.status_code) # status code of 200 is a successful request, do a try except on error
# print(r.headers)
