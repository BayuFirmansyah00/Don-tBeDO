import streamlit as st

st.markdown("""
<style>
    .title-txt { font-size: 1.85rem; font-weight: 800; color: #111827; margin-bottom: 4px; }
    .subtitle-txt { font-size: 0.95rem; color: #6B7280; margin-bottom: 28px; }
    .card-about { background: #FFFFFF; border: 1px solid #E5E7EB; padding: 28px 32px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); margin-bottom: 20px; }
    .card-about-title { font-size: 1.05rem; font-weight: 700; color: #111827; margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid #F3F4F6; }
    .card-about-desc { font-size: 0.92rem; color: #374151; line-height: 1.7; text-align: justify; }
    .tech-badge { background-color: #F3F4F6; color: #1F2937; font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 6px; display: inline-block; margin-right: 8px; margin-bottom: 8px; border: 1px solid #E5E7EB; }
    .pipeline-step { display: flex; align-items: flex-start; gap: 14px; margin-bottom: 16px; }
    .pipeline-num { background: #4F46E5; color: white; font-weight: 700; font-size: 0.82rem; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
    .pipeline-text { font-size: 0.9rem; color: #374151; line-height: 1.6; }
    .pipeline-text b { color: #111827; }
    .info-box { background: #EEF2FF; border: 1px solid #E0E7FF; border-radius: 8px; padding: 14px 18px; font-size: 0.88rem; color: #3730A3; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-txt">Tentang Sistem</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-txt">Detail fundamental pengembangan Sistem Peringatan Dini (Early Warning System) DontBe-DO.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card-about">
    <div class="card-about-title">Filosofi Early Warning System (EWS)</div>
    <div class="card-about-desc">
        Sistem <b>DontBe-DO</b> dirancang secara spesifik untuk memecahkan problem keterlambatan birokrasi kampus dalam mengidentifikasi sinyal penurunan performa mahasiswa. Berdasarkan riset, tindakan penyelamatan mahasiswa dari risiko putus studi paling krusial dieksekusi sebelum memasuki tahun kedua perkuliahan.<br><br>
        Oleh karena itu, sistem ini bertindak sebagai alat deteksi dini dengan memanfaatkan data historis performa akademik dari <b>Semester 1 dan Semester 2</b>. Melalui pendekatan dinamis, sistem mampu membaca pola anomali nilai, tumpukan beban SKS, serta status finansial untuk memetakan prediksi tingkat kerentanan mahasiswa bahkan ketika mereka baru saja menyelesaikan semester pertama studi.
    </div>
</div>

<div class="card-about">
    <div class="card-about-title">Dataset dan Spesifikasi Pemodelan AI</div>
    <div class="card-about-desc">
        Inti kecerdasan sistem ini dibangun menggunakan basis data terverifikasi <b>Predict Students' Dropout and Academic Success</b> dari <b>UCI Machine Learning Repository</b>. Dataset ini mengintegrasikan faktor makro ekonomi, data demografi, latar belakang sosial orang tua, kondisi finansial, serta capaian kurikuler mendalam pada unit semester awal.<br><br>
        Klasifikasi risiko dieksekusi oleh algoritma <b>Random Forest Classifier</b> yang telah dioptimasi melalui proses <i>hyperparameter tuning</i> (GridSearchCV). Model dilatih untuk memprediksi probabilitas tiga kelas output: <b>Dropout</b>, <b>Enrolled</b>, dan <b>Graduate</b> — dengan fokus utama pada akurasi prediksi kelas Dropout.
    </div>
</div>

<div class="card-about">
    <div class="card-about-title">Alur Pipeline Data dan Model</div>
    <div class="pipeline-step">
        <div class="pipeline-num">1</div>
        <div class="pipeline-text"><b>Preprocessing</b> — Pembersihan data, encoding variabel kategorikal, dan penanganan nilai hilang dari dataset UCI.</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">2</div>
        <div class="pipeline-text"><b>Feature Engineering</b> — Seleksi fitur relevan, transformasi skala, dan penyeimbangan kelas data training.</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">3</div>
        <div class="pipeline-text"><b>Modeling</b> — Training Random Forest dengan SMOTE pada data train, StandardScaler untuk normalisasi, dan GridSearchCV untuk hyperparameter tuning.</div>
    </div>
    <div class="pipeline-step">
        <div class="pipeline-num">4</div>
        <div class="pipeline-text"><b>Deployment</b> — Model, scaler, dan daftar kolom diserialisasi ke format <code>.pkl</code> dan di-load oleh aplikasi Streamlit ini.</div>
    </div>
</div>

<div class="card-about">
    <div class="card-about-title">Infrastruktur Teknologi</div>
    <div class="tech-badge">Python 3.x</div>
    <div class="tech-badge">Streamlit Framework</div>
    <div class="tech-badge">Scikit-Learn</div>
    <div class="tech-badge">Pandas & NumPy</div>
    <div class="tech-badge">imbalanced-learn (SMOTE)</div>
</div>

<div class="info-box">
    <b>Project Plan ID: PJK-GM068</b> — Dikembangkan sebagai wujud kolaborasi Capstone Project program Pijak 2026 di bawah bimbingan keahlian AI Engineer Path.
</div>
""", unsafe_allow_html=True)