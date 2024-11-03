import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

df_aotizhongxin = pd.read_csv("df_Aotizhongxin_AQ.csv")
df_changping = pd.read_csv("df_Changping_AQ.csv")

df = pd.concat([df_aotizhongxin, df_changping])

df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])

st.title('Weather and Air Quality Analysis Dashboard')
st.sidebar.image("kuncen-langit.png")

st.sidebar.header("Filter by Date")
min_date, max_date = df['datetime'].min(), df['datetime'].max()
start_date, end_date = st.sidebar.date_input('Select Date Range', [min_date, max_date], min_value=min_date, max_value=max_date)

filtered_df = df[(df['datetime'] >= pd.to_datetime(start_date)) & (df['datetime'] <= pd.to_datetime(end_date))]

st.header('Correlation Analysis of Meteorological Parameters')
meteorological_params = ['RAIN', 'TEMP', 'PRES', 'DEWP', 'WSPM']
correlation_meteorological = filtered_df[meteorological_params].corr()

fig, ax = plt.subplots()
sns.heatmap(correlation_meteorological, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix of Meteorological Parameters')
st.pyplot(fig)

st.header('Correlation Analysis of PM2.5 with Gas Compounds')
pm2_5_gas_compounds = ['PM2.5', 'SO2', 'NO2', 'CO', 'O3']
correlation_pm2_5 = filtered_df[pm2_5_gas_compounds].corr()

fig, ax = plt.subplots()
sns.heatmap(correlation_pm2_5, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix of PM2.5 and Gas Compounds')
st.pyplot(fig)

st.header('Correlation Analysis of PM10 with Gas Compounds')
pm10_gas_compounds = ['PM10', 'SO2', 'NO2', 'CO', 'O3']
correlation_pm10 = filtered_df[pm10_gas_compounds].corr()

fig, ax = plt.subplots()
sns.heatmap(correlation_pm10, annot=True, cmap='coolwarm', ax=ax)
ax.set_title('Correlation Matrix of PM10 and Gas Compounds')
st.pyplot(fig)

st.header('Trend Analysis of PM2.5')
daily_trends_pm25 = filtered_df.resample('D', on='datetime').agg({'PM2.5': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='datetime', y='PM2.5', data=daily_trends_pm25, marker='o', color='blue')
ax.set_title('Daily Average Concentration of PM2.5')
ax.set_ylabel('Concentration (µg/m³)')
ax.set_xlabel('Date')
st.pyplot(fig)

st.header('Trend Analysis of PM10')
daily_trends_pm10 = filtered_df.resample('D', on='datetime').agg({'PM10': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='datetime', y='PM10', data=daily_trends_pm10, marker='o', color='orange')
ax.set_title('Daily Average Concentration of PM10')
ax.set_ylabel('Concentration (µg/m³)')
ax.set_xlabel('Date')
st.pyplot(fig)

st.header('Trend Analysis of Rainfall')
daily_trends_rain = filtered_df.resample('D', on='datetime').agg({'RAIN': 'sum'}).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='datetime', y='RAIN', data=daily_trends_rain, marker='o', color='green')
ax.set_title('Daily Total Rainfall')
ax.set_ylabel('Rainfall (mm)')
ax.set_xlabel('Date')
st.pyplot(fig)

st.header('Distribution of PM2.5 and PM10')
fig, ax = plt.subplots(2, 1, figsize=(10, 15))

sns.histplot(filtered_df['PM2.5'], bins=30, kde=True, ax=ax[0], color='blue')
ax[0].set_title('Distribution of PM2.5')
ax[0].set_xlabel('PM2.5 (µg/m³)')
ax[0].set_ylabel('Frequency')

sns.histplot(filtered_df['PM10'], bins=30, kde=True, ax=ax[1], color='orange')
ax[1].set_title('Distribution of PM10')
ax[1].set_xlabel('PM10 (µg/m³)')
ax[1].set_ylabel('Frequency')

st.pyplot(fig)

st.caption('Weather and Air Quality Data Analysis © 2024 - by zulfihidayat')
