"""
=============================================================
Real-Time Stock Market Dashboard - VIBRANT EDITION v3
Proyek Capstone: Real-Time Stock Market Streaming Analytics
Saham Timor-Leste: STO.AX, WDS.AX, FDR.AX
=============================================================
Pipeline: API → Kafka → Spark → PostgreSQL → Streamlit
Fitur: KPI, Stock Cards, Price Change Analysis, Charts, Analytics
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", message=".*pandas only supports SQLAlchemy.*")
warnings.filterwarnings("ignore", message=".*When grouping with a length-1 list-like.*")

import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time


# ============================================================
# KONFIGURASI
# ============================================================
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "6797"
POSTGRES_DB = "stock_db"

# Interval pembanding perubahan harga (menit)
# Ubah ke 60 untuk 1 jam, 30 untuk 30 menit, 10 untuk 10 menit
PRICE_CHANGE_INTERVAL_MINUTES = 10


# ============================================================
# PALET WARNA VIBRANT
# ============================================================
COLOR_PRIMARY = "#3b82f6"
COLOR_SECONDARY = "#06b6d4"
COLOR_SUCCESS = "#10b981"
COLOR_WARNING = "#f59e0b"
COLOR_DANGER = "#ef4444"
COLOR_PURPLE = "#8b5cf6"
COLOR_PINK = "#ec4899"

COLOR_TEXT_DARK = "#1e293b"
COLOR_TEXT_MUTED = "#64748b"

COLOR_BG_LIGHT = "#f8fafc"
COLOR_BG_CARD = "#ffffff"

CHART_PALETTE = [
    "#3b82f6", "#10b981", "#f59e0b", "#ef4444",
    "#8b5cf6", "#ec4899", "#06b6d4",
]

STOCK_STYLES = {
    'STO.AX': ('sky', 'blue', '🔵'),
    'WDS.AX': ('emerald', 'green', '🟢'),
    'FDR.AX': ('amber', 'amber', '🟠'),
    'ENI.MI': ('violet', 'blue', '🟣'),
    'ESR.AX': ('pink', 'amber', '🔴'),
}
DEFAULT_STYLE = ('violet', 'blue', '🟣')


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Stock Market Analytics - Timor-Leste",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main { padding: 1rem 2rem; }
    
    .main-header {
        background: linear-gradient(135deg, #3b82f6 0%, #06b6d4 100%);
        padding: 2rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.35);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
    }
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 800;
        color: white !important;
        position: relative;
        z-index: 1;
    }
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
        font-size: 1.1rem;
        color: white !important;
        position: relative;
        z-index: 1;
    }
    
    .kpi-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: transform 0.3s, box-shadow 0.3s;
        position: relative;
        overflow: hidden;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
    }
    .kpi-card.blue::before { background: #3b82f6; }
    .kpi-card.green::before { background: #10b981; }
    .kpi-card.amber::before { background: #f59e0b; }
    .kpi-card.violet::before { background: #8b5cf6; }
    
    .kpi-card h3 {
        margin: 0;
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    .kpi-card .value {
        font-size: 2rem;
        font-weight: 800;
        margin: 0.5rem 0 0 0;
        color: #1e293b;
        line-height: 1.1;
    }
    .kpi-card .delta {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        color: #64748b;
        font-weight: 500;
    }
    
    .stock-card {
        background: #ffffff;
        padding: 1.5rem;
        border-radius: 14px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s;
        position: relative;
        overflow: hidden;
    }
    .stock-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.15);
    }
    .stock-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
    }
    .stock-card.sky::before { background: linear-gradient(90deg, #0ea5e9, #06b6d4); }
    .stock-card.emerald::before { background: linear-gradient(90deg, #10b981, #34d399); }
    .stock-card.amber::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .stock-card.violet::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
    .stock-card.pink::before { background: linear-gradient(90deg, #ec4899, #f472b6); }
    .stock-card.pink::before { background: linear-gradient(90deg, #ec4899, #f472b6); }
    
    .stock-symbol {
        font-size: 0.85rem;
        color: #3b82f6;
        font-weight: 800;
        letter-spacing: 1.2px;
        margin-bottom: 0.3rem;
    }
    .stock-name {
        font-size: 0.85rem;
        color: #64748b;
        margin-bottom: 0.9rem;
        font-weight: 500;
    }
    .stock-price {
        font-size: 1.9rem;
        font-weight: 800;
        color: #1e293b;
        line-height: 1.1;
    }
    .stock-volume {
        font-size: 0.85rem;
        margin-top: 0.7rem;
        font-weight: 600;
        display: inline-block;
        padding: 0.3rem 0.7rem;
        border-radius: 8px;
    }
    .stock-volume.blue { color: #1e40af; background: #dbeafe; }
    .stock-volume.green { color: #065f46; background: #d1fae5; }
    .stock-volume.amber { color: #92400e; background: #fef3c7; }
    
    .section-header {
        background: linear-gradient(90deg, #3b82f6 0%, #06b6d4 50%, #10b981 100%);
        color: white;
        padding: 0.9rem 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0 1rem 0;
        font-weight: 700;
        font-size: 1.15rem;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.25);
        letter-spacing: 0.3px;
    }
    
    .trend-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    .trend-up {
        background: linear-gradient(135deg, #d1fae5, #a7f3d0);
        color: #065f46;
    }
    .trend-down {
        background: linear-gradient(135deg, #fee2e2, #fecaca);
        color: #991b1b;
    }
    .trend-sideways {
        background: linear-gradient(135deg, #fef3c7, #fde68a);
        color: #92400e;
    }
    
    .status-live {
        display: inline-block;
        width: 10px;
        height: 10px;
        background: #10b981;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        50% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 22px;
        border-radius: 8px;
        font-weight: 600;
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #06b6d4) !important;
        color: white !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        border-right: 1px solid #e2e8f0;
    }
    section[data-testid="stSidebar"] h3 { color: #3b82f6; }
    
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE FUNCTIONS
# ============================================================
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )


def query_df(sql, params=None):
    try:
        conn = get_connection()
        return pd.read_sql(sql, conn, params=params)
    except Exception as e:
        st.error(f"Error query: {e}")
        return pd.DataFrame()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("### ⚙️ Controls")
    st.markdown("---")
    
    auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)
    refresh_interval = st.slider("Refresh (detik)", 5, 60, 10, 5)
    
    st.markdown("---")
    st.markdown("### 📊 Filters")
    
    time_range = st.selectbox(
        "Time Range",
        options=[50, 100, 200, 500, 1000],
        index=2,
        format_func=lambda x: f"{x} data points"
    )
    
    df_available_symbols = query_df("SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol;")
    available_symbols = df_available_symbols['symbol'].tolist() if not df_available_symbols.empty else []
    
    selected_symbols = st.multiselect(
        "Pilih Saham",
        options=available_symbols,
        default=available_symbols,
    )
    
    if not selected_symbols:
        selected_symbols = available_symbols
    
    st.markdown("---")
    st.markdown("### ℹ️ Info")
    st.caption(f"🕐 Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    st.caption(f"📊 Aktif: {len(available_symbols)} saham")


# ============================================================
# HEADER
# ============================================================
st.markdown("""
<div class="main-header">
    <h1>📈 Real-Time Stock Market Dashboard</h1>
    <p>🇹🇱 Saham Timor-Leste • API → Kafka → Spark → PostgreSQL</p>
</div>
""", unsafe_allow_html=True)

col_status1, col_status2, col_status3 = st.columns([1, 1, 2])
with col_status1:
    st.markdown('<span class="status-live"></span>**LIVE**', unsafe_allow_html=True)
with col_status2:
    st.caption(f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
with col_status3:
    st.caption(f"🎯 {', '.join(selected_symbols)}")


# ============================================================
# KPI CARDS
# ============================================================
st.markdown('<div class="section-header">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

symbols_list = "','".join(selected_symbols)
df_count = query_df(f"SELECT COUNT(*) as total FROM stock_prices WHERE symbol IN ('{symbols_list}');")
total_records = int(df_count['total'].iloc[0]) if not df_count.empty else 0

df_volume = query_df(f"SELECT COALESCE(SUM(volume), 0) as total_volume FROM stock_prices WHERE symbol IN ('{symbols_list}');")
total_volume = int(df_volume['total_volume'].iloc[0]) if not df_volume.empty else 0

df_windows = query_df("SELECT COUNT(DISTINCT window_start) as total_windows FROM stock_trends;")
total_windows = int(df_windows['total_windows'].iloc[0]) if not df_windows.empty else 0

df_latest_time = query_df("SELECT MAX(inserted_at) as latest FROM stock_prices;")
latest_time = df_latest_time['latest'].iloc[0] if not df_latest_time.empty else None

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="kpi-card blue">
        <h3>📥 Total Records</h3>
        <div class="value">{total_records:,}</div>
        <div class="delta">Data streaming</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card green">
        <h3>📦 Total Volume</h3>
        <div class="value">{total_volume:,}</div>
        <div class="delta">Agregasi volume</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card amber">
        <h3>📊 Aggregation Windows</h3>
        <div class="value">{total_windows}</div>
        <div class="delta">Window 1 menit</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    latest_str = latest_time.strftime('%H:%M:%S') if latest_time else "N/A"
    st.markdown(f"""
    <div class="kpi-card violet">
        <h3>⏱️ Last Data</h3>
        <div class="value">{latest_str}</div>
        <div class="delta">Timestamp terbaru</div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# STOCK CARDS
# ============================================================
st.markdown('<div class="section-header">💰 Last Prices per Saham</div>', unsafe_allow_html=True)

df_latest = query_df(f"""
    SELECT DISTINCT ON (symbol)
        symbol, name, price, volume, inserted_at
    FROM stock_prices
    WHERE symbol IN ('{symbols_list}')
    ORDER BY symbol, inserted_at DESC;
""")

if not df_latest.empty:
    cols = st.columns(len(df_latest))
    for idx, row in df_latest.iterrows():
        with cols[idx]:
            card_class, vol_class, icon = STOCK_STYLES.get(row['symbol'], DEFAULT_STYLE)
            st.markdown(f"""
            <div class="stock-card {card_class}">
                <div class="stock-symbol">{icon} {row['symbol']}</div>
                <div class="stock-name">{row['name']}</div>
                <div class="stock-price">${row['price']:.2f}</div>
                <div class="stock-volume {vol_class}">📊 Vol: {int(row['volume']):,}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.info("⏳ Belum ada data.")


# ============================================================
# SECTION BARU: PERUBAHAN HARGA SIGNIFIKAN (NATIVE STREAMLIT)
# ============================================================
st.markdown('<div class="section-header">🔥 Significant Price Changes</div>', unsafe_allow_html=True)

# Query: ambil harga terbaru dan harga N menit lalu per saham
df_price_change = query_df(f"""
    WITH latest AS (
        SELECT DISTINCT ON (symbol)
            symbol, name, price as current_price, inserted_at as latest_time
        FROM stock_prices
        WHERE symbol IN ('{symbols_list}')
        ORDER BY symbol, inserted_at DESC
    ),
    baseline AS (
        SELECT DISTINCT ON (symbol)
            symbol, price as previous_price, inserted_at as previous_time
        FROM stock_prices
        WHERE symbol IN ('{symbols_list}')
          AND inserted_at <= (NOW() - INTERVAL '{PRICE_CHANGE_INTERVAL_MINUTES} minutes')
        ORDER BY symbol, inserted_at DESC
    )
    SELECT 
        l.symbol,
        l.name,
        b.previous_price,
        l.current_price,
        (l.current_price - b.previous_price) as change_amount,
        ROUND(((l.current_price - b.previous_price) / NULLIF(b.previous_price, 0)) * 100, 2) as change_pct,
        l.latest_time,
        b.previous_time
    FROM latest l
    LEFT JOIN baseline b ON l.symbol = b.symbol
    ORDER BY change_pct DESC NULLS LAST;
""")

# Cek apakah ada data baseline (perbandingan)
has_baseline = not df_price_change.empty and df_price_change['previous_price'].notna().any()

if has_baseline:
    # Filter yang punya baseline (harga sebelumnya tersedia)
    df_display = df_price_change[df_price_change['previous_price'].notna()].copy()
    
    # Saham baru yang belum punya baseline
    df_new = df_price_change[df_price_change['previous_price'].isna()].copy()
    
    # Tentukan kategori trend
    def categorize(pct):
        if pct > 0.01:
            return "📈 RISE"
        elif pct < -0.01:
            return "📉 DOWN"
        else:
            return "➡️ STABLE"
    
    # Proses saham dengan baseline
    if not df_display.empty:
        df_display['Trend'] = df_display['change_pct'].apply(categorize)
        df_display['Harga Sebelumnya'] = df_display['previous_price'].apply(lambda x: f"${x:.2f}")
        df_display['Harga Sekarang'] = df_display['current_price'].apply(lambda x: f"${x:.2f}")
        df_display['Perubahan'] = df_display['change_amount'].apply(lambda x: f"{'+' if x >= 0 else ''}${x:.2f}")
        df_display['Persen'] = df_display['change_pct'].apply(lambda x: f"{'+' if x >= 0 else ''}{x:.2f}%")
        df_display_final = df_display[['symbol', 'name', 'Harga Sebelumnya', 'Harga Sekarang', 'Perubahan', 'Persen', 'Trend']].copy()
    else:
        df_display_final = pd.DataFrame(columns=['symbol', 'name', 'Harga Sebelumnya', 'Harga Sekarang', 'Perubahan', 'Persen', 'Trend'])
    
    # Proses saham baru (tanpa baseline)
    if not df_new.empty:
        df_new['Trend'] = "🆕 BARU"
        df_new['Harga Sebelumnya'] = "—"
        df_new['Harga Sekarang'] = df_new['current_price'].apply(lambda x: f"${x:.2f}")
        df_new['Perubahan'] = "—"
        df_new['Persen'] = "—"
        df_new_final = df_new[['symbol', 'name', 'Harga Sebelumnya', 'Harga Sekarang', 'Perubahan', 'Persen', 'Trend']].copy()
    else:
        df_new_final = pd.DataFrame(columns=['symbol', 'name', 'Harga Sebelumnya', 'Harga Sekarang', 'Perubahan', 'Persen', 'Trend'])
    
    # Gabungkan: saham dengan baseline + saham baru
    df_all = pd.concat([df_display_final, df_new_final], ignore_index=True)
    df_all.columns = ['Saham', 'Kompania', 'Previous Price', 'Current Price', 'Change', 'Percentage', 'Trend']
    
    # Tampilkan tabel
    st.dataframe(
        df_all,
        use_container_width=True,
        hide_index=True
    )
    
    st.caption(f"💡 Comparison of prices **now** vs **{PRICE_CHANGE_INTERVAL_MINUTES} minutes ago** • 🟢 Rise | 🔴 Down | 🟡 Stable | 🆕 New")
    
    # Ringkasan
    st.markdown("#### 📊 Summary of Change")
    
    rising_count = int(len(df_display[df_display['change_pct'] > 0.01])) if not df_display.empty else 0
    falling_count = int(len(df_display[df_display['change_pct'] < -0.01])) if not df_display.empty else 0
    flat_count = int(len(df_display[df_display['change_pct'].abs() <= 0.01])) if not df_display.empty else 0
    new_count = int(len(df_new))
    
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric(label="📈 RISING", value=f"{rising_count} saham")
    with col_b:
        st.metric(label="📉 DOWN", value=f"{falling_count} saham")
    with col_c:
        st.metric(label="➡️ STABLE", value=f"{flat_count} saham")
    with col_d:
        st.metric(label="🆕 NEW", value=f"{new_count} saham")

else:
    # Info jika data historis belum cukup
    df_oldest = query_df(f"""
        SELECT MIN(inserted_at) as oldest FROM stock_prices WHERE symbol IN ('{symbols_list}');
    """)
    oldest_time = df_oldest['oldest'].iloc[0] if not df_oldest.empty else None
    
    if oldest_time:
        elapsed = (datetime.now() - oldest_time).total_seconds() / 60
        st.info(f"""
        ⏳ **Menunggu data historis terkumpul...**
        
        Dibutuhkan minimal **{PRICE_CHANGE_INTERVAL_MINUTES} menit** untuk analisis perubahan harga.
        
        - Data tertua: **{oldest_time.strftime('%Y-%m-%d %H:%M:%S')}**
        - Sudah berjalan: **{elapsed:.1f} menit**
        """)
    else:
        st.info("⏳ Belum ada data. Tunggu Spark Streaming memproses data dari Kafka...")


# ============================================================
# TABS
# ============================================================
st.markdown('<div class="section-header">📈 Charts & Analysis</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📉 Harga Real-Time",
    "📊 Volume & Distribusi",
    "⏱️ Agregasi Window",
    "🧠 Analytics (MA)"
])


# ========== TAB 1 ==========
with tab1:
    df_prices = query_df(f"""
        SELECT symbol, price, volume, inserted_at
        FROM stock_prices
        WHERE symbol IN ('{symbols_list}')
        ORDER BY inserted_at DESC
        LIMIT {time_range};
    """)
    
    if not df_prices.empty:
        df_prices = df_prices.sort_values('inserted_at')
        
        fig_line = px.line(
            df_prices,
            x='inserted_at',
            y='price',
            color='symbol',
            title=f'Pergerakan Harga ({time_range} data terbaru)',
            labels={'inserted_at': 'Waktu', 'price': 'Harga (USD)', 'symbol': 'Saham'},
            markers=True,
            color_discrete_sequence=CHART_PALETTE
        )
        fig_line.update_layout(
            height=500,
            hovermode='x unified',
            plot_bgcolor='rgba(248, 250, 252, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            font=dict(color=COLOR_TEXT_DARK, size=12),
            title_font=dict(size=16, color=COLOR_TEXT_DARK)
        )
        fig_line.update_traces(line=dict(width=3))
        st.plotly_chart(fig_line, use_container_width=True)
        
        fig_vol = px.bar(
            df_prices,
            x='inserted_at',
            y='volume',
            color='symbol',
            title='Volume per Waktu',
            labels={'inserted_at': 'Waktu', 'volume': 'Volume', 'symbol': 'Saham'},
            color_discrete_sequence=CHART_PALETTE
        )
        fig_vol.update_layout(
            height=300,
            plot_bgcolor='rgba(248, 250, 252, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_TEXT_DARK, size=12)
        )
        st.plotly_chart(fig_vol, use_container_width=True)
    else:
        st.info("⏳ Belum ada data.")


# ========== TAB 2 ==========
with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        df_vol = query_df(f"""
            SELECT symbol, SUM(volume) as total_volume
            FROM stock_prices
            WHERE symbol IN ('{symbols_list}')
            GROUP BY symbol
            ORDER BY total_volume DESC;
        """)
        if not df_vol.empty:
            fig_bar = px.bar(
                df_vol,
                x='symbol',
                y='total_volume',
                title='Total Volume per Saham',
                color='symbol',
                labels={'total_volume': 'Volume', 'symbol': 'Saham'},
                text='total_volume',
                color_discrete_sequence=CHART_PALETTE
            )
            fig_bar.update_traces(texttemplate='%{text:,}', textposition='outside')
            fig_bar.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(248, 250, 252, 1)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLOR_TEXT_DARK, size=12)
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    
    with col_b:
        df_dist = query_df(f"""
            SELECT symbol, COUNT(*) as data_points
            FROM stock_prices
            WHERE symbol IN ('{symbols_list}')
            GROUP BY symbol
            ORDER BY data_points DESC;
        """)
        if not df_dist.empty:
            fig_pie = px.pie(
                df_dist,
                names='symbol',
                values='data_points',
                title='Distribusi Data per Saham',
                hole=0.5,
                color_discrete_sequence=CHART_PALETTE
            )
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#ffffff', width=2))
            )
            fig_pie.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color=COLOR_TEXT_DARK, size=12)
            )
            st.plotly_chart(fig_pie, use_container_width=True)


# ========== TAB 3 ==========
with tab3:
    df_trends = query_df(f"""
        SELECT symbol, window_start, avg_price, max_price, min_price, total_volume, data_points
        FROM stock_trends
        WHERE symbol IN ('{symbols_list}')
        ORDER BY window_start DESC
        LIMIT 60;
    """)
    
    if not df_trends.empty:
        df_trends = df_trends.sort_values('window_start')
        
        fig_trend = px.line(
            df_trends,
            x='window_start',
            y='avg_price',
            color='symbol',
            title='Average Price per Window (1 menit)',
            labels={'window_start': 'Window Start', 'avg_price': 'Avg Price (USD)', 'symbol': 'Saham'},
            markers=True,
            color_discrete_sequence=CHART_PALETTE
        )
        fig_trend.update_layout(
            height=450,
            hovermode='x unified',
            plot_bgcolor='rgba(248, 250, 252, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_TEXT_DARK, size=12)
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        with st.expander("📋 Detail Agregasi Window"):
            st.dataframe(
                df_trends.sort_values('window_start', ascending=False),
                use_container_width=True,
                hide_index=True
            )
    else:
        st.info("⏳ Belum ada agregasi.")


# ========== TAB 4 ==========
with tab4:
    df_analytics = query_df("""
        SELECT DISTINCT ON (symbol)
            symbol, ma_5, ma_20, volatility, trend, latest_price, price_change_pct, computed_at
        FROM stock_analytics
        ORDER BY symbol, computed_at DESC;
    """)
    
    if not df_analytics.empty:
        cols = st.columns(len(df_analytics))
        for idx, row in df_analytics.iterrows():
            with cols[idx]:
                trend_class = f"trend-{row['trend'].lower()}"
                trend_icon = {"UP": "📈", "DOWN": "📉", "SIDEWAYS": "➡️"}.get(row['trend'], "➡️")
                card_class, _, _ = STOCK_STYLES.get(row['symbol'], DEFAULT_STYLE)
                st.markdown(f"""
                <div class="stock-card {card_class}">
                    <div class="stock-symbol">{row['symbol']}</div>
                    <div class="stock-price">${row['latest_price']:.2f}</div>
                    <div style="margin: 0.6rem 0;">
                        <span class="trend-badge {trend_class}">{trend_icon} {row['trend']}</span>
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b; margin-top: 0.6rem; line-height: 1.8;">
                        MA-5: <b style="color: #1e293b;">${row['ma_5']:.2f}</b><br>
                        MA-20: <b style="color: #1e293b;">${row['ma_20']:.2f}</b><br>
                        Volatility: <b style="color: #1e293b;">{row['volatility']:.4f}</b>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        fig_ma = go.Figure()
        color_map_ma5 = {"STO.AX": "#3b82f6", "WDS.AX": "#10b981", "FDR.AX": "#f59e0b"}
        color_map_ma20 = {"STO.AX": "#93c5fd", "WDS.AX": "#6ee7b7", "FDR.AX": "#fcd34d"}
        
        for _, row in df_analytics.iterrows():
            fig_ma.add_trace(go.Bar(
                name=f"{row['symbol']} MA-5",
                x=[row['symbol']],
                y=[float(row['ma_5'])],
                marker_color=color_map_ma5.get(row['symbol'], "#8b5cf6"),
                text=f"${row['ma_5']:.2f}",
                textposition='outside'
            ))
            fig_ma.add_trace(go.Bar(
                name=f"{row['symbol']} MA-20",
                x=[row['symbol']],
                y=[float(row['ma_20'])],
                marker_color=color_map_ma20.get(row['symbol'], "#c4b5fd"),
                text=f"${row['ma_20']:.2f}",
                textposition='outside'
            ))
        
        fig_ma.update_layout(
            title='Moving Average (MA-5 vs MA-20)',
            barmode='group',
            height=450,
            yaxis_title='Harga (USD)',
            plot_bgcolor='rgba(248, 250, 252, 1)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color=COLOR_TEXT_DARK, size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_ma, use_container_width=True)
        
        with st.expander("📋 Detail Analytics"):
            st.dataframe(
                df_analytics.sort_values('symbol'),
                use_container_width=True,
                hide_index=True
            )
        
        latest_computed = df_analytics['computed_at'].max()
        st.caption(f"🕐 Analytics terakhir dihitung: {latest_computed}")
    else:
        st.info("⏳ Belum ada data analytics. Jalankan `trend_analysis.py` dulu.")


# ============================================================
# DATA TABLE
# ============================================================
st.markdown('<div class="section-header">📋 Data Terbaru (Raw)</div>', unsafe_allow_html=True)

df_table = query_df(f"""
    SELECT symbol, name, exchange, price, open, high, low, volume, inserted_at
    FROM stock_prices
    WHERE symbol IN ('{symbols_list}')
    ORDER BY inserted_at DESC
    LIMIT 30;
""")

if not df_table.empty:
    st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.info("⏳ Belum ada data.")


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #64748b;">
    <p style="font-size: 0.9rem;">
        🔧 <b>Tech Stack:</b> Python 3.11 | Apache Kafka 3.6.1 | Apache Spark 3.5.0 | PostgreSQL 17 | Streamlit
    </p>
    <p style="font-size: 0.9rem;">
        📊 <b>Pipeline:</b> yfinance API → Kafka Producer → Kafka Topic → Spark Streaming → PostgreSQL → Streamlit
    </p>
    <p style="font-size: 0.9rem;">
        🇹🇱 <b>Konteks:</b> Saham terkait Timor-Leste (Santos STO.AX, Woodside WDS.AX, Finder Energy FDR.AX)
    </p>
    <p style="font-size: 0.8rem; margin-top: 1rem; background: linear-gradient(90deg, #3b82f6, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
        © 2026 Capstone Project - Big Data | S1 Ilmu Komputer
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# AUTO REFRESH
# ============================================================
if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()