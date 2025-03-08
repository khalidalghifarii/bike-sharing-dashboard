# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk visualisasi dan analisis dataset Bike Sharing. Dashboard ini menampilkan analisis tentang penyewaan sepeda berdasarkan kondisi cuaca, musim, dan waktu.

## Pengembang

- **Nama:** Muhammad Khalid Al Ghifari
- **Email:** alghi.bna@gmail.com
- **ID Dicoding:** MC322D5Y2203

## Setup Environment - Shell/Terminal

```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App

```
streamlit run dashboard.py
```

## Struktur File

- `dashboard.py` - File utama aplikasi Streamlit
- `day.csv` - Dataset penyewaan sepeda harian
- `hour.csv` - Dataset penyewaan sepeda per jam
- `requirements.txt` - Daftar library yang diperlukan

## Fitur Dashboard

1. **Pengaruh Kondisi Cuaca**

   - Visualisasi distribusi penyewaan berdasarkan kondisi cuaca
   - Analisis korelasi antara faktor cuaca dan jumlah penyewaan
   - Fitur interaktif untuk memfilter berdasarkan rentang temperatur

2. **Pola Penggunaan Berdasarkan Waktu**

   - Analisis pola penggunaan sepeda sepanjang hari
   - Perbandingan pola penyewaan hari kerja vs akhir pekan
   - Distribusi penyewaan berdasarkan musim

3. **Analisis Lanjutan**
   - Kategorisasi penggunaan sepeda (Low, Moderate, High Usage)
   - Distribusi kategori penggunaan berdasarkan musim dan cuaca

## Dependencies

- pandas==2.0.3
- numpy==1.24.3
- matplotlib==3.7.2
- seaborn==0.12.2
- streamlit==1.29.0

## Cara Kontribusi

1. Fork repository ini
2. Buat branch baru (`git checkout -b feature/fiturBaru`)
3. Commit perubahan Anda (`git commit -m 'Menambahkan fitur baru'`)
4. Push ke branch tersebut (`git push origin feature/fiturBaru`)
5. Buat Pull Request baru

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE)
