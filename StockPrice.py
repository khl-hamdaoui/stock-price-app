import yfinance as yf
import streamlit as st
from datetime import date
import altair as alt
import pandas as pd

# App setup
st.set_page_config(page_title="Stock Price App", layout="centered")

st.title("📈 Simple Stock Price App")
st.markdown("This app shows the **closing price** and **volume** of a selected stock using data from Yahoo Finance.")

# Sidebar for user inputs
st.sidebar.header(" Input")
tickerSymbol = st.sidebar.text_input("Enter Stock Ticker", value="GOOGL")
start_date = st.sidebar.date_input("Start date", value=date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", value=date(2025, 1, 1))

# Fetching data
try:
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date).reset_index()

    if tickerDf.empty:
        st.warning("No data found for the selected stock and date range.")
    else:
         # ----- Summary Statistics -----
        st.subheader("📊 Summary Statistics")
        min_price = tickerDf['Close'].min()
        max_price = tickerDf['Close'].max()
        avg_price = tickerDf['Close'].mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Min Price", f"${min_price:,.2f}")
        col2.metric("Max Price", f"${max_price:,.2f}")
        col3.metric("Avg Price", f"${avg_price:,.2f}")

        st.markdown("""
        ℹ️ **How to read this?**  
        - **Min/Max Price**: Lowest and highest closing prices in your selected date range.  
        - **Average Price**: The overall average closing price.  
        """)
        # ----- Chart 1: Closing Price -----
        st.subheader(f"📉 Closing Price for {tickerSymbol}")
        close_chart = alt.Chart(tickerDf).mark_line().encode(
            x='Date:T',
            y=alt.Y('Close:Q', title='Price (USD)', axis=alt.Axis(format='~s'))
        ).properties(
            width=700,
            height=400,
            title=f"{tickerSymbol} Closing Price"
        )
        st.altair_chart(close_chart, use_container_width=True)

        # Explanation for Closing Price Chart
        st.markdown("""
        🧾 **What does this chart show?**  
        This line chart displays the *closing price* of the stock over time.  
        - The **closing price** is the last price the stock was traded at each day.
        - This helps you see trends like increases, drops, or stability in the stock’s value.
        """)

        # ----- Chart 2: Volume -----
        st.subheader(f"📊 Volume for {tickerSymbol}")
        volume_chart = alt.Chart(tickerDf).mark_line(color='orange').encode(
            x='Date:T',
            y=alt.Y('Volume:Q', title='Volume', axis=alt.Axis(format='~s'))
        ).properties(
            width=700,
            height=400,
            title=f"{tickerSymbol} Volume"
        )
        st.altair_chart(volume_chart, use_container_width=True)

        # Explanation for Volume Chart
        st.markdown("""
        🧾 **What does this chart show?**  
        This chart shows the *trading volume* of the stock each day.  
        - **Volume** means how many shares were traded on a given day.
        - Higher volume usually means more interest or activity in the stock.
        - You can use it to spot important events, like news or earnings.
        """)

       

except Exception as e:
    st.error(f"An error occurred: {e}")
