# 1. Instalasi Awal
pastikan kamu sudah punya Python 3.7+. Kalau belum, install dulu dengan perintah ini:

```
pip install streamlit pandas seaborn matplotlib numpy
```

# 2. Menjalankan Dashboard di Komputer Sendiri
1. Download atau clone proyek ini:
    ```
   git clone https://github.com/username/repository-name.git
   cd repository-name
   ```

2. Jalankan aplikasi Streamlit dengan perintah ini:
   ```
   streamlit run dashboard.py
   ```

3. Kalau sudah jalan, buka browser dan akses http://localhost:8501 buat lihat dashboard.

# Data yang Digunakan
Dashboard ini pakai dataset dalam bentuk file CSV (`day.csv` dan `hour.csv`). Pastikan kedua file ini ada di folder proyek sebelum menjalankan aplikasinya.

---

# Cara Menjalankan di Streamlit Cloud
Kalau mau menjalankan dashboard ini di Streamlit Cloud, ikuti langkah-langkah berikut:

1. Buat file `requirements.txt` dan tambahkan daftar berikut:
   ```
   matplotlib==3.10.1
   numpy==2.2.3
   pandas==2.2.3
   seaborn==0.13.2
   streamlit==1.42.2
   ```

2. Upload proyek ke GitHub, lalu deploy di [Streamlit Cloud](https://share.streamlit.io/).

3. Kalau ada perubahan kode, cukup update repositori GitHub dan restart aplikasi di Streamlit Cloud.

---
