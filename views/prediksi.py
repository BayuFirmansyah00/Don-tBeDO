import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ── OPTIONAL FIREBASE ──
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    if not firebase_admin._apps:
        if os.path.exists("firebase-key.json"):
            cred = credentials.Certificate("firebase-key.json")
            firebase_admin.initialize_app(cred)
    db = firestore.client() if firebase_admin._apps else None
except Exception:
    db = None

# ── LOAD MODEL ──
MODEL_PATH  = "notebooks/model_random_forest.pkl"
SCALER_PATH = "notebooks/scaler.pkl"
COLS_PATH   = "notebooks/columns.pkl"
DATA_PATH   = "data/dataset_encoded.csv"

@st.cache_resource
def load_assets():
    model, scaler, cols = None, None, None
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, "rb") as f:  model  = pickle.load(f)
        with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)
        if os.path.exists(COLS_PATH):
            with open(COLS_PATH, "rb") as f: cols = pickle.load(f)
        elif os.path.exists(DATA_PATH):
            cols = pd.read_csv(DATA_PATH, nrows=1).drop(columns=["Target"], errors="ignore").columns.tolist()
    return model, scaler, cols

model, scaler, columns_list = load_assets()

# ══════════════════════════════════════════════════════════════════════════════
# CSS – meniru mockup Form Prediksi persis
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #FFFFFF !important;
    font-family: 'Plus Jakarta Sans', sans-serif;
}
[data-testid="stHeader"]  { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
.block-container          { padding: 0 !important; max-width: 100% !important; }
footer                    { display: none !important; }

/* NAV */
.navbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 72px;
    border-bottom: 1px solid #E5E7EB;
    background: #FFFFFF;
    position: sticky; top: 0; z-index: 100;
}
.nav-brand { font-size: 1.35rem; font-weight: 800; color: #1D77E6; letter-spacing: -0.5px; }
.nav-links { display: flex; gap: 36px; align-items: center; }
.nav-link  { font-size: 0.95rem; font-weight: 500; color: #111827; cursor: pointer; }
.nav-link.active { color: #1D77E6; font-weight: 600; }

/* PAGE TITLE */
.page-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #1D77E6;
    padding: 40px 0 24px;
    letter-spacing: -0.5px;
}

/* FORM CONTAINER */
.form-wrapper {
    max-width: 860px;
    margin: 0 auto;
    padding: 0 24px 60px;
}

/* SECTION CARD */
.section-card {
    border: 1px solid #D1D5DB;
    border-radius: 12px;
    padding: 32px 36px;
    margin-bottom: 28px;
    background: #FFFFFF;
}
.section-card-title {
    text-align: center;
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 28px;
}

/* Streamlit form element overrides */
div[data-testid="stTextInput"] > label,
div[data-testid="stSelectbox"] > label,
div[data-testid="stNumberInput"] > label {
    font-size: 0.9rem !important;
    font-weight: 500 !important;
    color: #374151 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

div[data-testid="stTextInput"] input,
div[data-testid="stNumberInput"] input,
div[data-testid="stSelectbox"] > div {
    border: 1px solid #D1D5DB !important;
    border-radius: 8px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Submit button */
div[data-testid="stButton"] > button[kind="primary"] {
    background: #1D77E6 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 48px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    display: block !important;
    margin: 0 auto !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background: #1560C4 !important;
}

/* Hasil prediksi */
.hasil-box {
    border-radius: 12px;
    padding: 28px 32px;
    margin-top: 32px;
    margin-bottom: 16px;
}
.hasil-rendah { background: #F0FDF4; border: 1.5px solid #86EFAC; }
.hasil-sedang { background: #FFFBEB; border: 1.5px solid #FCD34D; }
.hasil-tinggi { background: #FFF1F2; border: 1.5px solid #FECDD3; }

.hasil-label  { font-size: 0.85rem; font-weight: 600; color: #6B7280; margin-bottom: 4px; }
.hasil-resiko-rendah { font-size: 2.2rem; font-weight: 800; color: #16A34A; }
.hasil-resiko-sedang { font-size: 2.2rem; font-weight: 800; color: #D97706; }
.hasil-resiko-tinggi { font-size: 2.2rem; font-weight: 800; color: #DC2626; }
.hasil-prob   { font-size: 1.5rem; font-weight: 700; color: #1D77E6; margin-top: 8px; }
.rekomen-text { font-size: 0.9rem; color: #374151; line-height: 1.6; margin-top: 16px; }

.progress-bg { background: #E5E7EB; border-radius: 99px; height: 8px; margin: 10px 0; overflow: hidden; }
.progress-bar { height: 100%; border-radius: 99px; }
</style>
""", unsafe_allow_html=True)

# ── NAVBAR ──
st.markdown("""
<div class="navbar">
    <div class="nav-brand">DontBe–DO</div>
    <div class="nav-links">
        <span class="nav-link">Beranda</span>
        <span class="nav-link active">Prediksi</span>
        <span class="nav-link">Tentang</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── JUDUL HALAMAN ──
st.markdown('<div class="page-title">Prediksi Dropout</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# FORM – 3 SECTION CARD sesuai mockup
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="form-wrapper">', unsafe_allow_html=True)

# ── SECTION 1: FAKTOR AKADEMIK ──
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-card-title">Faktor Akademik</div>', unsafe_allow_html=True)

nama = st.text_input("Nama Mahasiswa", placeholder="Masukkan nama lengkap mahasiswa")

col_gender, col_prodi = st.columns(2)
with col_gender:
    gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
with col_prodi:
    prodi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi", "Sains Data", "Lainnya"])

# Baris IPK, SKS, Matkul Lulus – Semester 1
col_ipk1, col_sks1, col_mk_lulus1 = st.columns(3)
with col_ipk1:
    ipk_sem_1 = st.number_input("IPK Semester 1", min_value=0.0, max_value=4.0, value=3.50, step=0.01, format="%.2f")
with col_sks1:
    sks_sem_1 = st.number_input("Jumlah SKS smt 1", min_value=0, max_value=30, value=20)
with col_mk_lulus1:
    mk_lulus_1 = st.number_input("Jumlah Matkul Lulus (Smt 1)", min_value=0, max_value=15, value=6)

# Baris IPK, SKS, Matkul Lulus – Semester 2
col_ipk2, col_sks2, col_mk_lulus2 = st.columns(3)
with col_ipk2:
    ipk_sem_2 = st.number_input("IPK Semester 2", min_value=0.0, max_value=4.0, value=3.50, step=0.01, format="%.2f")
with col_sks2:
    sks_sem_2 = st.number_input("Jumlah SKS smt 2", min_value=0, max_value=30, value=20)
with col_mk_lulus2:
    mk_lulus_2 = st.number_input("Jumlah Matkul Lulus (Smt 2)", min_value=0, max_value=15, value=6)

st.markdown('</div>', unsafe_allow_html=True)

# ── SECTION 2: FAKTOR SOSIAL ──
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-card-title">Faktor Sosial</div>', unsafe_allow_html=True)

col_s1, col_s2 = st.columns(2)
with col_s1:
    status_nikah = st.selectbox("Status Pernikahan", ["Belum Menikah", "Menikah", "Cerai"])
with col_s2:
    usia = st.number_input("Usia Saat Masuk Kuliah", min_value=15, max_value=60, value=19)

col_s3, col_s4 = st.columns(2)
with col_s3:
    waktu_kuliah = st.selectbox("Waktu Kuliah", ["Pagi / Reguler", "Malam / Karyawan"])
with col_s4:
    pindahan = st.selectbox("Mahasiswa Pindahan", ["Tidak", "Ya"])

st.markdown('</div>', unsafe_allow_html=True)

# ── SECTION 3: FAKTOR EKONOMI ──
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-card-title">Faktor Ekonomi</div>', unsafe_allow_html=True)

col_e1, col_e2 = st.columns(2)
with col_e1:
    tunggakan = st.selectbox("Tunggakan", ["Tidak Ada", "Ada Tunggakan"])
with col_e2:
    status_ukt = st.selectbox("Status Biaya Kuliah", ["Lunas / Tepat Waktu", "Belum Lunas"])

beasiswa = st.selectbox("Penerima Beasiswa", ["Tidak", "Ya"])

st.markdown('</div>', unsafe_allow_html=True)

# ── TOMBOL PREDIKSI ──
st.markdown("<br>", unsafe_allow_html=True)
col_btn = st.columns([1, 2, 1])
with col_btn[1]:
    submit = st.button("Mulai Prediksi", type="primary", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# LOGIKA PREDIKSI
# ══════════════════════════════════════════════════════════════════════════════
if submit:
    if not nama:
        st.error("Nama Mahasiswa wajib diisi!")
    elif model is None:
        st.error("❌ Model belum tersedia. Jalankan `Week5_Modeling.ipynb` terlebih dahulu untuk membuat `model_random_forest.pkl` dan `scaler.pkl` di folder `notebooks/`.")
    else:
        try:
            # ── Hitung jumlah matkul enrolled dari SKS ──
            matkul_enrolled_1 = max(1, round(sks_sem_1 / 3))
            matkul_enrolled_2 = max(1, round(sks_sem_2 / 3))

            # ── Grade (skala 0-20, format UCI dataset) ──
            grade_1 = round(ipk_sem_1 / 4.0 * 20.0, 4) if mk_lulus_1 > 0 else 0.0
            grade_2 = round(ipk_sem_2 / 4.0 * 20.0, 4) if mk_lulus_2 > 0 else 0.0

            # ── Encode fitur sosial-ekonomi ──
            marital_map = {"Belum Menikah": 1, "Menikah": 2, "Cerai": 3}
            marital     = marital_map.get(status_nikah, 1)
            daytime     = 1 if waktu_kuliah == "Pagi / Reguler" else 0
            displaced   = 1 if pindahan == "Ya" else 0
            debtor      = 1 if tunggakan == "Ada Tunggakan" else 0
            tuition_ok  = 0 if status_ukt == "Belum Lunas" else 1
            scholarship = 1 if beasiswa == "Ya" else 0
            gender_val  = 1 if gender == "Laki-laki" else 0

            # ── Bangun dataframe input sesuai kolom training ──
            df_input = pd.DataFrame(0.0, index=[0], columns=columns_list)

            # Isi nilai yang tersedia
            mapping = {
                "Marital status"                              : marital,
                "Application mode"                           : 1,
                "Application order"                          : 1,
                "Course"                                     : 9,
                "Daytime/evening attendance"                 : daytime,
                "Previous qualification"                     : 1,
                "Nacionality"                                : 1,
                "Mother's qualification"                     : 1,
                "Father's qualification"                     : 1,
                "Mother's occupation"                        : 4,
                "Father's occupation"                        : 4,
                "Displaced"                                  : displaced,
                "Educational special needs"                  : 0,
                "Debtor"                                     : debtor,
                "Tuition fees up to date"                    : tuition_ok,
                "Gender"                                     : gender_val,
                "Scholarship holder"                         : scholarship,
                "Age at enrollment"                          : int(usia),
                "International"                              : 0,
                "Curricular units 1st sem (credited)"        : 0,
                "Curricular units 1st sem (enrolled)"        : int(matkul_enrolled_1),
                "Curricular units 1st sem (evaluations)"     : int(matkul_enrolled_1) + 2,
                "Curricular units 1st sem (approved)"        : int(mk_lulus_1),
                "Curricular units 1st sem (grade)"           : grade_1,
                "Curricular units 1st sem (without evaluations)": 0,
                "Curricular units 2nd sem (credited)"        : 0,
                "Curricular units 2nd sem (enrolled)"        : int(matkul_enrolled_2),
                "Curricular units 2nd sem (evaluations)"     : int(matkul_enrolled_2) + 2,
                "Curricular units 2nd sem (approved)"        : int(mk_lulus_2),
                "Curricular units 2nd sem (grade)"           : grade_2,
                "Curricular units 2nd sem (without evaluations)": 0,
                "Unemployment rate"                          : 11.5,
                "Inflation rate"                             : 1.24,
                "GDP"                                        : 0.32,
            }
            for col, val in mapping.items():
                if col in df_input.columns:
                    df_input[col] = val

            df_input = df_input[columns_list]

            # ── Prediksi ──
            proba         = model.predict_proba(scaler.transform(df_input.values))[0]
            # Target 0=Dropout, 1=Enrolled, 2=Graduate
            prob_dropout  = float(proba[0]) * 100
            prob_enrolled = float(proba[1]) * 100
            prob_graduate = float(proba[2]) * 100

            # ── Klasifikasi risiko ──
            if prob_dropout >= 50.0:
                resiko = "TINGGI"
                level  = "tinggi"
                rekomen = "⚠️ PERINGATAN! Risiko drop-out sangat tinggi. Diperlukan intervensi segera berupa bimbingan akademik intensif, peninjauan kondisi ekonomi, dan pendampingan konselor."
                bar_color = "#DC2626"
            elif prob_dropout >= 25.0:
                resiko = "SEDANG"
                level  = "sedang"
                rekomen = "⚡ Mahasiswa masuk kategori waspada. Disarankan memberikan konseling akademik atau pemantauan kehadiran dan nilai secara berkala."
                bar_color = "#D97706"
            else:
                resiko = "RENDAH"
                level  = "rendah"
                rekomen = "✅ Mahasiswa memiliki risiko dropout rendah. Pertahankan performa akademik dan terus tingkatkan motivasi belajar."
                bar_color = "#16A34A"

            bar_pct = int(np.clip(prob_dropout, 0, 100))

            # ── Tampilkan hasil ──
            st.markdown(f"""
            <div style="max-width:860px;margin:0 auto;padding:0 24px;">
                <div class="hasil-box hasil-{level}">
                    <div style="font-size:1.2rem;font-weight:800;color:#111827;margin-bottom:20px">📊 Hasil Prediksi – {nama}</div>

                    <div style="display:flex;gap:48px;flex-wrap:wrap;margin-bottom:20px;">
                        <div>
                            <div class="hasil-label">Risiko Drop-out</div>
                            <div class="hasil-resiko-{level}">{resiko}</div>
                        </div>
                        <div>
                            <div class="hasil-label">Probabilitas Drop-out</div>
                            <div class="hasil-prob">{prob_dropout:.2f}%</div>
                        </div>
                        <div>
                            <div class="hasil-label">Prob. Lulus</div>
                            <div style="font-size:1.2rem;font-weight:700;color:#16A34A;">{prob_graduate:.2f}%</div>
                        </div>
                    </div>

                    <div class="hasil-label">Skala Probabilitas Drop-out</div>
                    <div class="progress-bg">
                        <div class="progress-bar" style="width:{bar_pct}%;background:{bar_color};"></div>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:11px;color:#9CA3AF;margin-bottom:16px;">
                        <span>0%</span><span>50%</span><span>100%</span>
                    </div>

                    <div class="rekomen-text">{rekomen}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Simpan ke Firebase (opsional) ──
            if db:
                payload = {
                    "nama"        : nama,
                    "ipk_sem_1"   : float(ipk_sem_1),
                    "ipk_sem_2"   : float(ipk_sem_2),
                    "sks_sem_1"   : int(sks_sem_1),
                    "sks_sem_2"   : int(sks_sem_2),
                    "mk_lulus_1"  : int(mk_lulus_1),
                    "mk_lulus_2"  : int(mk_lulus_2),
                    "status_nikah": status_nikah,
                    "usia"        : int(usia),
                    "waktu_kuliah": waktu_kuliah,
                    "tunggakan"   : tunggakan,
                    "beasiswa"    : beasiswa,
                    "resiko"      : resiko,
                    "probabilitas": f"{prob_dropout:.2f} %",
                    "tanggal"     : datetime.now().strftime("%d %b %Y"),
                }
                db.collection("riwayat_prediksi").add(payload)
                st.toast("☁️ Data tersimpan ke Firebase!", icon="☁️")

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")