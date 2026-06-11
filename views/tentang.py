import streamlit as st

st.markdown("""
<style>
    .title-txt { font-size: 1.85rem; font-weight: 800; color: #111827; margin-bottom: 4px; }
    .subtitle-txt { font-size: 0.95rem; color: #6B7280; margin-bottom: 24px; }
    .card-about { background: #FFFFFF; border: 1px solid #E5E7EB; padding: 24px; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.03); margin-bottom: 20px; }
    .card-about-title { font-size: 1.15rem; font-weight: 700; color: #111827; margin-bottom: 12px; }
    .card-about-desc { font-size: 0.92rem; color: #374151; line-height: 1.6; text-align: justify; }
    .tech-badge { background-color: #F3F4F6; color: #1F2937; font-size: 0.8rem; font-weight: 600; padding: 4px 12px; border-radius: 6px; display: inline-block; margin-right: 8px; margin-bottom: 8px; border: 1px solid #E5E7EB; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title-txt">ℹ️ Tentang Sistem & Arsitektur</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-txt">Detail fundamental pengembangan Sistem Peringatan Dini (Early Warning System) DontBe-DO.</div>', unsafe_allow_html=True)

st.markdown("""
<div class="card-about">
    <div class="card-about-title">🛡️ Filosofi Early Warning System (EWS)</div>
    <div class="card-about-desc">
        Sistem <b>DontBe-DO</b> dirancang secara spesifik untuk memecahkan problem keterlambatan birokrasi kampus dalam mengidentifikasi sinyal penurunan performa mahasiswa. Berdasarkan riset, tindakan penyelamatan mahasiswa dari risiko putus studi paling krusial dieksekusi sebelum memasuki tahun kedua perkuliahan.<br><br>
        Oleh karena itu, sistem ini bertindak sebagai alat deteksi dini dengan memanfaatkan data historis performa akademik dari <b>Semester 1 dan Semester 2</b>. Melalui pendekatan dinamis, sistem mampu membaca pola anomali nilai, tumpukan beban SKS, serta status finansial untuk memetakan prediksi tingkat kerentanan mahasiswa bahkan ketika mereka baru saja menyelesaikan semester pertama studi. Hal ini memberikan jendela waktu yang berharga bagi pihak program studi untuk merumuskan strategi penanganan preventif sebelum terlambat.
    </div>
</div>

<div class="card-about">
    <div class="card-about-title">📊 Dataset & Spesifikasi Pemodelan AI</div>
    <div class="card-about-desc">
        Inti kecerdasan sistem ini dibangun menggunakan basis data terverifikasi <b>Predict Students' Dropout and Academic Success</b> dari <b>UCI Machine Learning Repository</b>. Dataset komprehensif ini mengintegrasikan faktor makro ekonomi, data demografi, latar belakang sosial orang tua, kondisi finansial, serta capaian kurikuler mendalam pada unit semester awal.<br><br>
        Klasifikasi risiko dieksekusi oleh algoritma <b>Random Forest Classifier</b> yang telah dioptimasi melalui proses hyperparameter tuning. Model dilatih untuk memisahkan output ke dalam probabilistik multitarget (Dropout, Enrolled, Graduate), di mana fokus utama ditekankan pada akurasi prediksi probabilitas kelas 'Dropout'.
    </div>
</div>

<div class="card-about">
    <div class="card-about-title">🛠️ Spesifikasi Infrastruktur Teknologi</div>
    <div class="tech-badge">Python 3.x</div>
    <div class="tech-badge">Streamlit Framework</div>
    <div class="tech-badge">Scikit-Learn (Modeling)</div>
    <div class="tech-badge">Pandas & NumPy</div>
    <div class="tech-badge">Firebase Serverless Firestore</div>
</div>
""", unsafe_allow_html=True)

st.info("🎯 **Project Plan ID: PJK-GM068** — Dikembangkan sebagai wujud kolaborasi Capstone Project program Pijak 2026 di bawah bimbingan keahlian AI Engineer Path.")