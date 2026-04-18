# E-Commerce Data Analysis Project 🛍️

Proyek ini merupakan analisis data publik e-commerce untuk memahami performa penjualan, demografi pelanggan, dan perilaku belanja berdasarkan parameter RFM (Recency, Frequency, Monetary).

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```
## Setup Environment - Shell/Terminal
```
cd submission
pip install -r requirements.txt
```

## Run Streamlit App
```
streamlit run dashboard/dashboard.py
```
## Struktur Project
```
submission/
├── dashboard/
│   ├── main_data.csv        # Dataset yang telah dibersihkan untuk dashboard
│   └── dashboard.py         # Script aplikasi Streamlit
├── data/
│   ├── customers_dataset.csv          
│   └── geolocation_dataset.csv
│   └── ...                  # File dataset
├── notebook.ipynb           # Analisis data lengkap (Wrangling, EDA, Visualization)
├── README.md                # Dokumentasi proyek
├── requirements.txt         # Daftar library Python yang dibutuhkan
└── url.txt                  # Tautan dashboard yang telah dideploy
```

## Fitur Dashboard
1. Filter Rentang Waktu: Pengguna dapat memilih periode data yang ingin dianalisis melalui sidebar.<br/>
2. Metrik Utama: Menampilkan Total Revenue dan Total Orders secara dinamis.<br/>
3. Analisis Produk: Menampilkan Top 5 kategori produk dengan pendapatan tertinggi.<br/>
4. Tren Penjualan: Grafik garis yang menunjukkan fluktuasi pendapatan bulanan.<br/>
5. Demografi & Karakteristik: Analisis nilai transaksi per wilayah dan sebaran perilaku belanja pelanggan.<br/>
6. Segmentasi RFM: Klasifikasi pelanggan menjadi Recent, Repeat, dan One-time Customer.<br/>

## Dependencies
1. matplotlib<br/>
2. pandas<br/>
3. seaborn<br/>
4. streamlit<br/>

## Copyright (c) 2026 - Richard Liestianto
