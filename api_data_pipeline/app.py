import streamlit as st
import requests
import pandas as pd
import sqlite3
from datetime import datetime

# App Title
st.title("💱 Live Currency Data Pipeline Dashboard")
st.write("Fetch, view, and store real-time currency exchange rates using an API.")

# Fetch Data
if st.button("Fetch Latest Data"):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        rates = pd.DataFrame(list(data['rates'].items()), columns=['Currency', 'Rate'])
        rates['Base'] = data['base']
        rates['Date'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        st.success("✅ Data fetched successfully!")
        st.dataframe(rates)

        # Save option
        if st.button("Save to Database"):
            conn = sqlite3.connect('exchange_data.db')
            rates.to_sql('exchange_rates', conn, if_exists='append', index=False)
            conn.close()
            st.info("💾 Data saved to SQLite database successfully!")

    else:
        st.error("Failed to fetch data. Please try again later.")

# Show stored data
if st.button("Show Stored Data"):
    try:
        conn = sqlite3.connect('exchange_data.db')
        stored_data = pd.read_sql("SELECT * FROM exchange_rates ORDER BY Date DESC LIMIT 50", conn)
        conn.close()
        st.dataframe(stored_data)
    except Exception as e:
        st.error("⚠️ No data found in database yet.")
