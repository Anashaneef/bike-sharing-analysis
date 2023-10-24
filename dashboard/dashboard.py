import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Helper functions

def create_daily_orders_df(df):
    df['date'] = pd.to_datetime(df['date'])
    orders_df = df.resample('M', on='date').sum()
    return orders_df

def create_sum_casual_user_df(df):
    sum_casual_user_df = df.groupby("day").casual_user.sum().sort_values(ascending=False).reset_index()
    return sum_casual_user_df

def create_sum_registered_user_df(df):
    sum_registered_user_df = df.groupby("day").registered_user.sum().sort_values(ascending=False).reset_index()
    return sum_registered_user_df

def create_byweather_df(df):
    byweather_df = df.groupby("weather").total_user.sum().sort_values(ascending=False).reset_index()
    return byweather_df

def create_byseason_df(df):
    byseason_df = df.groupby("season").total_user.sum().sort_values(ascending=False).reset_index()
    return byseason_df

def create_rfm_df(df):
    rfm_df = day_df.groupby(by="day", as_index=False).agg({
        "date": "max",
        "instant": "nunique",
        "total_user": "sum"
    })
    rfm_df.columns = ["day", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date
    recent_date = day_df["date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(lambda x: (recent_date - x).days)
    rfm_df.drop("max_order_timestamp", axis=1, inplace=True)
    return rfm_df


# Prepare dataframe
day_df = pd.read_csv(".dashboard/day_clean.csv")

# Ensure the date column are of type datetime
datetime_columns = ["date"]
day_df.sort_values(by="date", inplace=True)
day_df.reset_index(inplace=True)
for column in datetime_columns:
    day_df[column] = pd.to_datetime(day_df[column])

# Create filter components
min_date = day_df["date"].min()
max_date = day_df["date"].max()

with st.sidebar:
    # Adding a company logo
    st.image("./logo.png")

    # Retrieve start_date & end_date from date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["date"] >= str(start_date)) &
                (day_df["date"] <= str(end_date))]

daily_orders_df = create_daily_orders_df(main_df)
sum_casual_user_df = create_sum_casual_user_df(main_df)
sum_registered_user_df = create_sum_registered_user_df(main_df)
byweather_df = create_byweather_df(main_df)
byseason_df = create_byseason_df(main_df)
rfm_df = create_rfm_df(main_df)

# Create dashboard
st.header('Capital Bike Share Dashboard :sparkles:')

# Daily Users
st.subheader('Daily Users')
col1, col2, col3 = st.columns(3)

with col1:
    total_casual = daily_orders_df.casual_user.sum()
    st.metric("Total Casual User", value=f'{total_casual:,}')

with col2:
    total_registered = daily_orders_df.registered_user.sum()
    st.metric("Total Registered User", value=f'{total_registered:,}')

with col3:
    total_users = daily_orders_df.total_user.sum()
    st.metric("Total Users", value=f'{total_users:,}')

plt.figure(figsize=(10, 6))
plt.plot(daily_orders_df.index, daily_orders_df['total_user'], color='#A5C0DD')
plt.xlabel(None)
plt.ylabel(None)
plt.title('Number of Users')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt)

# Number of Casual Users and Registered Users by Day
st.subheader("Number of Casual Users and Registered Users by Day")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="casual_user", y="day", data=sum_casual_user_df, palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Casual User", loc="center", fontsize=50)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=30, rotation=45)

sns.barplot(x="registered_user", y="day", data=sum_registered_user_df, palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Registered User", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis ='x', labelsize=30, rotation=-45)

st.pyplot(fig)

# The Effect of Weather and Season on Bike Sharing Productivity
st.subheader("Number of Users by Weather and Season")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))
sns.barplot(y="total_user", x="weather", data=byweather_df.sort_values(by="total_user", ascending=False), palette=colors, ax=ax[0])
ax[0].set_title("Number of User by Weather", loc="center", fontsize=50)
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].tick_params(axis ='y', labelsize=30)
ax[0].tick_params(axis ='x', labelsize=30)
ax[0].ticklabel_format(style='plain', axis='y')

sns.barplot(y="total_user", x="season", data=byseason_df.sort_values(by="total_user", ascending=False), palette=colors, ax=ax[1])
ax[1].set_title("Number of User by Season", loc="center", fontsize=50)
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=30)
ax[1].tick_params(axis ='x', labelsize=30)
ax[1].ticklabel_format(style='plain', axis='y')

st.pyplot(fig)

# RFM Analysis
st.subheader("Best Customer Based on RFM Parameters (day)")
col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df.recency.mean(), 1)
    st.metric("Average Recency (days)", value=avg_recency)

with col2:
    avg_frequency = round(rfm_df.frequency.mean(), 2)
    st.metric("Average Frequency", value=avg_frequency)

with col3:
    avg_frequency = format_currency(rfm_df.monetary.mean(), "AUD", locale='es_CO') 
    st.metric("Average Monetary", value=avg_frequency)

fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(35, 15))
colors = ["#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9", "#90CAF9"]

sns.barplot(y="recency", x="day", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("By Recency (days)", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=25)
ax[0].tick_params(axis ='x', labelsize=30, rotation=45)

sns.barplot(y="frequency", x="day", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("By Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=25)
ax[1].tick_params(axis='x', labelsize=30, rotation=45)

sns.barplot(y="monetary", x="day", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("By Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=25)
ax[2].tick_params(axis='x', labelsize=30, rotation=45)

st.pyplot(fig)

st.caption(f"Copyright © 2023 All Rights Reserved [Anas Fikri Hanif](https://www.linkedin.com/in/anashaneef/)")
