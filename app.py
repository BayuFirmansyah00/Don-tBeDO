import streamlit as st

# ==============================================================================
# 1. KONFIGURASI HALAMAN & TEMA UTAMA
# ==============================================================================
st.set_page_config(
    page_title="Drop-out Prediction System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. SISTEM NAVIGASI MULTI-PAGE (MENGACU PADA MOCKUP)
# ==============================================================================
dashboard_page = st.Page("views/dashboard.py", title="Dashboard", icon="🏠")
prediksi_page = st.Page("views/prediksi.py", title="Prediksi Mahasiswa", icon="👤")
statistik_page = st.Page("views/statistik.py", title="Statistik", icon="📊")
riwayat_page = st.Page("views/riwayat.py", title="Riwayat Prediksi", icon="📝")
tentang_page = st.Page("views/tentang.py", title="Tentang", icon="ℹ️")


if "enter_system" not in st.session_state:
    st.session_state.enter_system = False

if st.session_state.enter_system:
    pg = st.navigation({
        "Menu Utama": [dashboard_page, prediksi_page, statistik_page, riwayat_page, tentang_page]
    })
    pg.run()
else:
    # ==============================================================================
    # 3. TAMPILAN LANDING PAGE (JIKA BELUM MASUK SISTEM)
    # ==============================================================================

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        # Header Utama Landing Page
        st.textAlign = "center"
        st.markdown("<h1 style='text-align: center; color: #1E3A8A;'>🎓 Sistem Prediksi Risiko Drop-out Mahasiswa</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 18px; color: #4B5563;'>Platform Analisis Deteksi Dini Potensi Putus Studi Berdasarkan Indikator Akademik dan Kondisi Sosial-Ekonomi Mahasiswa.</p>", unsafe_allow_html=True)
        st.markdown("---")
        
        st.markdown("### 💡 Tentang Platform")
        st.write(
            "Sistem ini dirancang khusus untuk membantu program studi dan manajemen institusi pendidikan "
            "dalam melakukan intervensi dini. Menggunakan algoritma **Random Forest Classifier** yang dilatih "
            "dengan data historis, sistem mampu memprediksi status kelulusan mahasiswa secara akurat."
        )
        
        # Fitur Utama Aplikasi
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            st.info("**📊 Dashboard Monitor**\nMelihat ringkasan total risiko mahasiswa terdata secara real-time.")
        with col_f2:
            st.info("**🔮 Prediksi Akurat**\nInput indikator mahasiswa untuk melihat probabilitas risiko drop-out.")
        with col_f3:
            st.info("**☁️ Firebase Storage**\nSeluruh riwayat hasil komputasi prediksi langsung tersimpan aman di cloud.")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # TOMBOL AKSI UTAMA (CTA) - PINTU MASUK TANPA LOGIN
        st.write("###")
        btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
        with btn_col2:
            if st.button("🚀 MASUK KE DASHBOARD SISTEM", use_container_width=True, type="primary"):
                st.session_state.enter_system = True
                st.rerun()
                
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 12px; color: #9CA3AF;'>Capstone Project Team AI Engineer - Pijak 2026</p>", unsafe_allow_html=True)