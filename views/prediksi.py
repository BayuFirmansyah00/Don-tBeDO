import streamlit as st
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ── LOAD ASSETS MODEL ──
MODEL_PATH  = "notebooks/model_random_forest.pkl"
SCALER_PATH = "notebooks/scaler.pkl"
COLS_PATH   = "notebooks/columns.pkl"

@st.cache_resource
def load_assets():
    model, scaler, cols = None, None, None
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        with open(MODEL_PATH, "rb") as f:  model  = pickle.load(f)
        with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)
        if os.path.exists(COLS_PATH):
            with open(COLS_PATH, "rb") as f: cols = pickle.load(f)
    return model, scaler, cols

model, scaler, columns_list = load_assets()

# ── INJEKSI CSS STRUKTUR CARD FORM (MOCKUP COCOK) ──
st.markdown("""
<style>
    .main-title { font-size: 1.85rem; font-weight: 800; color: #111827; margin-bottom: 2px; }
    .sub-title { font-size: 0.95rem; color: #6B7280; margin-bottom: 24px; }
    .section-card { background: #FFFFFF; padding: 24px; border-radius: 12px; border: 1px solid #E5E7EB; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 20px; }
    .section-card-title { font-size: 1.1rem; font-weight: 700; color: #111827; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
    .hasil-box { padding: 24px; border-radius: 12px; margin-top: 24px; border: 1px solid #E5E7EB; }
    .hasil-rendah { background-color: #F0FDF4; border-color: #DCFCE7; }
    .hasil-sedang { background-color: #FFFBEB; border-color: #FEF3C7; }
    .hasil-tinggi { background-color: #FEF2F2; border-color: #FEE2E2; }
    .hasil-label { font-size: 0.85rem; color: #4B5563; font-weight: 500; }
    .hasil-prob { font-size: 1.2rem; font-weight: 700; color: #111827; }
    .hasil-resiko-rendah { font-size: 1.2rem; font-weight: 800; color: #16A34A; }
    .hasil-resiko-sedang { font-size: 1.2rem; font-weight: 800; color: #D97706; }
    .hasil-resiko-tinggi { font-size: 1.2rem; font-weight: 800; color: #DC2626; }
    .progress-bg { background-color: #E5E7EB; border-radius: 9999px; height: 8px; width: 100%; margin-top: 8px; overflow: hidden; }
    .progress-bar { height: 100%; border-radius: 9999px; }
    .rekomen-text { font-size: 0.9rem; color: #374151; line-height: 1.5; font-weight: 500; background: #FFFFFF; padding: 12px 16px; border-radius: 8px; border: 1px solid #E5E7EB; margin-top: 12px; }
    div[data-testid="stForm"] { border: none !important; padding: 0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🔮 Formulir Prediksi Risiko Dropout</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Isi data akademik dan sosial ekonomi mahasiswa untuk menganalisis potensi kelangsungan studi.</div>', unsafe_allow_html=True)

with st.form("form_prediksi_internal"):
    # ── KELOMPOK 1: DATA IDENTITAS & BASIS EVALUASI ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-card-title">📋 Data Identitas & Basis Evaluasi</div>', unsafe_allow_html=True)
    col_nama, col_mode = st.columns([2, 2])
    with col_nama:
        nama = st.text_input("Nama Lengkap Mahasiswa", placeholder="Contoh: Bayu Firmansyah")
    with col_mode:
        mode_semester = st.selectbox(
            "Mode Sistem Deteksi Dini (Early Warning)",
            ["Evaluasi Akhir Semester 1 (Deteksi Dini)", "Evaluasi Akhir Semester 2 (Deteksi Akhir Tahun Pertama)"]
        )
    col_gender, col_prodi, col_usia = st.columns([1, 2, 1])
    with col_gender:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    with col_prodi:
        prodi = st.selectbox("Program Studi", ["Agro-industrial Management", "Informatics / Teknik Informatika", "Sistem Informasi", "Sains Data"])
    with col_usia:
        usia = st.number_input("Usia Saat Masuk Kuliah", min_value=15, max_value=60, value=18)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── KELOMPOK 2: PERFORMA AKADEMIK ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-card-title">📊 Performa Academic Mahasiswa</div>', unsafe_allow_html=True)
    if mode_semester == "Evaluasi Akhir Semester 1 (Deteksi Dini)":
        st.info("💡 Mode Deteksi Dini Aktif: Parameter Semester 2 akan otomatis disesuaikan dengan performa Semester 1 agar model klasifikasi tetap konsisten.")
        col_ipk1, col_sks1, col_mk_lulus1 = st.columns(3)
        with col_ipk1:
            ipk_sem_1 = st.number_input("IPK Semester 1", min_value=0.0, max_value=4.0, value=3.00, step=0.01)
        with col_sks1:
            sks_sem_1 = st.number_input("Jumlah SKS Diambil (Semester 1)", min_value=0, max_value=30, value=20)
        with col_mk_lulus1:
            mk_lulus_1 = st.number_input("Jumlah Matkul Lulus (Semester 1)", min_value=0, max_value=15, value=6)
        ipk_sem_2, sks_sem_2, mk_lulus_2 = ipk_sem_1, sks_sem_1, mk_lulus_1
    else:
        col_ipk1, col_sks1, col_mk_lulus1 = st.columns(3)
        with col_ipk1: ipk_sem_1 = st.number_input("IPK Semester 1", min_value=0.0, max_value=4.0, value=3.00, step=0.01)
        with col_sks1: sks_sem_1 = st.number_input("Jumlah SKS Diambil (Semester 1)", min_value=0, max_value=30, value=20)
        with col_mk_lulus1: mk_lulus_1 = st.number_input("Jumlah Matkul Lulus (Semester 1)", min_value=0, max_value=15, value=6)
        st.markdown("<hr style='margin:12px 0; border-color:#E5E7EB;'>", unsafe_allow_html=True)
        col_ipk2, col_sks2, col_mk_lulus2 = st.columns(3)
        with col_ipk2: ipk_sem_2 = st.number_input("IPK Semester 2", min_value=0.0, max_value=4.0, value=3.00, step=0.01)
        with col_sks2: sks_sem_2 = st.number_input("Jumlah SKS Diambil (Semester 2)", min_value=0, max_value=30, value=20)
        with col_mk_lulus2: mk_lulus_2 = st.number_input("Jumlah Matkul Lulus (Semester 2)", min_value=0, max_value=15, value=6)
    st.markdown('</div>', unsafe_allow_html=True)

    # ── KELOMPOK 3: FAKTOR SOSIAL & EKONOMI ──
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-card-title">💰 Kondisi Sosial & Keuangan</div>', unsafe_allow_html=True)
    col_nikah, col_waktu, col_pindah = st.columns(3)
    with col_nikah: status_nikah = st.selectbox("Status Pernikahan", ["Belum Menikah", "Menikah", "Cerai"])
    with col_waktu: waktu_kuliah = st.selectbox("Waktu Perkuliahan", ["Pagi / Reguler", "Malam / Karyawan"])
    with col_pindah: pindahan = st.selectbox("Mahasiswa Imigran/Pindahan?", ["Tidak", "Ya"])
    col_tunggakan, col_ukt, col_beasiswa = st.columns(3)
    with col_tunggakan: tunggakan = st.selectbox("Status Tunggakan Internal", ["Tidak Ada", "Ada Tunggakan"])
    with col_ukt: status_ukt = st.selectbox("Pembayaran UKT Semester Ini", ["Lunas", "Belum Lunas"])
    with col_beasiswa: beasiswa = st.selectbox("Menerima Beasiswa?", ["Tidak", "Ya"])
    st.markdown('</div>', unsafe_allow_html=True)

    submit = st.form_submit_button("Mulai Analisis Prediksi Risiko 🚀", use_container_width=True)

# ── PROSES INFERENSI MODEL AI ──
if submit:
    if not nama:
        st.error("⚠️ Nama Lengkap Mahasiswa wajib diisi!")
    elif model is None:
        st.error("❌ Berkas model Random Forest tidak siap.")
    else:
        try:
            matkul_enrolled_1, matkul_enrolled_2 = max(1, round(sks_sem_1 / 3)), max(1, round(sks_sem_2 / 3))
            grade_1 = round(ipk_sem_1 / 4.0 * 20.0, 4) if mk_lulus_1 > 0 else 0.0
            grade_2 = round(ipk_sem_2 / 4.0 * 20.0, 4) if mk_lulus_2 > 0 else 0.0

            marital_map = {"Belum Menikah": 1, "Menikah": 2, "Cerai": 3}
            df_input = pd.DataFrame(0.0, index=[0], columns=columns_list)
            
            mapping = {
                "Marital status": marital_map.get(status_nikah, 1), "Application mode": 1, "Application order": 1, "Course": 9,
                "Daytime/evening attendance": 1 if waktu_kuliah == "Pagi / Reguler" else 0, "Previous qualification": 1, "Nacionality": 1,
                "Mother's qualification": 1, "Father's qualification": 1, "Mother's occupation": 4, "Father's occupation": 4,
                "Displaced": 1 if pindahan == "Ya" else 0, "Educational special needs": 0, "Debtor": 1 if tunggakan == "Ada Tunggakan" else 0,
                "Tuition fees up to date": 0 if status_ukt == "Belum Lunas" else 1, "Gender": 1 if gender == "Laki-laki" else 0,
                "Scholarship holder": 1 if beasiswa == "Ya" else 0, "Age at enrollment": int(usia), "International": 0,
                "Curricular units 1st sem (credited)": 0, "Curricular units 1st sem (enrolled)": int(matkul_enrolled_1),
                "Curricular units 1st sem (evaluations)": int(matkul_enrolled_1) + 2, "Curricular units 1st sem (approved)": int(mk_lulus_1),
                "Curricular units 1st sem (grade)": grade_1, "Curricular units 1st sem (without evaluations)": 0, "Curricular units 2nd sem (credited)": 0,
                "Curricular units 2nd sem (enrolled)": int(matkul_enrolled_2), "Curricular units 2nd sem (evaluations)": int(matkul_enrolled_2) + 2,
                "Curricular units 2nd sem (approved)": int(mk_lulus_2), "Curricular units 2nd sem (grade)": grade_2, "Curricular units 2nd sem (without evaluations)": 0,
                "Unemployment rate": 11.5, "Inflation rate": 1.24, "GDP": 0.32
            }
            for col, val in mapping.items():
                if col in df_input.columns: df_input[col] = val

            df_input = df_input[columns_list] # Garansi urutan array fiture
            proba = model.predict_proba(scaler.transform(df_input))[0]
            classes = list(model.classes_)
            prob_dropout  = proba[classes.index(0)] * 100 if 0 in classes else 0.0
            prob_graduate = proba[classes.index(2)] * 100 if 2 in classes else 0.0

            if prob_dropout >= 50.0:
                resiko, level, bar_color = "TINGGI", "tinggi", "#DC2626"
                rekomen = "⚠️ <b>PERINGATAN SEGERA!</b> Mahasiswa terindikasi berada dalam risiko tinggi putus studi. Diwajibkan bimbingan intensif bersama Dosen Wali."
            elif prob_dropout >= 25.0:
                resiko, level, bar_color = "SEDANG", "sedang", "#D97706"
                rekomen = "⚡ <b>STATUS WASPADA!</b> Mahasiswa memiliki kerentanan akademik sedang. Disarankan mendapatkan monitoring berkala."
            else:
                resiko, level, bar_color = "RENDAH", "rendah", "#16A34A"
                rekomen = "✅ <b>PERFORMA AMAN.</b> Evaluasi tracking menunjukkan tingkat persistensi studi yang solid. Pertahankan!"

            bar_pct = int(np.clip(prob_dropout, 0, 100))
            st.markdown(f"""
            <div class="hasil-box hasil-{level}">
                <div style="font-size:1.15rem; font-weight:800; color:#111827; margin-bottom:16px;">📊 Hasil Analisis Prediksi – {nama}</div>
                <div style="display:flex; gap:40px; flex-wrap:wrap; margin-bottom:18px;">
                    <div><div class="hasil-label">Kategori Risiko</div><div class="hasil-resiko-{level}">{resiko}</div></div>
                    <div><div class="hasil-label">Potensi Dropout</div><div class="hasil-prob">{prob_dropout:.2f}%</div></div>
                    <div><div class="hasil-label">Estimasi Kelulusan</div><div style="font-size:1.2rem; font-weight:700; color:#16A34A;">{prob_graduate:.2f}%</div></div>
                </div>
                <div class="hasil-label">Skala Visualisasi Indeks Kerawanan Dropout</div>
                <div class="progress-bg"><div class="progress-bar" style="width:{bar_pct}%; background:{bar_color};"></div></div>
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#9CA3AF; margin-top:4px;"><span>0% (Aman)</span><span>100% (Kritis)</span></div>
                <div class="rekomen-text">{rekomen}</div>
            </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Kesalahan kalkulasi teknis: {e}")