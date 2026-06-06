import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

if not firebase_admin._apps:
    cred = credentials.Certificate("firebase-key.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #EEEEF8 !important; }
[data-testid="stHeader"]            { background: transparent !important; }

.metric-card {
    background: #FFFFFF; border-radius: 16px; padding: 22px 24px;
    display: flex; align-items: center; gap: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); height: 100px;
}
.metric-icon  { font-size: 2rem; }
.metric-label { font-size: 12px; color: #6B7280; font-weight: 500; }
.metric-value { font-size: 1.8rem; font-weight: 800; color: #111827; line-height: 1.1; }
.metric-sub   { font-size: 11px; color: #6B7280; margin-top: 2px; }

.table-card {
    background: #FFFFFF; border-radius: 16px; padding: 28px 32px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06); margin-top: 4px;
}
.table-header-row {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 20px; flex-wrap: wrap; gap: 12px;
}
.table-title { font-size: 1.1rem; font-weight: 700; color: #111827; }

.riwayat-table { width:100%; border-collapse:collapse; }
.riwayat-table th {
    background:#F9FAFB; color:#374151; font-size:13px;
    font-weight:600; padding:12px 14px; text-align:left;
    border-bottom: 2px solid #E5E7EB;
}
.riwayat-table td {
    padding: 13px 14px; font-size:13px; color:#374151;
    border-bottom: 1px solid #F3F4F6;
}
.riwayat-table tr:last-child td { border-bottom: none; }
.riwayat-table tr:hover td { background:#FAFAFA; }
.no-cell { color:#9CA3AF; font-weight:600; }
.name-bold { font-weight:600; color:#111827; }
.prob-bold { font-weight:700; }
.prob-rendah { color:#16A34A; }
.prob-sedang { color:#D97706; }
.prob-tinggi { color:#DC2626; }

.badge-rendah { background:#D1FAE5;color:#065F46;padding:3px 12px;border-radius:99px;font-size:12px;font-weight:600; }
.badge-sedang { background:#FEF3C7;color:#92400E;padding:3px 12px;border-radius:99px;font-size:12px;font-weight:600; }
.badge-tinggi { background:#FEE2E2;color:#991B1B;padding:3px 12px;border-radius:99px;font-size:12px;font-weight:600; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:2rem;font-weight:700;color:#111827;margin-bottom:4px'>Riwayat Prediksi</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280;margin-top:0;margin-bottom:24px'>Berikut adalah Riwayat Prediksi Resiko Drop-out Mahasiswa</p>", unsafe_allow_html=True)

# ── TARIK DATA ──
docs = db.collection("riwayat_prediksi").stream()
data_list = [d.to_dict() for d in docs]

if data_list:
    df = pd.DataFrame(data_list)
    total_pred = len(df)
    rendah = len(df[df['resiko'] == 'RENDAH'])
    sedang  = len(df[df['resiko'] == 'SEDANG'])
    tinggi  = len(df[df['resiko'] == 'TINGGI'])
else:
    total_pred, rendah, sedang, tinggi = 0, 0, 0, 0

# ── 4 METRIC CARDS ──
c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "👥", "Total Prediksi",   f"{total_pred:,}", "Data prediksi tersimpan"),
    (c2, "✅", "Resiko Rendah",    f"{rendah:,}",    f"{rendah/total_pred*100:.1f}% dari total" if total_pred else "0% dari total"),
    (c3, "⚠️",  "Resiko Sedang",   f"{sedang:,}",    f"{sedang/total_pred*100:.1f}% dari total"  if total_pred else "0% dari total"),
    (c4, "🚨", "Resiko Tinggi",    f"{tinggi:,}",    f"{tinggi/total_pred*100:.1f}% dari total"  if total_pred else "0% dari total"),
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

# ── TABEL RIWAYAT ──
st.markdown('<div class="table-card">', unsafe_allow_html=True)

if data_list:
    col_title, col_search, col_export = st.columns([2, 1.5, 0.8])
    with col_title:
        st.markdown('<div class="table-title">Riwayat Prediksi Mahasiswa</div>', unsafe_allow_html=True)
    with col_search:
        search = st.text_input("", placeholder="🔍  Cari nama mahasiswa", label_visibility="collapsed")
    with col_export:
        df_exp = df.copy()
        if 'nama' in df_exp.columns:
            csv = df_exp.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Export CSV", data=csv, file_name="riwayat_dropout.csv", mime="text/csv", use_container_width=True)

    # Filter pencarian
    df_show = df.copy()
    if search:
        df_show = df_show[df_show['nama'].str.contains(search, case=False, na=False)]
    df_show = df_show.reset_index(drop=True)

    # Render tabel HTML
    rows_html = ""
    for i, row in df_show.iterrows():
        r = str(row.get('resiko', '')).upper()
        badge = f'<span class="badge-{r.lower()}">{r.capitalize()}</span>' if r in ["RENDAH","SEDANG","TINGGI"] else r
        prob_class = f"prob-{r.lower()}" if r in ["RENDAH","SEDANG","TINGGI"] else ""
        rows_html += f"""<tr>
            <td class="no-cell">{i+1}</td>
            <td class="name-bold">{row.get('nama','–')}</td>
            <td>{row.get('tanggal','–')}</td>
            <td>{row.get('ipk_sem_1','–')}</td>
            <td>{row.get('ipk_sem_2','–')}</td>
            <td>{row.get('kehadiran','–')}</td>
            <td>{badge}</td>
            <td class="prob-bold {prob_class}">{row.get('probabilitas','–')}</td>
        </tr>"""

    st.markdown(f"""
    <table class="riwayat-table">
        <thead><tr>
            <th>No</th>
            <th>Nama Mahasiswa</th>
            <th>Tanggal Prediksi</th>
            <th>IPK Smt 1</th>
            <th>IPK Smt 2</th>
            <th>Kehadiran (%)</th>
            <th>Resiko</th>
            <th>Probabilitas</th>
        </tr></thead>
        <tbody>{rows_html}</tbody>
    </table>""", unsafe_allow_html=True)
else:
    st.info("Database Firebase masih kosong, belum ada data riwayat prediksi.")

st.markdown('</div>', unsafe_allow_html=True)