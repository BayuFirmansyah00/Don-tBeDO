import streamlit as st
import pandas as pd
import numpy as np

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #EEEEF8 !important; }
[data-testid="stHeader"]            { background: transparent !important; }

.chart-card {
    background: #FFFFFF; border-radius: 16px;
    padding: 26px 28px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    height: 100%;
}
.chart-title {
    font-size: 1rem; font-weight: 700; color: #111827; margin-bottom: 18px;
}
/* Donut chart placeholder */
.donut-wrap {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; min-height: 220px; gap: 16px;
}
.legend-row { display: flex; gap: 20px; flex-wrap: wrap; justify-content: center; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; color: #374151; }
.legend-dot  { width: 10px; height: 10px; border-radius: 50%; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size:2rem;font-weight:700;color:#111827;margin-bottom:4px'>📊 Statistik Pola Data</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#6B7280;margin-top:0;margin-bottom:24px'>Lihat Ringkasan Data dan Pola yang mempengaruhi Resiko Drop-out Mahasiswa</p>", unsafe_allow_html=True)

# ── LOAD DATASET ──
DATA_PATH = "data/dataset_encoded.csv"
try:
    import os
    if os.path.exists(DATA_PATH):
        df_raw = pd.read_csv(DATA_PATH)
        has_data = True
    else:
        has_data = False
except Exception:
    has_data = False

# ── BARIS 1: Distribusi Resiko + IPK Semester 1 ──
row1_left, row1_right = st.columns(2, gap="medium")

with row1_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi Resiko Drop-out</div>', unsafe_allow_html=True)
    if has_data:
        counts = df_raw['Target'].value_counts().sort_index()
        label_map = {0: 'Dropout', 1: 'Enrolled', 2: 'Graduate'}
        pie_df = pd.DataFrame({
            'Status': [label_map.get(i, i) for i in counts.index],
            'Jumlah': counts.values
        })
        # Gunakan st.bar_chart sebagai fallback pie chart (Streamlit tidak support native pie)
        # Tampilkan sebagai horizontal bar yang proporsional
        total = pie_df['Jumlah'].sum()
        colors = ['#EF4444', '#F59E0B', '#10B981']
        for idx, row in pie_df.iterrows():
            pct = row['Jumlah'] / total * 100
            col_style = colors[idx % len(colors)]
            st.markdown(f"""
            <div style="margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px">
                    <span style="font-weight:600;color:#374151">{row['Status']}</span>
                    <span style="color:#6B7280">{row['Jumlah']:,} ({pct:.1f}%)</span>
                </div>
                <div style="background:#F3F4F6;border-radius:99px;height:10px">
                    <div style="width:{pct}%;background:{col_style};border-radius:99px;height:10px"></div>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        # Data dummy mockup
        for label, val, pct, color in [("Dropout","2.209","33.3%","#EF4444"),("Enrolled","2.209","33.3%","#F59E0B"),("Graduate","2.209","33.3%","#10B981")]:
            st.markdown(f"""
            <div style="margin-bottom:10px">
                <div style="display:flex;justify-content:space-between;font-size:13px;margin-bottom:4px">
                    <span style="font-weight:600;color:#374151">{label}</span>
                    <span style="color:#6B7280">{val} ({pct})</span>
                </div>
                <div style="background:#F3F4F6;border-radius:99px;height:10px">
                    <div style="width:33.3%;background:{color};border-radius:99px;height:10px"></div>
                </div>
            </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with row1_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi Berdasarkan IPK Semester 1</div>', unsafe_allow_html=True)
    if has_data:
        grade_col = "Curricular units 1st sem (grade)"
        # Konversi grade UCI (0-20) ke IPK (0-4)
        df_raw['ipk_approx'] = df_raw[grade_col] / 20 * 4
        bins   = [0, 2.0, 2.75, 3.25, 4.01]
        labels = ['< 2.00', '2.00 – 2.75', '2.76 – 3.25', '3.26 – 4.00']
        df_raw['ipk_bin'] = pd.cut(df_raw['ipk_approx'], bins=bins, labels=labels, right=False)
        dist = df_raw['ipk_bin'].value_counts().reindex(labels).fillna(0)
        total = dist.sum()
        chart_df = pd.DataFrame({'Persen (%)': (dist / total * 100).round(1)})
        st.bar_chart(chart_df, color="#3B5BDB")
    else:
        chart_df = pd.DataFrame({'Persen (%)': [7, 27, 35, 26]},
                                 index=['< 2.00','2.00 – 2.75','2.76 – 3.25','3.26 – 4.00'])
        st.bar_chart(chart_df, color="#3B5BDB")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── BARIS 2: Kehadiran + Matkul Mengulang ──
row2_left, row2_right = st.columns(2, gap="medium")

with row2_left:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi Berdasarkan Kehadiran</div>', unsafe_allow_html=True)
    if has_data:
        # Proxy kehadiran dari Daytime/evening attendance
        attend_col = "Daytime/evening attendance"
        if attend_col in df_raw.columns:
            dist = df_raw[attend_col].value_counts()
            attend_df = pd.DataFrame({
                'Jumlah Mahasiswa': dist.values
            }, index=['Kelas Pagi' if i == 1 else 'Kelas Malam' for i in dist.index])
            st.bar_chart(attend_df, color="#3B5BDB")
        else:
            st.info("Kolom kehadiran tidak tersedia di dataset.")
    else:
        attend_df = pd.DataFrame({'Jumlah Mahasiswa': [5200, 1400]},
                                  index=['Kelas Pagi (≥75%)', 'Kelas Malam (<75%)'])
        st.bar_chart(attend_df, color="#3B5BDB")
    st.markdown('</div>', unsafe_allow_html=True)

with row2_right:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">Distribusi Berdasarkan Jumlah Mata Kuliah Mengulang</div>', unsafe_allow_html=True)
    if has_data:
        # Matkul tidak lulus = enrolled - approved sem2
        df_raw['matkul_ulang'] = (
            df_raw['Curricular units 2nd sem (enrolled)'] -
            df_raw['Curricular units 2nd sem (approved)']
        ).clip(lower=0)
        bins2   = [-0.1, 0, 1, 3, 100]
        labels2 = ['0 (Lulus Semua)', '1 Matkul', '2–3 Matkul', '> 3 Matkul']
        df_raw['ulang_bin'] = pd.cut(df_raw['matkul_ulang'], bins=bins2, labels=labels2)
        dist2 = df_raw['ulang_bin'].value_counts().reindex(labels2).fillna(0)
        ulang_df = pd.DataFrame({'Jumlah Mahasiswa': dist2.values}, index=labels2)
        st.bar_chart(ulang_df, color="#3B5BDB")
    else:
        ulang_df = pd.DataFrame({'Jumlah Mahasiswa': [3800, 1200, 900, 330]},
                                 index=['0 (Lulus Semua)','1 Matkul','2–3 Matkul','> 3 Matkul'])
        st.bar_chart(ulang_df, color="#3B5BDB")
    st.markdown('</div>', unsafe_allow_html=True)