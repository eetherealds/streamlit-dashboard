import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_day = pd.read_csv("day.csv")
df_hour = pd.read_csv("hour.csv")

#konversi kolom tanggal ke format datetime supaya mudah difilter
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])

#mapping angka season dan weathersit ke dalam bentuk emoji
season_mapping = {1: "🌸 Spring", 2: "☀️ Summer", 3: "🍂 Fall", 4: "❄️ Winter"}
weathersit_mapping = {1: "☀️ Clear/Few clouds", 2: "🌫️ Mist/Cloudy", 3: "🌨️ Light Snow/Rain", 4: "⛈️ Heavy Rain/Ice"}

df_day['season'] = df_day['season'].map(season_mapping)
df_hour['season'] = df_hour['season'].map(season_mapping)
df_day['weathersit'] = df_day['weathersit'].map(weathersit_mapping)
df_hour['weathersit'] = df_hour['weathersit'].map(weathersit_mapping)

#sidebar untuk filter data
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("📅 Pilih tanggal awal", df_day['dteday'].min())
end_date = st.sidebar.date_input("📅 Pilih tanggal akhir", df_day['dteday'].max())

#filtering berdasarkan musim dan cuaca
season_options = df_day['season'].dropna().unique()
selected_season = st.sidebar.multiselect("🍁 Pilih Musim", season_options, default=[])
weathersit_options = df_day['weathersit'].dropna().unique()
selected_weathersit = st.sidebar.multiselect("🌦️ Pilih Kondisi Cuaca", weathersit_options, default=[])

#filter dataset
filtered_df_day = df_day[(df_day['dteday'] >= pd.to_datetime(start_date)) & (df_day['dteday'] <= pd.to_datetime(end_date))]
filtered_df_hour = df_hour[(df_hour['dteday'] >= pd.to_datetime(start_date)) & (df_hour['dteday'] <= pd.to_datetime(end_date))]

if selected_season:
    filtered_df_day = filtered_df_day[filtered_df_day['season'].isin(selected_season)]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['season'].isin(selected_season)]

if selected_weathersit:
    filtered_df_day = filtered_df_day[filtered_df_day['weathersit'].isin(selected_weathersit)]
    filtered_df_hour = filtered_df_hour[filtered_df_hour['weathersit'].isin(selected_weathersit)]

st.title("Dashboard Analisis Data Penyewaan Sepeda")

if not filtered_df_day.empty:
    #grafik hubungan suhu dengan jumlah penyewaan sepeda 
    st.subheader("🌡️ Hubungan Suhu vs Total Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.regplot(x='temp', y='cnt', data=filtered_df_day, scatter_kws={'alpha':0.3}, ax=ax)
    ax.set_title('Hubungan Suhu vs Total Penyewaan Sepeda', fontsize=14)
    ax.set_xlabel('Suhu', fontsize=12)
    ax.set_ylabel('Total Penyewaan Sepeda', fontsize=12)
    st.pyplot(fig)

    #menentukan apakah hari tersebut weekday atau weekend
    filtered_df_hour['day_type'] = np.where(filtered_df_hour['workingday'] == 1, '📅 Weekday', '🎉 Weekend')

    #menghitung rata-rata penyewaan sepeda 
    day_comparison_hour = filtered_df_hour.groupby('day_type', as_index=False)['cnt'].mean()

    #grafik perbandingan weekday vs weekend
    st.subheader("📅 Distribusi Penyewaan Sepeda antara Hari Kerja vs Akhir Pekan")
    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x='day_type', y='cnt', data=day_comparison_hour, hue='day_type', legend=False, ax=ax, palette=['#1f77b4', '#1f77b4'])
    ax.set_title('Distribusi Penyewaan Sepeda antara Hari Kerja vs Akhir Pekan', fontsize=14)
    ax.set_xlabel('Kategori Hari', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    #mengelompokkan penyewaan sepeda berdasarkan jam
    time_cluster = filtered_df_hour.groupby('hr', observed=True)['cnt'].sum().reset_index()

    if not time_cluster.empty:

        #mengkategorikan penggunaan berdasarkan jumlah penyewaan
        time_cluster['Usage_Category'] = pd.cut(time_cluster['cnt'], bins=3, labels=['🔴 Rendah', '🟡 Sedang', '🟢 Tinggi'])

        #grafik penyewaan sepeda berdasarkan jam
        st.subheader("⏰ Clustering Penyewaan Sepeda Berdasarkan Jam")
        fig, ax = plt.subplots(figsize=(10,5))
        sns.barplot(x='hr', y='cnt', hue='Usage_Category', data=time_cluster, palette='viridis', ax=ax)
        ax.set_title("Clustering Penyewaan Sepeda Berdasarkan Jam", fontsize=14)
        ax.set_xlabel("Jam", fontsize=12)
        ax.set_ylabel("Total Penyewaan", fontsize=12)
        ax.set_xticks(range(0, 24, 1))
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.legend(title="Kategori Penggunaan")
        st.pyplot(fig)
else:
    st.write("🚫 **Tidak ada data yang tersedia untuk filter yang dipilih.**")

#footer
st.markdown("---")
st.markdown("By: Dearni Lambardo Saragih MC-37")
