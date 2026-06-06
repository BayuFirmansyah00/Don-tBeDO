import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pickle
import pandas as pd
import numpy as np
from datetime import datetime
import os

# ── FIREBASE & MODEL ──
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

MODEL_PATH  = "notebooks/model_random_forest.pkl"
SCALER_PATH = "notebooks/scaler.pkl"
DATA_PATH   = "data/dataset_encoded.csv"

@st.cache_resource
def load_assets():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH) and os.path.exists(DATA_PATH):
        with open(MODEL_PATH, "rb") as f: model = pickle.load(f)
        with open(SCALER_PATH, "rb") as f: scaler = pickle.load(f)
        cols = pd.read_csv(DATA_PATH, nrows=1).drop(columns=["Target"], errors="ignore").columns.tolist()
        return model, scaler, cols
    return None, None, None

model, scaler, columns_list = load_assets()

def ipk_to_grade(ipk: float, approved: int) -> float:
    return 0.0 if approved == 0 else round(ipk / 4.0 * 20.0, 4)

# ── CSS ──
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #EEEEF8 !important; }
[data-testid="stHeader"]            { background: transparent !important; }

.form-card {
    background: #FFFFFF; border-radius: 16px;
    padding: 28px 32px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.form-title { font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 20px; }
.divider    { border: none; border-top: 1px solid #F3F4F6; margin: 18px 0; }

/* Panel hasil prediksi */
.hasil-card {
    background: #FFFFFF; border-radius: 16px;
    padding: 24px 26px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.hasil-title { font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 18px;
               display: flex; align-items: center; gap: 8px; }
.resiko-label { font-size: 13px; color: #6B7280; font-weight: 500; margin-bottom: 4px; }
.resiko-value-rendah { font-size: 1.9rem; font-weight: 800; color: #16A34A; }
.resiko-value-sedang { font-size: 1.9rem; font-weight: 800; color: #D97706; }
.resiko-value-tinggi { font-size: 1.9rem; font-weight: 800; color: #DC2626; }
.prob-label  { font-size: 13px; color: #6B7280; font-weight: 500; margin: 14px 0 4px; }
.prob-value  { font-size: 1.6rem; font-weight: 800; color: #3B5BDB; }

/* Progress bar custom */
.progress-wrap { background: #E5E7EB; border-radius: 99px; height: 8px; margin: 8px 0 4px; overflow:hidden; }
.progress-fill { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
.progress-labels { display: flex; justify-content: space-between; font-size: 11px; color: #9CA3AF; }

.rekomen-box {
    background: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 10px;
    padding: 14px 16px; margin-top: 16px;
}
.rekomen-box.sedang { background:#FFFBEB; border-color:#FDE68A; }
.rekomen-box.tinggi { background:#FFF1F2; border-color:#FECDD3; }
.rekomen-title { font-weight: 700; font-size: 13px; color: #065F46; margin-bottom: 4px; }
.rekomen-title.sedang { color:#92400E; }
.rekomen-title.tinggi { color:#991B1B; }
.rekomen-text  { font-size: 13px; color: #374151; line-height: 1.5; }

/* Tentang Prediksi box */
.info-box {
    background: #FFFFFF; border-radius: 16px; padding: 22px 26px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-top: 20px;
    display: flex; gap: 16px; align-items: flex-start;
}
.info-icon  { font-size: 1.6rem; }
.info-title { font-weight: 700; color: #111827; margin-bottom: 6px; }
.info-text  { font-size: 13px; color: #6B7280; line-height: 1.6; }
</style>
""", unsafe_allow_html=True)

# ── JUDUL ──
st.markdown("<h1 style='font-size:2rem;font-weight:700;color:#111827;margin-bottom:4px'>Sistem Prediksi Resiko Drop-out Mahasiswa</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280;margin-top:0;margin-bottom:24px'>Prediksi resiko mahasiswa berdasarkan performa akademik dan status sosial ekonomi</p>", unsafe_allow_html=True)

col_form, col_hasil = st.columns([2, 1.2], gap="large")

# ── FORM ──
with col_form:
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    st.markdown('<div class="form-title">Form Data Mahasiswa</div>', unsafe_allow_html=True)

    nama = st.text_input("Nama Mahasiswa", placeholder="Masukkan nama mahasiswa", label_visibility="visible")

    c1, c2, c3 = st.columns(3)
    with c1:
        semester = st.number_input("Semester Saat Ini", min_value=1, max_value=14, value=2)
    with c2:
        prodi = st.selectbox("Program Studi", ["Teknik Informatika", "Sistem Informasi", "Sains Data"])
    with c3:
        gender = st.selectbox("Jenis Kelamin", ["Laki-laki", "Perempuan"])

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    if semester <= 2:
        a1, a2 = st.columns(2)
        with a1:
            ipk_sem_1 = st.number_input("IPK Semester 1", min_value=0.0, max_value=4.0, value=3.50, step=0.01)
        with a2:
            ipk_sem_2 = st.number_input("IPK Semester 2", min_value=0.0, max_value=4.0, value=3.85, step=0.01) if semester >= 2 else st.number_input("IPK Semester 2", value=3.50, disabled=True)
    else:
        st.caption(f"📌 Semester {semester}: masukkan IPK Kumulatif & IPK Semester Terakhir")
        a1, a2 = st.columns(2)
        with a1:
            ipk_kum = st.number_input("IPK Kumulatif", min_value=0.0, max_value=4.0, value=3.20, step=0.01)
        with a2:
            ipk_last = st.number_input(f"IPK Semester {semester}", min_value=0.0, max_value=4.0, value=3.00, step=0.01)
        ipk_sem_1, ipk_sem_2 = ipk_kum, ipk_last

    b1, b2, b3 = st.columns(3)
    with b1:
        kehadiran = st.number_input("Persentase Kehadiran (%)", min_value=0, max_value=100, value=85)
    with b2:
        sks = st.number_input("Jumlah SKS yang Diambil", min_value=0, max_value=50, value=18)
    with b3:
        mk_ulang = st.number_input("Matkul Mengulang", min_value=0, max_value=20, value=0)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    d1, d2 = st.columns(2)
    with d1:
        beasiswa = st.selectbox("Status Beasiswa", ["Tidak", "Ya"])
    with d2:
        penghasilan = st.selectbox("Penghasilan Orang Tua Perbulan", ["< 1 Juta", "1 – 3 Juta", "3 – 6 Juta", "> 6 Juta"])

    tunggakan = st.selectbox("Status UKT / Biaya Kuliah", ["Lunas / Tepat Waktu", "Ada Tunggakan"])

    st.markdown("<br>", unsafe_allow_html=True)
    submit_btn = st.button("🔍  Prediksi Resiko Drop-out", type="primary", use_container_width=True)
    st.markdown("<p style='text-align:center;color:#9CA3AF;font-size:12px;margin-top:8px'>Pastikan semua data telah diisi dengan benar sebelum melakukan prediksi</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Info box bawah form
    st.markdown("""
    <div class="info-box">
        <span class="info-icon">ℹ️</span>
        <div>
            <div class="info-title">Tentang Prediksi</div>
            <div class="info-text">Prediksi ini menggunakan algoritma <strong>Random Forest</strong> dengan memanfaatkan
            performa akademik dan status sosial-ekonomi mahasiswa. Hasil prediksi digunakan sebagai
            peringatan dini untuk intervensi yang lebih tepat.</div>
        </div>
    </div>""", unsafe_allow_html=True)

# ── HASIL ──
with col_hasil:
    if submit_btn:
        if not nama:
            st.error("Nama Mahasiswa wajib diisi!")
        elif model is None:
            st.error("File model/scaler belum tersedia. Pastikan folder notebooks/ dan data/ sudah lengkap.")
        else:
            matkul_enrolled = int(np.clip(round(sks / 3), 1, 10))
            matkul_approved_2 = max(0, int(round(matkul_enrolled * ipk_sem_2 / 4.0)) - mk_ulang)
            matkul_approved_1 = int(round(matkul_enrolled * ipk_sem_1 / 4.0))
            grade_1 = ipk_to_grade(ipk_sem_1, matkul_approved_1)
            grade_2 = ipk_to_grade(ipk_sem_2, matkul_approved_2)

            daytime    = 1 if kehadiran >= 75 else 0
            debtor     = 1 if tunggakan == "Ada Tunggakan" else 0
            tuition_ok = 1 if debtor == 0 else 0
            scholarship= 1 if beasiswa == "Ya" else 0
            gender_val = 1 if gender == "Laki-laki" else 0
            age_est    = 18 + int(semester // 2)

            df_input = pd.DataFrame(0.0, index=[0], columns=columns_list)
            df_input["Marital status"] = 1; df_input["Application mode"] = 1
            df_input["Application order"] = 1; df_input["Course"] = 9
            df_input["Previous qualification"] = 1; df_input["Nacionality"] = 1
            df_input["Mother's qualification"] = 1; df_input["Father's qualification"] = 1
            df_input["Mother's occupation"] = 4; df_input["Father's occupation"] = 4
            df_input["Displaced"] = 0; df_input["Educational special needs"] = 0
            df_input["International"] = 0
            df_input["Daytime/evening attendance"] = daytime
            df_input["Gender"] = gender_val
            df_input["Age at enrollment"] = age_est
            df_input["Scholarship holder"] = scholarship
            df_input["Debtor"] = debtor
            df_input["Tuition fees up to date"] = tuition_ok
            df_input["Curricular units 1st sem (enrolled)"]   = matkul_enrolled
            df_input["Curricular units 1st sem (approved)"]   = matkul_approved_1
            df_input["Curricular units 1st sem (evaluations)"]= matkul_enrolled + 2
            df_input["Curricular units 1st sem (grade)"]      = grade_1
            df_input["Curricular units 1st sem (credited)"]   = 0
            df_input["Curricular units 1st sem (without evaluations)"] = 0
            df_input["Curricular units 2nd sem (enrolled)"]   = matkul_enrolled
            df_input["Curricular units 2nd sem (approved)"]   = matkul_approved_2
            df_input["Curricular units 2nd sem (evaluations)"]= matkul_enrolled + 2
            df_input["Curricular units 2nd sem (grade)"]      = grade_2
            df_input["Curricular units 2nd sem (credited)"]   = 0
            df_input["Curricular units 2nd sem (without evaluations)"] = 0
            df_input["Unemployment rate"] = 11.5
            df_input["Inflation rate"]    = 1.24
            df_input["GDP"]               = 0.32

            try:
                df_input = df_input[columns_list]
                proba = model.predict_proba(scaler.transform(df_input.values))[0]
                prob_dropout  = float(proba[0]) * 100
                prob_enrolled = float(proba[1]) * 100
                prob_graduate = float(proba[2]) * 100

                if prob_dropout >= 50.0:
                    resiko, level = "TINGGI", "tinggi"
                    rekomen = "PERINGATAN! Resiko drop-out sangat tinggi. Diperlukan intervensi segera berupa bimbingan akademik intensif, peninjauan kondisi ekonomi, dan pendampingan konselor."
                elif prob_dropout >= 25.0:
                    resiko, level = "SEDANG", "sedang"
                    rekomen = "Mahasiswa masuk kategori waspada. Disarankan Kaprodi memberikan konseling akademik atau pemantauan kehadiran dan nilai secara berkala."
                else:
                    resiko, level = "RENDAH", "rendah"
                    rekomen = "Mahasiswa memiliki resiko Drop-out rendah. Pertahankan performa akademik dan terus tingkatkan motivasi belajar."

                bar_color = "#16A34A" if level == "rendah" else ("#D97706" if level == "sedang" else "#DC2626")
                bar_pct   = int(np.clip(prob_dropout, 0, 100))

                st.markdown(f"""
                <div class="hasil-card">
                    <div class="hasil-title">📊 Hasil Prediksi</div>
                    <div class="resiko-label">Resiko Drop-out</div>
                    <div class="resiko-value-{level}">{resiko}</div>
                    <div class="prob-label">Probabilitas Drop-out</div>
                    <div class="prob-value">{prob_dropout:.2f} %</div>
                    <div class="progress-wrap">
                        <div class="progress-fill" style="width:{bar_pct}%;background:{bar_color}"></div>
                    </div>
                    <div class="progress-labels"><span>0%</span><span>50%</span><span>100%</span></div>
                    <div class="rekomen-box {level}">
                        <div class="rekomen-title {level}">Rekomendasi</div>
                        <div class="rekomen-text">{rekomen}</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                payload = {
                    "nama": nama, "semester": int(semester),
                    "ipk_sem_1": float(ipk_sem_1), "ipk_sem_2": float(ipk_sem_2),
                    "kehadiran": int(kehadiran), "resiko": resiko,
                    "probabilitas": f"{prob_dropout:.2f} %",
                    "tanggal": datetime.now().strftime("%d %b %Y"),
                }
                db.collection("riwayat_prediksi").add(payload)
                st.toast("Data sukses disinkronisasi ke Cloud Firebase!", icon="☁️")

            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
    else:
        st.markdown("""
        <div class="hasil-card">
            <div class="hasil-title">📊 Hasil Prediksi</div>
            <div style="color:#9CA3AF;font-size:13px;margin-bottom:16px">
                Silakan isi form di sebelah kiri dan klik tombol prediksi untuk melihat hasil analisis di sini.
            </div>
            <div style="background:#F9FAFB;border-radius:10px;padding:14px;font-size:13px;color:#374151">
                <div style="margin-bottom:6px"><span style="color:#16A34A;font-weight:700">● RENDAH</span> — probabilitas dropout &lt; 25%</div>
                <div style="margin-bottom:6px"><span style="color:#D97706;font-weight:700">● SEDANG</span> — probabilitas dropout 25–50%</div>
                <div><span style="color:#DC2626;font-weight:700">● TINGGI</span> — probabilitas dropout ≥ 50%</div>
            </div>
        </div>""", unsafe_allow_html=True)