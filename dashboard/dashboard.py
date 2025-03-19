import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Fungsi untuk memuat data
def load_data():
    day_df = pd.read_csv(r'./data/day.csv', parse_dates=['dteday'])
    hour_df = pd.read_csv(r'./data/hour.csv', parse_dates=['dteday'])
    combined_df = pd.merge(day_df, hour_df, on='dteday', suffixes=('_day', '_hour'))
    return day_df, hour_df, combined_df

day_df, hour_df, combined_df = load_data()

# Konfigurasi Dashboard
st.set_page_config(page_title="Dashboard Penggunaan Sepeda", layout="wide")
st.title("Dashboard Penggunaan Sepeda")

# Membuat sidebar
with st.sidebar:
    st.title("🚲 Proyek Analisis Data")
    st.subheader("Bike Sharing Dataset")
    st.write("**Nama:** Muh. Irsyad Asrori")
    st.write("**Email:** sastrojendro1119@gmail.com")
    st.write("**ID Dicoding:** sastrojendro1119")

# Legend untuk Kategori Cuaca
legend_labels = {
    1: "1: Cerah, Sedikit Awan",
    2: "2: Kabut + Berawan",
    3: "3: Salju Ringan/Hujan Ringan + Mendung",
    4: "4: Hujan Deras + Badai + Kabut"
}

handles = [
    plt.Line2D([], [], marker='o', linestyle='',
               markerfacecolor='gray', markersize=8,
               label=legend_labels[k])
    for k in sorted(legend_labels.keys())
]

# 1. Pengaruh Cuaca (Harian)
st.header("1. Pengaruh Cuaca terhadap Penggunaan Sepeda")

col1, col2 = st.columns(2)

with col1:
    st.subheader("a. Data Harian")
    fig_day, ax_day = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='weathersit_day', y='cnt_day', data=combined_df, ax=ax_day)
    ax_day.set_title('Pengaruh Cuaca terhadap Penggunaan Sepeda (Harian)')
    ax_day.set_xlabel('Kondisi Cuaca')
    ax_day.set_ylabel('Jumlah Penyewa Sepeda')
    ax_day.legend(handles=handles, title="Deskripsi Kondisi Cuaca",
                  loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    st.pyplot(fig_day)


# 2. Pengaruh Cuaca (Per Jam)
with col2:
    st.subheader("b. Data Per Jam")
    fig_hour, ax_hour = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='weathersit_hour', y='cnt_hour', data=combined_df, ax=ax_hour)
    ax_hour.set_title('Pengaruh Cuaca terhadap Penggunaan Sepeda (Per Jam)')
    ax_hour.set_xlabel('Kondisi Cuaca')
    ax_hour.set_ylabel('Jumlah Penyewa Sepeda')
    ax_hour.legend(handles=handles, title="Deskripsi Kondisi Cuaca",
                   loc="upper left", bbox_to_anchor=(1, 1))
    plt.tight_layout()
    st.pyplot(fig_hour)

# 3. Korelasi antara Variabel
st.header("2. Analisis Korelasi")
correlation_matrix = combined_df[['weathersit_day', 'cnt_day', 'weathersit_hour', 'cnt_hour']].corr()
st.write("**Matriks Korelasi:**")
st.dataframe(correlation_matrix)

fig_heatmap, ax_heatmap = plt.subplots(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax_heatmap)
ax_heatmap.set_title('Korelasi antara Cuaca dan Penggunaan Sepeda')
plt.tight_layout()
st.pyplot(fig_heatmap)

st.header("3. Tren dan Pola Penggunaan Sepeda")
col1, col2 = st.columns(2)

# 4. Tren Bulanan
with col1:
    st.subheader("a. Tren Bulanan Jumlah Penyewa Sepeda")
    monthly_trend = combined_df.groupby(combined_df['dteday'].dt.to_period('M'))['cnt_day'].sum()
    fig_monthly, ax_monthly = plt.subplots(figsize=(10, 6))
    ax_monthly.plot(monthly_trend.index.to_timestamp(), monthly_trend.values, marker='o')
    ax_monthly.set_xlabel('Bulan')
    ax_monthly.set_ylabel('Jumlah Penyewa Sepeda')
    ax_monthly.set_title('Tren Bulanan Jumlah Penyewa Sepeda')
    ax_monthly.grid(True)
    plt.tight_layout()
    st.pyplot(fig_monthly)

# 5. Tren Musiman
with col2:
    st.subheader("b. Tren Musiman Jumlah Penyewa Sepeda")
    seasonal_trend = combined_df.groupby('season_day')['cnt_day'].mean()
    fig_season, ax_season = plt.subplots(figsize=(10, 6))
    ax_season.bar(seasonal_trend.index, seasonal_trend.values, color='skyblue')
    ax_season.set_xlabel('Musim')
    ax_season.set_ylabel('Rata-rata Jumlah Penyewa Sepeda')
    ax_season.set_title('Tren Musiman Rata-Rata Jumlah Penyewa Sepeda')
    ax_season.set_xticks(seasonal_trend.index)
    ax_season.set_xticklabels(['Musim Semi', 'Musim Panas', 'Musim Gugur', 'Musim Digin'])
    ax_season.grid(axis='y')
    plt.tight_layout()
    st.pyplot(fig_season)

# 6. Dampak Hari Libur
st.header("4. Pengaruh Hari Libur")
holiday_impact = combined_df.groupby('holiday_day')['cnt_day'].mean()
fig_holiday, ax_holiday = plt.subplots(figsize=(8, 6))
ax_holiday.bar([0, 1], holiday_impact.values, color='lightgreen')
ax_holiday.set_ylabel('Rata-rata Jumlah Penyewa Sepeda')
ax_holiday.set_title('Pengaruh Hari Libur terhadap Penggunaan Sepeda')
ax_holiday.set_xticks([0, 1])
ax_holiday.set_xticklabels(['Hari Kerja', 'Hari Libur'])
ax_holiday.grid(True)
plt.tight_layout()
st.pyplot(fig_holiday)

st.markdown(
    """
    <div style="text-align: center; color: gray; font-size: 14px; padding-top: 20px;">
        🚴 <b>Bike Sharing Analysis</b> | Dibuat oleh <b>Muh. Irsyad Asrori</b> | 📧 sastrojendro1119@gmail.com <br>
        💡 <i>Powered by Streamlit</i>
    </div>
    """,
    unsafe_allow_html=True
)