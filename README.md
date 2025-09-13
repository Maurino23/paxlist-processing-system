# ✈️ Paxlist Data Processing System

Aplikasi web untuk memproses data penerbangan dengan berbagai filter dan sorting berdasarkan menu yang dipilih. Dibangun menggunakan **Streamlit** dengan interface yang user-friendly.

## 🚀 Demo Live
**[Akses Aplikasi](https://your-app-url.streamlit.app/)** *(akan tersedia setelah deployment)*

## 📋 Fitur Utama

### 🎯 **5 Menu Pemrosesan Data:**
- **JT OUTGOING**: Filter `Dep Station = 'CGK'`
- **JT INCOMING**: Filter `Dep Station ≠ 'CGK'`  
- **IW**: Tanpa filter stasiun
- **IU**: Tanpa filter stasiun
- **ID**: Filter hapus flight yang mengandung "TAXI"

### 📊 **Analisis & Visualisasi:**
- **Statistik Rank**: Distribusi CPT, FO, PU, SFA, FA
- **Statistik Stasiun**: Departure & arrival stations
- **Route Analysis**: Rute penerbangan paling populer
- **Summary Statistics**: Metrics operasional

### 🔧 **Fitur Teknis:**
- ✅ Upload file Excel/CSV (skip header baris pertama)
- ✅ Validasi format file otomatis
- ✅ Custom sorting untuk Rank (CPT→FO→PU→SFA→FA)  
- ✅ Preview 10 baris teratas
- ✅ Download hasil sebagai Excel
- ✅ Interface responsive dan user-friendly

## 🛠️ Teknologi

- **Frontend**: Streamlit
- **Backend**: Python, Pandas
- **Visualisasi**: Streamlit Charts
- **File Processing**: OpenPyXL, XlsxWriter
- **Deployment**: Streamlit Community Cloud

## 📥 Instalasi & Menjalankan Lokal

### Prerequisites
- Python 3.8+
- pip

### Langkah Instalasi
```bash
# Clone repository
git clone https://github.com/username/flight-data-processor.git
cd flight-data-processor

# Install dependencies
pip install -r requirements.txt

# Jalankan aplikasi
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📁 Struktur Project

```
flight-data-processor/
├── app.py                 # Aplikasi utama
├── requirements.txt       # Dependencies Python
├── .streamlit/           
│   └── config.toml       # Konfigurasi Streamlit
├── sample_data/
│   └── sample_flight.xlsx # Contoh data untuk testing
├── screenshots/          # Screenshot aplikasi
├── README.md             # Dokumentasi ini
└── LICENSE               # MIT License
```

## 🎯 Cara Penggunaan

1. **Pilih Menu** - Pilih salah satu dari 5 menu pemrosesan
2. **Upload File** - Upload file Excel/CSV yang berisi data penerbangan
3. **Lihat Hasil** - Preview data yang telah diproses dan statistik
4. **Download** - Unduh hasil pemrosesan sebagai file Excel

### 📋 Format Data yang Diperlukan

File harus memiliki kolom-kolom berikut (header di baris ke-2):
- `Departure Date Time (LT)`
- `Dep Station` 
- `Arr Station`
- `Flight`
- `Pairing Code`
- `Rank`
- Kolom lain sesuai kebutuhan

## 📊 Screenshot

### Dashboard Utama
![Dashboard](screenshots/dashboard.png)

### Statistik & Analytics  
![Statistics](screenshots/statistics.png)

### Data Processing
![Processing](screenshots/processing.png)

## 🚀 Deployment

Aplikasi ini di-deploy menggunakan **Streamlit Community Cloud**.

### Deploy Sendiri:
1. Fork repository ini
2. Kunjungi [share.streamlit.io](https://share.streamlit.io/)  
3. Connect dengan GitHub dan pilih repository
4. Deploy!

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:

1. Fork repository
2. Buat feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📝 Changelog

### v1.0.0 (2024-09-13)
- ✨ Initial release
- 🎯 5 menu pemrosesan data
- 📊 Statistik rank dan stasiun
- 🔧 Custom sorting untuk rank
- 📥 Download hasil sebagai Excel

## 📄 License

Project ini menggunakan [MIT License](LICENSE).

## 👨‍💻 Author

Dibuat dengan ❤️ untuk memudahkan pemrosesan data penerbangan.

---

## 📞 Support

Jika ada pertanyaan atau issue:
- 🐛 [Report Bug](https://github.com/username/flight-data-processor/issues)
- 💡 [Request Feature](https://github.com/username/flight-data-processor/issues)
- 📧 [Contact](mailto:your-email@example.com)

---

⭐ **Star repository ini jika bermanfaat!** ⭐
