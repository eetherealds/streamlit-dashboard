import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#berisi informasi tentang penyewaan sepeda berdasarkan hari dan jam

day_df = pd.read_csv("day.csv")
hour_df = pd.read_csv("hour.csv")

#membuat sidebar untuk memilih dataset
st.sidebar.title("📊 Dashboard Data Analysis")
page = st.sidebar.radio("📌 Pilih Dataset", ["Harian", "Jam"])

#menampilkan judul utama dashboard
st.title("🚴‍♂️ Dashboard Analisis Data Penyewaan Sepeda")

#memilih dataset harian 
if page == "Harian":
    #menampilkan subset dari dataset harian
    st.subheader("📆 Dataset Harian")
    st.write(day_df.head())
    
    #menampilkan plot regresi antara suhu dan total penyewaan sepeda
    st.subheader("🌞 Hubungan Suhu vs Total Penyewaan Sepeda")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(x='temp', y='cnt', data=day_df, scatter_kws={'alpha': 0.3}, ax=ax)
    ax.set_title("Hubungan Suhu vs Total Penyewaan Sepeda", fontsize=14)
    ax.set_xlabel("Suhu", fontsize=12)
    ax.set_ylabel("Total Penyewaan Sepeda", fontsize=12)
    st.pyplot(fig)
    
    #spasi antar gambar
    st.markdown("<br>", unsafe_allow_html=True)
    
    #menghitung dan menampilkan korelasi Pearson antara suhu dan jumlah penyewaan sepeda
    correlation_day = day_df[['temp', 'cnt']].corr().iloc[0, 1]
    st.write(f"📈 **Korelasi Pearson:** {correlation_day:.2f}")

#memilih dataset jam
elif page == "Jam":
    #menampilkan subset dari dataset jam
    st.subheader("⏰ Dataset Jam")
    st.write(hour_df.head())
    
    #mengelompokkan data berdasarkan hari kerja dan akhir pekan
    hour_df['day_type'] = np.where(hour_df['workingday'] == 1, '🏢 Weekday', '🏖️ Weekend')
    day_comparison_hour = hour_df.groupby('day_type')['cnt'].mean().reset_index()
    
    #menampilkan perbandingan penyewaan sepeda antara hari kerja dan akhir pekan
    st.subheader("📊 Distribusi Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='day_type', y='cnt', data=day_comparison_hour, hue='day_type', legend=False, ax=ax)
    ax.set_title("Distribusi Penyewaan Sepeda antara Hari Kerja vs Akhir Pekan", fontsize=14)
    ax.set_xlabel("Kategori Hari", fontsize=12)
    ax.set_ylabel("Rata-rata Penyewaan", fontsize=12)
    st.pyplot(fig)
    
    #spasi antar gambar
    st.markdown("<br>", unsafe_allow_html=True)
    
    #mengelompokkan penyewaan sepeda berdasarkan jam
    time_cluster = hour_df.groupby('hr')['cnt'].sum().reset_index()
    time_cluster['Usage_Category'] = pd.cut(time_cluster['cnt'], bins=3, labels=['🟢 Rendah', '🟡 Sedang', '🔴 Tinggi'])
    
    #menampilkan clustering penyewaan sepeda berdasarkan jam
    st.subheader("⏳ Clustering Penyewaan Sepeda Berdasarkan Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x='hr', y='cnt', hue='Usage_Category', data=time_cluster, palette='viridis', ax=ax)
    ax.set_title("⏰ Clustering Penyewaan Sepeda Berdasarkan Jam")
    ax.set_xlabel("Jam")
    ax.set_ylabel("Total Penyewaan")
    ax.legend(title="Kategori Penggunaan")
    st.pyplot(fig)

#foter
st.markdown("---")
st.markdown("Dearni Lambardo Saragih MC-37")