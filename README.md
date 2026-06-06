# 🎓 Sistem Prediksi Risiko Drop-out Mahasiswa

Aplikasi berbasis web untuk deteksi dini potensi putus studi mahasiswa menggunakan algoritma **Random Forest Classifier** (Akurasi: 81.01%) dan terintegrasi secara real-time dengan **Firebase Cloud Firestore**.

🚀 Panduan Instalasi & Menjalankan di Lokal
Ikuti langkah-langkah di bawah ini untuk memasang proyek ini di laptop lo:

1. Persiapan Dokumen Kunci Firebase
Pastikan lo sudah mengunduh file kredensial akun layanan Firebase lo dari konsol Firebase. Simpan file tersebut di root direktori proyek ini dengan nama firebase-key.json.

2. Clone Repositori & Masuk ke Folder Proyek
Bash
git clone [https://github.com/BayuFirmansyah00/Don-tBeDO.git](https://github.com/BayuFirmansyah00/Don-tBeDO.git)
cd Don-tBeDO
3. Aktivasi Virtual Environment (.venv)
Untuk Windows (PowerShell):

PowerShell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
Untuk Linux / macOS:

Bash
source .venv/bin/activate
4. Install Seluruh Dependensi Library
Gunakan pengelola paket pip untuk memasang modul-modul yang dibutuhkan:

Bash
pip install streamlit scikit-learn imbalanced-learn firebase-admin pandas numpy matplotlib seaborn
5. Jalankan Aplikasi Web Streamlit
Jalankan perintah di bawah ini untuk membuka dashboard di browser lokal lo (localhost:8501):

Bash
python -m streamlit run app.py
