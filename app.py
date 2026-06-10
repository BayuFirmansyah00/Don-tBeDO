import streamlit as st

# ==============================================================================
# KONFIGURASI HALAMAN
# ==============================================================================
st.set_page_config(
    page_title="DontBe-DO | Prediksi Risiko Dropout Mahasiswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# HALAMAN NAVIGASI
# ==============================================================================
prediksi_page = st.Page("views/prediksi.py", title="Prediksi Dropout", icon="🔮")
tentang_page  = st.Page("views/tentang.py",  title="Tentang",          icon="ℹ️")

if "enter_system" not in st.session_state:
    st.session_state.enter_system = False

if st.session_state.enter_system:
    pg = st.navigation({
        "Menu": [prediksi_page, tentang_page]
    })
    pg.run()
else:
    # ══════════════════════════════════════════════════════════════════════════
    # CSS GLOBAL BERANDA – meniru desain mockup persis
    # ══════════════════════════════════════════════════════════════════════════
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #FFFFFF !important;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    [data-testid="stHeader"]     { display: none !important; }
    [data-testid="stSidebar"]    { display: none !important; }
    .block-container             { padding: 0 !important; max-width: 100% !important; }
    footer                       { display: none !important; }

    /* ── NAV ── */
    .navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 20px 72px;
        border-bottom: 1px solid #E5E7EB;
        background: #FFFFFF;
    }
    .nav-brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #1D77E6;
        letter-spacing: -0.5px;
    }
    .nav-links { display: flex; gap: 36px; align-items: center; }
    .nav-link  {
        font-size: 0.95rem;
        font-weight: 500;
        color: #111827;
        text-decoration: none;
        cursor: pointer;
    }
    .nav-link.active { color: #1D77E6; font-weight: 600; }

    /* ── HERO ── */
    .hero-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 72px 72px 60px;
        max-width: 1200px;
        margin: 0 auto;
        gap: 48px;
    }
    .hero-left { flex: 1; }
    .hero-right { flex: 0 0 420px; }

    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: #111827;
        line-height: 1.18;
        letter-spacing: -1px;
        margin-bottom: 20px;
    }
    .hero-title .accent { color: #1D77E6; }

    .hero-subtitle {
        font-size: 1.05rem;
        color: #4B5563;
        line-height: 1.7;
        max-width: 480px;
        margin-bottom: 36px;
    }

    .hero-buttons { display: flex; gap: 16px; flex-wrap: wrap; margin-bottom: 40px; }
    .btn-primary {
        background: #1D77E6;
        color: #FFFFFF;
        border: none;
        border-radius: 8px;
        padding: 14px 28px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .btn-outline {
        background: transparent;
        color: #1D77E6;
        border: 1.5px solid #1D77E6;
        border-radius: 8px;
        padding: 13px 28px;
        font-size: 1rem;
        font-weight: 700;
        cursor: pointer;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .trust-badges { display: flex; gap: 28px; flex-wrap: wrap; }
    .badge-item   { display: flex; align-items: center; gap: 6px; font-size: 0.88rem; color: #6B7280; font-weight: 500; }

    /* Hero illustration placeholder */
    .hero-illustration {
        width: 100%;
        height: 300px;
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 7rem;
    }

    /* ── SEPARATOR ── */
    .section-divider {
        border: none;
        border-top: 1px solid #E5E7EB;
        margin: 0;
    }

    /* ── HOW IT WORKS ── */
    .how-section {
        padding: 72px 72px;
        background: #FAFAFA;
        text-align: center;
    }
    .how-badge {
        font-size: 0.8rem;
        font-weight: 700;
        color: #1D77E6;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .how-title {
        font-size: 2.1rem;
        font-weight: 800;
        color: #111827;
        margin-bottom: 48px;
        letter-spacing: -0.5px;
    }
    .steps-grid { display: flex; gap: 28px; justify-content: center; flex-wrap: wrap; max-width: 1100px; margin: 0 auto; }
    .step-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 32px 28px;
        flex: 1;
        min-width: 260px;
        max-width: 320px;
        text-align: left;
        border-bottom: 3px solid #1D77E6;
    }
    .step-number {
        font-size: 1rem;
        font-weight: 700;
        color: #1D77E6;
        margin-bottom: 12px;
    }
    .step-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #111827;
        margin-bottom: 10px;
    }
    .step-desc { font-size: 0.92rem; color: #6B7280; line-height: 1.65; }

    /* ── FOOTER ── */
    .site-footer {
        border-top: 1px solid #E5E7EB;
        padding: 28px 72px;
        text-align: center;
        font-size: 0.85rem;
        color: #9CA3AF;
        background: #FFFFFF;
    }

    /* Override Streamlit button styles */
    div[data-testid="stButton"] > button {
        background: #1D77E6 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 14px 28px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        cursor: pointer !important;
        width: auto !important;
    }
    div[data-testid="stButton"] > button:hover {
        background: #1560C4 !important;
        border: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── NAVBAR ──
    st.markdown("""
    <div class="navbar">
        <div class="nav-brand">DontBe–DO</div>
        <div class="nav-links">
            <span class="nav-link active">Beranda</span>
            <span class="nav-link">Tentang</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HERO SECTION ──
    st.markdown("""
    <div class="hero-section">
        <div class="hero-left">
            <div class="hero-title">
                Prediksi Dini Risiko<br>
                <span class="accent">Mahasiswa Dropout</span><br>
                Menggunakan AI
            </div>
            <p class="hero-subtitle">
                DontBe-DO menganalisis data akademik, sosial, dan ekonomi siswa untuk
                mengidentifikasi mahasiswa yang berisiko sejak dini, sehingga memungkinkan
                dilakukannya intervensi yang lebih tepat sasaran
            </p>
            <div class="trust-badges">
                <span class="badge-item">🤖 AI-Powered</span>
                <span class="badge-item">⚡ Instant Result</span>
                <span class="badge-item">👤 No Sign-up</span>
                <span class="badge-item">✨ Free to Use</span>
            </div>
        </div>
        <div class="hero-right">
            <div class="hero-illustration">🎓</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tombol aksi CTA
    col1, col2, col3 = st.columns([2, 1, 3])
    with col1:
        if st.button("Mulai Prediksi", key="hero_cta"):
            st.session_state.enter_system = True
            st.rerun()
    with col2:
        st.markdown("""
        <button class="btn-outline" onclick="">Pelajari Lebih Lanjut</button>
        """, unsafe_allow_html=True)

    # ── HOW IT WORKS ──
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="how-section">
        <div class="how-badge">3 LANGKAH MUDAH</div>
        <div class="how-title">Bagaimana Menggunakannya?</div>
        <div class="steps-grid">
            <div class="step-card">
                <div class="step-number">1. Masukkan Data Mahasiswa</div>
                <div class="step-desc">
                    Isi data akademik dan informasi pendukung mahasiswa pada formulir prediksi
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">2. Dapatkan Prediksi Instan</div>
                <div class="step-desc">
                    Klik tombol "Prediksi" untuk mendapatkan analisis instan yang didukung oleh
                    kecerdasan buatan mengenai risiko dropout, berdasarkan faktor akademik, sosial-ekonomi
                </div>
            </div>
            <div class="step-card">
                <div class="step-number">3. Lihat Hasil Prediksi</div>
                <div class="step-desc">
                    Lihat hasil prediksi dropout disesuaikan dengan risiko yang anda masukkan
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── FOOTER ──
    st.markdown("""
    <div class="site-footer">
        © 2026 DontBe-DO All right reserved
    </div>
    """, unsafe_allow_html=True)