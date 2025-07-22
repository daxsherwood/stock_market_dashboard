import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Set the title of the dashboard
st.title("Stock Market Explorer")

# User input for ticker symbol
st.subheader("Select a Stock Ticker")
ticker = st.text_input("Enter the stock ticker symbol (e.g., NVDA, AAPL, TSLA):", value="NVDA")

# Fetch stock data
st.subheader(f"{ticker.upper()} Stock Price Visualization")

# Define date range options
date_options = ["1 Day", "5 Days", "1 Month", "3 Months", "YTD", "1 Year", "All"]
selected_option = st.selectbox("Select Date Range", date_options)

# Calculate start and end dates based on the selected option
end_date = datetime.today()
if selected_option == "1 Day":
    start_date = end_date - timedelta(days=1)
elif selected_option == "5 Days":
    start_date = end_date - timedelta(days=5)
elif selected_option == "1 Month":
    start_date = end_date - timedelta(days=30)
elif selected_option == "3 Months":
    start_date = end_date - timedelta(days=90)
elif selected_option == "YTD":
    start_date = datetime(end_date.year, 1, 1)
elif selected_option == "1 Year":
    start_date = end_date - timedelta(days=365)
elif selected_option == "All":
    start_date = datetime(2000, 1, 1)  # Arbitrary start date for "All"

# Fetch data from yfinance
data = yf.download(ticker, start=start_date, end=end_date)

# Plot the closing price
if not data.empty:
    st.line_chart(data["Close"])
else:
    st.error("No data available for the selected ticker or date range.")