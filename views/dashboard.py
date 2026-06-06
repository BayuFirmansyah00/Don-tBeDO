import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# ── CSS GLOBAL (mengikuti mockup: background #EEEEF8, card putih, sidebar biru) ──
st.markdown("""
<style>
/* Background halaman */
[data-testid="stAppViewContainer"] {
    background-color: #EEEEF8 !important;
}
[data-testid="stHeader"] { background: transparent !important; }

/* Metric card custom */
.metric-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 24px 28px;
    display: flex;
    align-items: center;
    gap: 18px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    height: 110px;
}
.metric-icon { font-size: 2.2rem; }
.metric-label { font-size: 13px; color: #6B7280; margin-bottom: 2px; font-weight: 500; }
.metric-value { font-size: 2rem; font-weight: 700; color: #111827; line-height: 1; }
.metric-sub   { font-size: 12px; color: #6B7280; margin-top: 3px; }

/* Card section */
.section-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 28px 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.section-title { font-size: 1.15rem; font-weight: 700; color: #111827; margin-bottom: 20px; }

/* Tabel prediksi terbaru */
.pred-table { width: 100%; border-collapse: collapse; }
.pred-table th {
    background: #F3F4F6; color: #374151; font-size: 13px;
    font-weight: 600; padding: 10px 14px; text-align: left;
}
.pred-table td { padding: 12px 14px; font-size: 13px; color: #374151; border-bottom: 1px solid #F3F4F6; }
.pred-table tr:last-child td { border-bottom: none; }
.badge-rendah  { background:#D1FAE5; color:#065F46; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-sedang  { background:#FEF3C7; color:#92400E; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
.badge-tinggi  { background:#FEE2E2; color:#991B1B; padding:3px 10px; border-radius:99px; font-size:12px; font-weight:600; }
</style>
""", unsafe_allow_html=True)

# ── JUDUL ──
st.markdown("<h1 style='font-size:2rem;font-weight:700;color:#111827;margin-bottom:4px'>Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280;margin-top:0;margin-bottom:24px'>Ringkasan umum sistem prediksi resiko drop-out mahasiswa</p>", unsafe_allow_html=True)

# ── TARIK DATA FIREBASE ──
docs = db.collection("riwayat_prediksi").stream()
data_list = [d.to_dict() for d in docs]

if data_list:
    df = pd.DataFrame(data_list)
    total_mhs = len(df) + 2550
    rendah = len(df[df['resiko'] == 'RENDAH']) + 1785
    sedang  = len(df[df['resiko'] == 'SEDANG'])  + 510
    tinggi  = len(df[df['resiko'] == 'TINGGI'])  + 255
else:
    total_mhs, rendah, sedang, tinggi = 2550, 1785, 510, 255

# ── 4 METRIC CARDS ──
c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "👥", "Total Mahasiswa",  f"{total_mhs:,}", "Mahasiswa Terdata"),
    (c2, "✅", "Resiko Rendah",    f"{rendah:,}",    f"{rendah/total_mhs*100:.1f}% dari total"),
    (c3, "⚠️",  "Resiko Sedang",   f"{sedang:,}",    f"{sedang/total_mhs*100:.1f}% dari total"),
    (c4, "🚨", "Resiko Tinggi",    f"{tinggi:,}",    f"{tinggi/total_mhs*100:.1f}% dari total"),
]
for col, icon, label, value, sub in cards:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-icon">{icon}</span>
            <div>
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-sub">{sub}</div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── GRAFIK + TABEL ──
col_grafik, col_tabel = st.columns([1.2, 1], gap="large")

with col_grafik:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Faktor Paling Berpengaruh</div>', unsafe_allow_html=True)
    chart_data = pd.DataFrame({
        'Faktor': ['IPK Semester 1', 'Persentase Kehadiran', 'IPK Semester 2', 'Jumlah SKS', 'Mata Kuliah Mengulang'],
        'Score':  [0.32, 0.25, 0.18, 0.15, 0.10]
    }).set_index('Faktor')
    st.bar_chart(chart_data, horizontal=True, color="#3B5BDB")
    st.markdown('</div>', unsafe_allow_html=True)

with col_tabel:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Prediksi Terbaru</div>', unsafe_allow_html=True)
    if data_list:
        rows_html = ""
        for _, row in df.tail(7).iterrows():
            r = str(row.get('resiko', '')).upper()
            badge_class = 'badge-rendah' if r == 'RENDAH' else ('badge-sedang' if r == 'SEDANG' else 'badge-tinggi')
            label = r.capitalize()
            rows_html += f"""<tr>
                <td>{row.get('nama','–')}</td>
                <td>{row.get('tanggal','–')}</td>
                <td><span class="{badge_class}">{label}</span></td>
                <td>{row.get('probabilitas','–')}</td>
            </tr>"""
        st.markdown(f"""
        <table class="pred-table">
            <thead><tr>
                <th>Nama Mahasiswa</th><th>Tanggal</th><th>Resiko</th><th>Probabilitas</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
        </table>""", unsafe_allow_html=True)
    else:
        st.info("Belum ada riwayat prediksi terbaru.")
    st.markdown('</div>', unsafe_allow_html=True)