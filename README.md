# Dashboard Penggunaan Sepeda

Dashboard ini merupakan aplikasi analisis data *Bike Sharing* menggunakan **Streamlit**, **pandas**, **seaborn**, dan **matplotlib**. Aplikasi ini memvisualisasikan pengaruh cuaca, tren penggunaan, serta dampak hari libur terhadap jumlah penyewa sepeda.
## Fitur Utama
- **Analisis Cuaca:**  
  Menampilkan boxplot untuk data harian dan per jam berdasarkan kondisi cuaca.
  
- **Korelasi:**  
  Menampilkan matriks korelasi dan heatmap antara variabel cuaca dan jumlah penyewa.

- **Tren Penggunaan:**  
  Visualisasi tren bulanan dan musiman dari jumlah penyewa sepeda.

- **Dampak Hari Libur:**  
  Membandingkan rata-rata jumlah penyewa antara hari kerja dan hari libur.

## Data

Dataset yang digunakan berasal dari dua file:
- `day.csv`: Data harian penggunaan sepeda.
- `hour.csv`: Data per jam penggunaan sepeda.
## Teknologi yang Digunakan

- **Python Libraries:**
  - [Streamlit](https://streamlit.io/)
  - [pandas](https://pandas.pydata.org/)
  - [seaborn](https://seaborn.pydata.org/)
  - [matplotlib](https://matplotlib.org/)
- **Visualization Features:**
  - Diagram garis, *boxplot*, diagram batang, dan *heatmap*.

## Instalasi dan Penggunaan

1. **Clone repositori:**
   ```bash
   git clone <link-repo-anda>
   cd <nama-folder>

2. **Buat virtual environment**
     ```bash
     pip install pipenv
     pipenv shell

3. **Install dependensi:**
   ```bash
    pip install -r requirements.txt

4. **Jalankan aplikasi:**
   ```bash
    streamlit run <nama_file_script_anda>.py
