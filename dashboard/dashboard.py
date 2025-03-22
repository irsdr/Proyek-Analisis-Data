import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Rental Sepeda", layout="wide")

# Load dataset
def load_data():
    day_df = pd.read_csv('./data/day.csv')
    hour_df = pd.read_csv('./data/hour.csv')

    # Konversi format datetime
    day_df["dteday"] = pd.to_datetime(day_df["dteday"])
    hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

    # Mengubah kategori
    nama_musim = {1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'}
    day_df["season"].replace(nama_musim, inplace=True)
    hour_df["season"].replace(nama_musim, inplace=True)

    nama_bulan = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun', 7: 'Jul', 8: 'Agu', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'}
    day_df["mnth"].replace(nama_bulan, inplace=True)
    hour_df["mnth"].replace(nama_bulan, inplace=True)

    kondisi_cuaca = {1: 'Cerah', 2: 'Berkabut', 3: 'Hujan/Salju Ringan', 4: 'Hujan/Salju Lebat'}
    day_df["weathersit"].replace(kondisi_cuaca, inplace=True)
    hour_df["weathersit"].replace(kondisi_cuaca, inplace=True)

    nama_hari = {0: 'Minggu', 1: 'Senin', 2: 'Selasa', 3: 'Rabu', 4: 'Kamis', 5: 'Jumat', 6: 'Sabtu'}
    day_df["weekday"].replace(nama_hari, inplace=True)
    hour_df["weekday"].replace(nama_hari, inplace=True)

    day_df["yr"].replace({0: "2011", 1: "2012"}, inplace=True)
    hour_df["yr"].replace({0: "2011", 1: "2012"}, inplace=True)

    return day_df, hour_df

day_df, hour_df = load_data()

# Sidebar - Filter Data
st.sidebar.header("Filter Data")

# Menambahkan opsi "Semua Tahun" dalam selectbox
year_options = ["Semua Tahun", "2011", "2012"]
selected_year = st.sidebar.selectbox("Pilih Tahun", options=year_options)

# Multi-select untuk memilih lebih dari satu musim
season_options = ["Musim Semi", "Musim Panas", "Musim Gugur", "Musim Dingin"]
selected_seasons = st.sidebar.multiselect("Pilih Musim", options=season_options, default=season_options)

# Filter dataset berdasarkan tahun
if selected_year == "Semua Tahun":
    filtered_data = day_df  # Tidak ada filter tahun, ambil semua data
else:
    filtered_data = day_df[day_df["yr"] == selected_year]

# Filter berdasarkan musim
if selected_seasons:
    filtered_data = filtered_data[filtered_data["season"].isin(selected_seasons)]
    
# Dashboard Utama
st.title("📊 Dashboard Rental Sepeda")

# Ringkasan Data
col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", filtered_data["cnt"].sum())
col2.metric("Rata-rata Harian", round(filtered_data["cnt"].mean(), 2))
col3.metric("Hari dengan Penyewaan Tertinggi", filtered_data["cnt"].max())

# Tren Penyewaan Sepeda per Bulan
st.subheader("📈 Tren Penyewaan Sepeda per Bulan")
monthly_df = filtered_data.groupby("mnth")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(10,5))
sns.lineplot(x="mnth", y="cnt", data=monthly_df, marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_title(f"Tren Penyewaan Sepeda ({selected_year})")
ax.grid(True, linestyle="-", alpha=0.6)
st.pyplot(fig)

# Rata-rata Penggunaan Sepeda per Jam
st.subheader("⏰ Rata-rata Penyewaan Sepeda per Jam")
hourly_avg = hour_df.groupby("hr")[["casual", "registered", "cnt"]].mean()

fig, ax = plt.subplots(figsize=(12,6))
sns.lineplot(x=hourly_avg.index, y=hourly_avg["casual"], label="Casual", marker="o", ax=ax)
sns.lineplot(x=hourly_avg.index, y=hourly_avg["registered"], label="Registered", marker="s", ax=ax)
sns.lineplot(x=hourly_avg.index, y=hourly_avg["cnt"], label="Total", marker="d", linestyle="--", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Rata-rata Penyewaan Sepeda per Jam")
ax.grid(True, linestyle="-", alpha=0.6)
st.pyplot(fig)

col1, col2 = st.columns(2)

with col1:
    # Pengaruh Musim terhadap Penyewaan
    st.subheader("🌦️ Pengaruh Musim terhadap Penyewaan Sepeda")
    season_avg = filtered_data.groupby("season")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x="season", y="cnt", data=season_avg, palette="coolwarm", ax=ax)
    ax.set_xlabel("Musim")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title(f"Rata-rata Penyewaan Sepeda Berdasarkan Musim ({selected_year})")
    ax.set_axisbelow(True)
    ax.grid(True, linestyle="-", alpha=0.6)
    st.pyplot(fig)

with col2:
    # Pengaruh Cuaca terhadap Penyewaan
    st.subheader("🌤️ Pengaruh Cuaca terhadap Penyewaan Sepeda")

    filtered_weather_data = filtered_data.groupby("weathersit")["cnt"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x="weathersit", y="cnt", data=filtered_weather_data, palette="coolwarm", ax=ax)
    ax.set_xlabel("Kondisi Cuaca")
    ax.set_ylabel("Rata-rata Penyewaan Sepeda")
    ax.set_title(f"Rata-rata Penyewaan Sepeda Berdasarkan Cuaca ({selected_year})")
    ax.set_axisbelow(True)
    ax.grid(True, linestyle="-", alpha=0.6)
    st.pyplot(fig)

# Perbandingan Pengguna Casual vs Registered
st.subheader("👥 Perbandingan Pengguna Casual vs Registered")
user_data = filtered_data[["casual", "registered"]].sum()

fig, ax = plt.subplots(figsize=(6,6))
ax.pie(user_data, labels=["Casual", "Registered"], autopct="%1.1f%%", colors=["#7982B9", "#B3D1EF"], startangle=140, explode=(0.1, 0))
ax.set_title(f"Perbandingan Total Pengguna ({selected_seasons}) ({selected_year})")
st.pyplot(fig)

# Clustering Berdasarkan Jam Penyewaan
st.subheader("⏳ Clustering Berdasarkan Jam Penyewaan")
def categorize_hour(hr):
    if 0 <= hr < 6:
        return "Dini Hari"
    elif 6 <= hr < 12:
        return "Pagi"
    elif 12 <= hr < 18:
        return "Siang"
    else:
        return "Malam"

hour_df["time_category"] = hour_df["hr"].apply(categorize_hour)
time_segmentation = hour_df.groupby("time_category")["cnt"].mean().reset_index()

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="time_category", y="cnt", data=time_segmentation, palette="coolwarm", ax=ax)
ax.set_xlabel("Kategori Waktu")
ax.set_ylabel("Rata-rata Penyewaan Sepeda")
ax.set_title("Clustering Berdasarkan Jam Penyewaan")
ax.set_axisbelow(True)
ax.grid(True, linestyle="-", alpha=0.6)
st.pyplot(fig)

st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 14px; padding-top: 20px;">
        🚴 <b>Bike Sharing Analysis</b> | Dibuat oleh <b>Muh. Irsyad Asrori</b> | 📧 sastrojendro1119@gmail.com <br>
        💡 <i>Powered by Streamlit</i>
    </div>
    """,
    unsafe_allow_html=True
)