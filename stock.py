import yfinance as yf
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from datetime import date
import streamlit_shadcn_ui as ui
from alpha_vantage.fundamentaldata import FundamentalData
from stocknews import StockNews
# Set page title
st.set_page_config(page_title="Stock Dashboard", layout="wide")
# Fetch stock data
st.sidebar.header("Please filter over here:")
ticker = st.sidebar.text_input("Enter stock ticker:", "AAPL")
start_date = st.sidebar.date_input("Enter start date:",)
end_date = st.sidebar.date_input("Enter end date:")

stock_data = yf.download(ticker, start=start_date, end=end_date)

# Create line chart
fig = px.line(stock_data, x=stock_data.index, y=stock_data['Adj Close'], title=ticker)

# Display line chart
st.plotly_chart(fig)



option =ui.tabs(options=['Pricing Data','Fundmental Data','Top 10 News','Key Metrics'])
if option=='Pricing Data':
    st.header('Price')
    stock_data2 = stock_data
    stock_data2['% Change'] = stock_data['Adj Close'] / stock_data['Adj Close'].shift(1)
    st.write(stock_data2)
    annual_return = stock_data2['% Change'].mean()*365*100
    stdv = np.std(stock_data2['% Change'])*np.sqrt(365)
    st.write('Annual Return:',annual_return,'%')
    st.write('Standered Deviation:',stdv*100,'%')
    st.write('Risk Adj. Return:',annual_return/(stdv*100))

if option=='Fundmental Data':
    st.header('Fundmental Data')
    key = '0KD3CYFWW88PVU72'
    fd = FundamentalData(key,output_format = 'pandas')
    st.subheader('Balance Sheet')
    BS = fd.get_balance_sheet_annual(ticker)[0]
    bs = BS.T[2:]
    bs.columns = list(BS.T.iloc[0])
    st.write(bs)
    st.subheader('Income Statement')
    IS = fd.get_income_statement_annual(ticker)[0]
    is1 = IS.T[2:]
    is1.columns = list(IS.T.iloc[0])
    st.write(is1)
    st.subheader('Cash Flow Statement')
    CF = fd.get_cash_flow_annual(ticker)[0]
    cf = CF.T[2:]
    cf.columns = list(CF.T.iloc[0])
    st.write(cf)
    
if option == 'Top 10 News':
        st.header(f'News of {ticker}')
        sn = StockNews(ticker, save_news=False)
        df_news = sn.read_rss()
        for i in range(10):
            st.subheader(f'News {i+1}')
            st.write(df_news['published'][i])
            st.write(df_news['title'][i])
            st.write(df_news['summary'][i])
            title_sentiment = df_news['sentiment_title'][i]
            st.write(f'Title Sentiment {title_sentiment}')
            news_sentiment = df_news['sentiment_summary'][i]
            st.write(f'News Sentiment {news_sentiment}')

if option == 'Key Metrics':
            # Display key metrics
        st.header("Key Metrics")
        ticker_info = yf.Ticker(ticker).info
        st.write("Market Cap:", round(stock_data["Close"][-1] * ticker_info["sharesOutstanding"], 2))
        st.write("PE Ratio:", ticker_info["trailingPE"])
        st.write("Dividend Yield:", ticker_info["dividendYield"])