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
    cmc = requests.get("https://coinmarketcap.com")
    #return df

#df = load_data()

## SIDEBAR - CRYPTOCURRENCY SELECTIONS
