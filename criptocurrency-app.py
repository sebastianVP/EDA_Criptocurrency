import streamlit as st
from PIL import Image
import base64
from bs4 import BeautifulSoup
import  requests
import json
import pandas as pd

#-----------------------------------#
# Page Layout
##Page expands to full width
st.set_page_config(layout="wide")
#-----------------------------------#
# TITLE
image= Image.open("C:/Users/soporte/worspace/EDA_Criptocurrency/cripto_alex.jpg")
st.image(image,width=500)
st.title("Criptocurrency Web App - Data Analysis")

st.markdown("""
Esta aplicacion muestra el precio de una lista de criptomonedas en una moneda determinada
desde la  **CoinMarketCap**!
""")
#------------------------------------#
#About
expander_bar = st.expander("**About**")
expander_bar.markdown("""
Utiliza las librerias:
* **Python Libraries:** Streamlite,base64,request,json,bs4
* **DataSource:** [CoinMarketCap](https://coinmarketcap.com)
* **Credit:** Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf).
""")
#-------------------------------------#
# SETTING PAGE LAYOUT
# DIVIDE PAGE TO 3 COLUMNS (COL 1 =SIDEBAR,COL2 AND COL3 =PAGE_CONTENTS)
col1 = st.sidebar
col2,col3 =st.columns((2,1))

# Sidebar + Main Panel
col1.header("Input Options")
# Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Select currency for price',('USD','BTC','ETH'))

# Web Scraping of Coin Marketcap data
@st.cache_data
def load_data():
    cmc       = requests.get("https://coinmarketcap.com")
    soup      = BeautifulSoup(cmc.content,'html.parser')
    data      = soup.find('script',id='__NEXT_DATA__',type='application/json')
    coin_data = json.loads(data.contents[0])
    listingsT = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
    keysArr   = listingsT[0]['keysArr']
    listings  = listingsT[1:]
    coins     = {}
    for i in listings:
       coins[str(i[keysArr.index('id')])] = i[keysArr.index('slug')]
    coin_name   =[]
    coin_symbol =[]
    market_cap   =[]
    percent_change_1h  = []
    percent_change_24h = []
    percent_change_7d  = []
    price              = []
    volume_24h        = []

    for i in listings:
       coin_name.append(i[keysArr.index('slug')]) 
       coin_symbol.append(i[keysArr.index('symbol')])
       price.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'price')])
       percent_change_1h.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'percentChange1h')])
       percent_change_24h.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'percentChange24h')])
       percent_change_7d.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'percentChange7d')])
       market_cap.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'marketCap')])
       volume_24h.append(i[keysArr.index('quote'+'.'+currency_price_unit+'.'+'volume24h')])

    df = pd.DataFrame(columns=['coin_name', 'coin_symbol', 'market_cap', 'percent_change_1h', 'percent_change_24h', 'percent_change_7d', 'price', 'volume_24h'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['percent_change_1h'] = percent_change_1h
    df['percent_change_24h'] = percent_change_24h
    df['percent_change_7d'] = percent_change_7d
    df['market_cap'] = market_cap
    df['volume_24h'] = volume_24h
    return df

df = load_data()

## Sidebar - Cryptocurrency selections
sorted_coin = sorted( df['coin_symbol'] )
selected_coin = col1.multiselect('Cryptocurrency', sorted_coin, sorted_coin)

df_selected_coin = df[ (df['coin_symbol'].isin(selected_coin)) ] # Filtering data
## SIDEBAR - NUMBER OF COINS TO DISPLAY
num_coin = col1.slider('Display Top N Coins', 1, 100, 100)
df_coins = df_selected_coin[:num_coin]

## Sidebar - Percent change timeframe
percent_timeframe = col1.selectbox('Percent change time frame',
                                    ['7d','24h', '1h'])
percent_dict = {"7d":'percent_change_7d',"24h":'percent_change_24h',"1h":'percent_change_1h'}
selected_percent_timeframe = percent_dict[percent_timeframe]

## Sidebar - Sorting values
sort_values = col1.selectbox('Sort values?', ['Yes', 'No'])

col2.subheader('Price Data of Selected Cryptocurrency')
col2.write('Data Dimension: ' + str(df_selected_coin.shape[0]) + ' rows and ' + str(df_selected_coin.shape[1]) + ' columns.')

col2.dataframe(df_coins)

# Download CSV Data
def filedownload(df):
     csv = df.to_csv(index=False)
     b64 = base64.b64encode(csv.encode()).decode() # strings <-> bytes conversion
     href = f'<a href="data:file/csv;base64,{b64}" download="crypto.csv">Download CSV</a>'
     return href

col2.markdown(filedownload(df_selected_coin),unsafe_allow_html=True)


#-------------------------------#
#Preparing data for BAR Plot of % Price Change
