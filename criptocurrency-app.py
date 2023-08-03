import streamlit as st
from PIL import Image
from bs4 import BeautifulSoup
import  requests
import json

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
    soup      = BeautifulSoul(cmc.content,'html.parser')
    data      = soup.find('script',id='__NEXT_DATA__',type='application/json')
    coin_data = json.loads(data.contents[0])
    listingsT = json.loads(coin_data['props']['initialState'])['cryptocurrency']['listingLatest']['data']
    keysArr   = listingsT[0]
    listings  = listngsT[1:]
    coins     = {}
    for i in listings:
       coins[str(i[keysArr.index('id')])] = i[keysArr.index('slug')]
    coin_name   =[]
    coin_symbol =[]
    maket_cap   =[]
    percent_change_1h  = []
    percent_change_24h = []
    percent_change_7d  = []
    price              = []
    volumen_24h        = []

    for i in listings:
       coin_name.append(i[keysArr.index('slug')]) 
       coin_symbol.append(i[keysArr.index('symbol')])
    #return df

#df = load_data()

## SIDEBAR - CRYPTOCURRENCY SELECTIONS
