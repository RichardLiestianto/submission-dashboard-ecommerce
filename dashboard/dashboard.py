import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Konfigurasi gaya visualisasi
sns.set(style='darkgrid')

# 1. Load Data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    return df

all_df = load_data()

# 2. Menyiapkan Komponen Sidebar (Filter)
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()

with st.sidebar:
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter dataframe berdasarkan tanggal yang dipilih
main_df = all_df[(all_df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# --- HEADER ---
st.header('E-Commerce Data Dashboard 🛍️')
st.markdown(f"**Periode Analisis:** {start_date} hingga {end_date}")

# --- PERTANYAAN 1: REVENUE & TREND ---
st.subheader('Product Performance & Sales Trend')

col1, col2 = st.columns(2)

with col1:
    total_revenue = main_df.price.sum()
    st.metric("Total Revenue", value=f"R$ {total_revenue:,.2f}")

with col2:
    total_orders = main_df.order_id.nunique()
    st.metric("Total Orders", value=total_orders)

# Plot 1: Top 5 Categories
fig, ax = plt.subplots(figsize=(10, 5))
product_revenue_df = main_df.groupby("product_category_name_english").price.sum().sort_values(ascending=False).head(5).reset_index()
sns.barplot(x="price", y="product_category_name_english", data=product_revenue_df, palette="viridis", hue="product_category_name_english", legend=False, ax=ax)
ax.set_title(f"Top 5 Kategori Produk Berdasarkan Pendapatan", fontsize=15)
ax.set_xlabel("Total Revenue (R$)")
ax.set_ylabel(None)
st.pyplot(fig)

# Plot 2: Monthly Revenue Trend
st.write(f"#### Tren Pendapatan Bulanan")
fig, ax = plt.subplots(figsize=(15, 6))

# Menyiapkan data tren bulanan dari main_df (yang sudah difilter sidebar)
monthly_orders_df = main_df.resample(rule='ME', on='order_purchase_timestamp').agg({
    "price": "sum"
})

# Ubah format tanggal untuk tampilan di grafik
monthly_orders_df.index = monthly_orders_df.index.strftime('%B %Y')
monthly_orders_df = monthly_orders_df.reset_index()

# Membuat Line Chart
ax.plot(
    monthly_orders_df["order_purchase_timestamp"], 
    monthly_orders_df["price"], 
    marker='o', 
    linewidth=2, 
    color="#72BCD4"
)

# Pengaturan tampilan
plt.xticks(rotation=45, fontsize=10)
ax.set_title(f"Tren Pendapatan Bulanan ({start_date} - {end_date})", fontsize=15)
ax.set_ylabel("Total Revenue (R$)")
ax.set_xlabel(None)

st.pyplot(fig)

# --- PERTANYAAN 2: GEOGRAPHY ---
st.subheader('Customer Geography & Characteristics')

# Plot 1: Bar Chart Negara Bagian
fig, ax = plt.subplots(figsize=(12, 6))
state_monetary_df = main_df.groupby("customer_state").price.sum().sort_values(ascending=False).head(10).reset_index()
sns.barplot(x="price", y="customer_state", data=state_monetary_df, palette="magma", hue="customer_state", legend=False, ax=ax)
ax.set_title(f"Top 10 State dengan Nilai Transaksi Terbesar", fontsize=15)
ax.set_xlabel("Total Monetary (R$)")
ax.set_ylabel("State")
st.pyplot(fig)

# Plot 2: Scatter Plot Karakteristik Pelanggan
st.write(f"#### Customer Characteristics: Frequency vs Monetary (SP, RJ, MG)")
fig, ax = plt.subplots(figsize=(10, 6))

# Menyiapkan data karakteristik (Frekuensi vs Monetary)
top_states = ["SP", "RJ", "MG"]
state_characteristics = main_df[main_df['customer_state'].isin(top_states)].groupby("customer_unique_id").agg({
    "order_id": "nunique",
    "price": "sum"
}).reset_index()

# Membuat Scatter Plot menggunakan objek ax
sns.scatterplot(
    x="order_id", 
    y="price", 
    data=state_characteristics, 
    alpha=0.5, 
    color="teal", 
    ax=ax
)

# Menambahkan judul dan label sumbu
ax.set_title(f"Karakteristik Frekuensi vs Nilai Transaksi Pelanggan\nPeriode: {start_date} - {end_date}", fontsize=14)
ax.set_xlabel("Frekuensi Pembelian (Order Count)")
ax.set_ylabel("Total Pengeluaran (Monetary)")

st.pyplot(fig)

# --- ANALISIS LANJUTAN: RFM ---
st.subheader('Segmentasi Pelanggan (RFM Analysis)')
st.write("*(Catatan: Analisis segmentasi RFM dihitung menggunakan keseluruhan data historis pelanggan)*")

# MENGGUNAKAN ALL_DF (Data Keseluruhan) UNTUK RFM
now = all_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
rfm_df = all_df.groupby(by="customer_unique_id", as_index=False).agg({
    "order_purchase_timestamp": lambda x: (now - x.max()).days,
    "order_id": "nunique",
    "price": "sum"
})
rfm_df.columns = ["customer_id", "recency", "frequency", "monetary"]

# Segmentasi
def segment_customer(df):
    if df['frequency'] > 1: return 'Repeat Customer'
    elif df['recency'] < 30: return 'Recent Customer'
    else: return 'One-time Customer'

rfm_df['segment'] = rfm_df.apply(segment_customer, axis=1)
segment_counts = rfm_df['segment'].value_counts().reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='count', y='segment', data=segment_counts, palette='viridis', hue='segment', legend=False, ax=ax)
ax.set_title('Segmentasi Pelanggan Berdasarkan Perilaku RFM\n(Keseluruhan Periode Operasional)', fontsize=15)
ax.set_xlabel('Jumlah Pelanggan')
ax.set_ylabel(None)
st.pyplot(fig)

st.caption('Copyright (c) 2026 - Richard Liestianto')