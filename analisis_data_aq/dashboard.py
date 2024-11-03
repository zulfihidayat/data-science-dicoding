import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
sns.set(style='dark')

file_aotizhongxin = 'df_Aotizhongxin_AQ.csv'
file_changping = 'df_Changping_AQ.csv'
df_aotizhongxin = pd.read_csv(file_aotizhongxin)
df_changping = pd.read_csv(file_changping)
df = pd.concat([df_aotizhongxin, df_changping])

df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

def create_daily_weather_df(df):
    daily_weather_df = df.resample('D', on='datetime').agg({
        "RAIN": "sum",
        "PM2.5": "mean",
        "PM10": "mean",
        "TEMP": "mean"
    }).reset_index()
    daily_weather_df.rename(columns={
        "RAIN": "total_rain",
        "PM2.5": "avg_pm2.5",
        "PM10": "avg_pm10",
        "TEMP": "avg_temp"
    }, inplace=True)
    return daily_weather_df

st.sidebar.image("kuncen-langit.png")

min_date, max_date = df['datetime'].min(), df['datetime'].max()
start_date, end_date = st.sidebar.date_input('Date Range', [min_date, max_date], min_value=min_date, max_value=max_date)
filtered_df = df[(df['datetime'] >= str(start_date)) & (df['datetime'] <= str(end_date))]

daily_weather_df = create_daily_weather_df(filtered_df)

st.header('Weather Data Dashboard')
st.subheader('Daily Weather Summary')

col1, col2 = st.columns(2)
with col1:
    total_rain = daily_weather_df['total_rain'].sum()
    st.metric("Total Rainfall", f"{total_rain} mm")

with col2:
    avg_pm2_5 = round(daily_weather_df['avg_pm2.5'].mean(), 2)
    avg_pm10 = round(daily_weather_df['avg_pm10'].mean(), 2)
    st.metric("Average PM2.5 and PM10", f"{avg_pm2_5} µg/m³, {avg_pm10} µg/m³")

st.subheader("Rainfall Over Time")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="datetime", y="total_rain", data=daily_weather_df, marker='o', ax=ax)
ax.set_title("Daily Rainfall")
ax.set_ylabel("Rain (mm)")
ax.set_xlabel("Date")
st.pyplot(fig)

st.subheader("PM2.5 Levels Over Time")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="datetime", y="avg_pm2.5", data=daily_weather_df, marker='o', color='orange', ax=ax)
ax.set_title("Daily PM2.5 Levels")
ax.set_ylabel("PM2.5 (µg/m³)")
ax.set_xlabel("Date")
st.pyplot(fig)

st.subheader("PM10 Levels Over Time")
fig, ax = plt.subplots(figsize=(16, 8))
sns.lineplot(x="datetime", y="avg_pm10", data=daily_weather_df, marker='o', color='green', ax=ax)
ax.set_title("Daily PM10 Levels")
ax.set_ylabel("PM10 (µg/m³)")
ax.set_xlabel("Date")
st.pyplot(fig)

st.caption('Weather Data Dashboard © 2023')
