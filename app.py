import streamlit as st
import importlib.util
import sys
import os

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA (Wajib Paling Atas)
# ==============================================================================
st.set_page_config(
    page_title="DontBe-DO | Early Warning System Risiko Dropout",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. LOGIKA STATE NAVIGASI KUSTOM
# ==============================================================================
if "current_page" not in st.session_state:
    st.session_state.current_page = "Beranda"

def pindah_halaman(nama_halaman):
    # Cukup set session_state — Streamlit otomatis rerender, st.rerun() tidak diperlukan
    st.session_state.current_page = nama_halaman

def load_view(filepath: str):
    """Load halaman view secara aman menggunakan importlib."""
    abs_path = os.path.abspath(filepath)
    if not os.path.exists(abs_path):
        st.error(f"❌ File view tidak ditemukan: {abs_path}")
        return
    module_name = os.path.splitext(os.path.basename(abs_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, abs_path)
    module = importlib.util.module_from_spec(spec)
    if module_name in sys.modules:
        del sys.modules[module_name]
    spec.loader.exec_module(module)

# ==============================================================================
# 3. CSS GLOBAL & NAVBAR
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { font-family: 'Plus Jakarta Sans', sans-serif !important; }

/* Sembunyikan elemen bawaan Streamlit */
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { background: transparent !important; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Push konten ke bawah navbar */
.block-container { padding-top: 80px !important; }

/* Warna tombol aktif navbar */
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background-color: #4F46E5 !important;
    border-color: #4F46E5 !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 4. RENDER NAVBAR
# ==============================================================================
def render_custom_navbar():
    with st.container():
        st.markdown("""
        <div style="
            position: fixed; top: 0; left: 0; right: 0; z-index: 99999;
            background: #FFFFFF; border-bottom: 1px solid #E5E7EB;
            padding: 14px 40px; display: flex; align-items: center;
            justify-content: space-between;
        ">
            <div style="font-size:1.3rem; font-weight:800; color:#4F46E5; letter-spacing:-0.03em;">
                🎓 DontBe-DO
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tombol navigasi menggunakan columns agar bisa menerima klik
        _, nav_col = st.columns([3, 1])
        with nav_col:
            c1, c2, c3 = st.columns(3)
            with c1:
                active = st.session_state.current_page == "Beranda"
                if st.button("Beranda", key="btn_nav_home", use_container_width=True,
                             type="primary" if active else "secondary"):
                    pindah_halaman("Beranda")
            with c2:
                active = st.session_state.current_page == "Prediksi"
                if st.button("Prediksi", key="btn_nav_pred", use_container_width=True,
                             type="primary" if active else "secondary"):
                    pindah_halaman("Prediksi")
            with c3:
                active = st.session_state.current_page == "Tentang"
                if st.button("Tentang", key="btn_nav_about", use_container_width=True,
                             type="primary" if active else "secondary"):
                    pindah_halaman("Tentang")

render_custom_navbar()

# ==============================================================================
# 5. ROUTING HALAMAN
# ==============================================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if st.session_state.current_page == "Beranda":
    st.markdown("""
    <style>
    .hero-container { max-width: 960px; margin: 40px auto 30px auto; text-align: center; }
    .ews-badge {
        background-color: #EEF2FF; color: #4F46E5; font-size: 0.75rem; font-weight: 700;
        padding: 6px 16px; border-radius: 9999px; display: inline-block; margin-bottom: 20px;
        text-transform: uppercase; border: 1px solid #E0E7FF;
    }
    .hero-title { font-size: 2.8rem; font-weight: 800; color: #111827; line-height: 1.2; margin-bottom: 16px; }
    .hero-title span { color: #4F46E5; }
    .hero-subtitle { font-size: 1.1rem; color: #4B5563; max-width: 720px; margin: 0 auto 32px auto; line-height: 1.6; }
    .concept-card {
        background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 12px; padding: 24px;
        max-width: 960px; margin: 30px auto; box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .concept-title { font-size: 1.2rem; font-weight: 700; color: #111827; margin-bottom: 10px; }
    .concept-desc { font-size: 0.95rem; color: #4B5563; line-height: 1.6; text-align: justify; }
    .how-section { max-width: 960px; margin: 40px auto 60px auto; }
    .how-title { font-size: 1.75rem; font-weight: 800; color: #111827; margin-bottom: 24px; text-align: center; }
    .steps-grid { display: flex; gap: 24px; justify-content: space-between; }
    .step-card { background: #FFFFFF; border: 1px solid #E5E7EB; padding: 24px; border-radius: 12px; flex: 1; }
    .step-number { font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 8px; }
    .step-desc { font-size: 0.88rem; color: #6B7280; line-height: 1.5; }
    .site-footer { text-align: center; padding: 24px 0; font-size: 0.85rem; color: #9CA3AF; border-top: 1px solid #E5E7EB; margin-top: 40px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-container">
        <div class="ews-badge">🛡️ AI-Powered Early Warning System</div>
        <div class="hero-title">Sistem Deteksi Dini Risiko <span>Dropout Mahasiswa</span></div>
        <div class="hero-subtitle">
            Mengidentifikasi kerentanan kelangsungan studi mahasiswa secara prediktif sejak tahun pertama. 
            Menjembatani pencegahan preventif melalui integrasi algoritma Machine Learning dan data sosial-ekonomi.
        </div>
    </div>
    """, unsafe_allow_html=True)

    _, c_btn, _ = st.columns([2, 1, 2])
    with c_btn:
        if st.button("Masuk ke Sistem Evaluasi 🚀", key="btn_hero_enter", use_container_width=True, type="primary"):
            pindah_halaman("Prediksi")

    st.markdown("""
    <div class="concept-card">
        <div class="concept-title">💡 Mengapa Harus Early Warning System (EWS)?</div>
        <div class="concept-desc">
            Intervensi akademik yang paling efektif untuk menekan angka putus studi wajib dilakukan <b>sedini mungkin pada semester awal</b>, sebelum mahasiswa mengambil keputusan final untuk keluar. Menggunakan basis data performa akademik semester 1 dan 2 dari <i>UCI Machine Learning Repository</i>, sistem ini dirancang sebagai instrumen mitigasi bagi program studi untuk mendeteksi indikator kegagalan lebih awal dan menyusun program pendampingan yang tepat sasaran.
        </div>
    </div>

    <div class="how-section">
        <div class="how-title">Bagaimana Sistem Bekerja?</div>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">1. Pengisian Data Fleksibel</div>
                <div class="step-desc">Input data identitas, status finansial/sosial, serta capaian performa akademik secara dinamis menggunakan mode Semester 1 atau Semester 2.</div>
            </div>
            <div class="step-card">
                <div class="step-number">2. Komputasi Probabilitas AI</div>
                <div class="step-desc">Model klasifikasi Random Forest memproses data input, melakukan penyelarasan matriks fitur otomatis, dan menghitung bobot risiko secara objektif.</div>
            </div>
            <div class="step-card">
                <div class="step-number">3. Output & Rekomendasi Klinis</div>
                <div class="step-desc">Sistem menyajikan visualisasi indeks kerawanan, mengelompokkan tingkat risiko, serta mengeluarkan draf rekomendasi tindakan preventif.</div>
            </div>
        </div>
    </div>

    <div class="site-footer">
        © 2026 DontBe-DO Project — Capstone AI Engineer Pijak GM068. All Rights Reserved.
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "Prediksi":
    load_view(os.path.join(BASE_DIR, "views", "prediksi.py"))

elif st.session_state.current_page == "Tentang":
    load_view(os.path.join(BASE_DIR, "views", "tentang.py"))