import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Set the title of the dashboard
st.title("Stock Market Explorer")

# User input for ticker symbol
st.subheader("Select a Stock Ticker")
ticker = st.text_input("Enter the stock ticker symbol (e.g., NVDA, AAPL, TSLA):", value="NVDA")

# Define date range options and their corresponding periods
date_options = {
    "1 Day": "1d",
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "YTD": "ytd",
    "1 Year": "1y",
    "All": "max"
}

# User selects the date range
selected_option = st.selectbox("Select Date Range", list(date_options.keys()))

# Get the selected period from the dictionary
selected_period = date_options.get(selected_option, "1mo")  # Default to "1mo" if not found

# Caching the data fetching function
@st.cache_data
def fetch_data(ticker, period):
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)
    # Filter out weekends (Saturday and Sunday)
    refined_list = hist[hist.index.dayofweek < 5]
    return refined_list

# Fetch data using the cached function
data = fetch_data(ticker, selected_period)

# Remove rows with missing data
data = data.dropna(subset=['Open', 'High', 'Low', 'Close'])

# Remove rows where all four metrics (Open, High, Low, Close) are the same
data = data[~((data['Open'] == data['High']) & 
              (data['High'] == data['Low']) & 
              (data['Low'] == data['Close']))]

# Plot a candlestick chart
if not data.empty:
    fig = go.Figure(data=[go.Candlestick(
        x=data.index,  # Dates
        open=data['Open'],  # Open prices
        high=data['High'],  # High prices
        low=data['Low'],    # Low prices
        close=data['Close']  # Close prices
    )])

    # Customize the layout for better visualization
    fig.update_layout(
        title=f"{ticker.upper()} Stock Price Candlestick Chart",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        xaxis_rangeslider_visible=False,  # Hide the range slider for simplicity
        xaxis_type="date"
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)
else:
    st.error("No data available for the selected ticker or date range.")