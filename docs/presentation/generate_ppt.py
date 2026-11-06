"""
Generate PowerPoint Presentation untuk Capstone Project
Real-Time Stock Market Streaming Analytics
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime
import os


# ============================================================
# KONFIGURASI WARNA
# ============================================================
COLOR_PRIMARY = RGBColor(0x3b, 0x82, 0xf6)      # Blue
COLOR_SECONDARY = RGBColor(0x06, 0xb6, 0xd4)    # Teal
COLOR_SUCCESS = RGBColor(0x10, 0xb9, 0x81)      # Green
COLOR_WARNING = RGBColor(0xf5, 0x9e, 0x0b)      # Amber
COLOR_DANGER = RGBColor(0xef, 0x44, 0x44)       # Red
COLOR_PURPLE = RGBColor(0x8b, 0x5c, 0xf6)       # Purple
COLOR_PINK = RGBColor(0xec, 0x48, 0x99)         # Pink
COLOR_DARK = RGBColor(0x1e, 0x29, 0x3b)         # Slate dark
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8b)        # Slate muted
COLOR_WHITE = RGBColor(0xff, 0xff, 0xff)
COLOR_BG = RGBColor(0xf8, 0xfa, 0xfc)           # Slate light


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def add_gradient_header(slide, title, subtitle=""):
    """Tambah header dengan gradient blue-teal."""
    # Background rectangle
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        Inches(13.333), Inches(1.5)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = COLOR_PRIMARY
    header.line.fill.background()
    
    # Title
    title_box = slide.shapes.add_textbox(
        Inches(0.5), Inches(0.3),
        Inches(12), Inches(0.8)
    )
    tf = title_box.text_frame
    tf.text = title
    p = tf.paragraphs[0]
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE
    
    # Subtitle
    if subtitle:
        sub_box = slide.shapes.add_textbox(
            Inches(0.5), Inches(1.0),
            Inches(12), Inches(0.4)
        )
        tf = sub_box.text_frame
        tf.text = subtitle
        p = tf.paragraphs[0]
        p.font.size = Pt(14)
        p.font.color.rgb = COLOR_WHITE


def add_section_header(slide, text, color=COLOR_PRIMARY):
    """Tambah section header dengan warna."""
    header = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(0.5), Inches(1.8),
        Inches(12.333), Inches(0.6)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = color
    header.line.fill.background()
    
    tf = header.text_frame
    tf.text = text
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = COLOR_WHITE


def add_bullet_text(slide, items, top=2.6, left=0.5, width=12.333, font_size=14):
    """Tambah bullet list."""
    textbox = slide.shapes.add_textbox(
        Inches(left), Inches(top),
        Inches(width), Inches(5)
    )
    tf = textbox.text_frame
    tf.word_wrap = True
    
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        
        p.text = item
        p.font.size = Pt(font_size)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(8)


def add_table(slide, data, top=2.6, left=0.5, width=12.333, col_widths=None):
    """Tambah tabel."""
    rows = len(data)
    cols = len(data[0])
    
    table_shape = slide.shapes.add_table(
        rows, cols,
        Inches(left), Inches(top),
        Inches(width), Inches(0.4 * rows)
    )
    table = table_shape.table
    
    # Set column widths
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    
    # Fill data
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            
            # Header row
            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_PRIMARY
                p = cell.text_frame.paragraphs[0]
                p.font.bold = True
                p.font.size = Pt(12)
                p.font.color.rgb = COLOR_WHITE
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = COLOR_WHITE if r % 2 == 0 else COLOR_BG
                p = cell.text_frame.paragraphs[0]
                p.font.size = Pt(11)
                p.font.color.rgb = COLOR_DARK


def add_footer(slide, slide_num, total=16):
    """Tambah footer dengan nomor slide."""
    footer = slide.shapes.add_textbox(
        Inches(0.5), Inches(7.0),
        Inches(12.333), Inches(0.3)
    )
    tf = footer.text_frame
    tf.text = f"Real-Time Stock Market Analytics | Slide {slide_num}/{total}"
    p = tf.paragraphs[0]
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.RIGHT


# ============================================================
# INISIALISASI PRESENTASI
# ============================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]


# ============================================================
# SLIDE 1: JUDUL
# ============================================================
slide = prs.slides.add_slide(blank_layout)

# Gradient background
bg = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0), Inches(0),
    Inches(13.333), Inches(7.5)
)
bg.fill.solid()
bg.fill.fore_color.rgb = COLOR_PRIMARY
bg.line.fill.background()

# Judul
title_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(2.0),
    Inches(12.333), Inches(1.5)
)
tf = title_box.text_frame
tf.text = "Real-Time Stock Market Streaming Analytics"
p = tf.paragraphs[0]
p.font.size = Pt(40)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

# Subjudul
sub_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(3.5),
    Inches(12.333), Inches(0.6)
)
tf = sub_box.text_frame
tf.text = "Using Apache Kafka and Apache Spark"
p = tf.paragraphs[0]
p.font.size = Pt(24)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

# Info
info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(4.8),
    Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "Analisis Real-Time Saham Terkait Timor-Leste"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

p = tf.add_paragraph()
p.text = "Pipeline: API → Kafka → Spark → PostgreSQL → Streamlit"
p.font.size = Pt(14)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(12)

p = tf.add_paragraph()
p.text = f"Nama: [Nama Anda] | NIM: [NIM] | {datetime.now().year}"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(20)


# ============================================================
# SLIDE 2: AGENDA
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "📋 Agenda Presentasi", "8 Bagian Utama")

agenda = [
    "1. Overview Pipeline — Arsitektur Big Data end-to-end",
    "2. Data Source (API) — Sumber data & metode pengambilan",
    "3. Stream Processing — Kafka & Spark Streaming",
    "4. Data Storage — PostgreSQL & skema database",
    "5. Big Data Analytics — Trend Analysis & Moving Average",
    "6. Visualization — Dashboard Streamlit",
    "7. 5 Saham Terkait Timor-Leste — Profil & hubungan",
    "8. Demo & Kesimpulan",
]
add_bullet_text(slide, agenda, top=2.6, font_size=16)
add_footer(slide, 2)


# ============================================================
# SLIDE 3: PIPELINE OVERVIEW
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🏗️ Arsitektur Big Data Pipeline", "5 Layer Utama")

# Layer 1
layer1 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(1.9), Inches(12.333), Inches(0.9)
)
layer1.fill.solid()
layer1.fill.fore_color.rgb = COLOR_PRIMARY
layer1.line.fill.background()
tf = layer1.text_frame
tf.text = "1. DATA SOURCE (API) — yfinance → 5 Saham TL"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

# Arrow
arrow1 = slide.shapes.add_shape(
    MSO_SHAPE.DOWN_ARROW,
    Inches(6.4), Inches(2.85), Inches(0.5), Inches(0.35)
)
arrow1.fill.solid()
arrow1.fill.fore_color.rgb = COLOR_MUTED
arrow1.line.fill.background()

# Layer 2
layer2 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(3.25), Inches(12.333), Inches(0.9)
)
layer2.fill.solid()
layer2.fill.fore_color.rgb = COLOR_SECONDARY
layer2.line.fill.background()
tf = layer2.text_frame
tf.text = "2. STREAM PROCESSING — Apache Kafka → Apache Spark"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

# Arrow
arrow2 = slide.shapes.add_shape(
    MSO_SHAPE.DOWN_ARROW,
    Inches(6.4), Inches(4.2), Inches(0.5), Inches(0.35)
)
arrow2.fill.solid()
arrow2.fill.fore_color.rgb = COLOR_MUTED
arrow2.line.fill.background()

# Layer 3
layer3 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(4.6), Inches(12.333), Inches(0.9)
)
layer3.fill.solid()
layer3.fill.fore_color.rgb = COLOR_SUCCESS
layer3.line.fill.background()
tf = layer3.text_frame
tf.text = "3. DATA STORAGE — PostgreSQL (3 tabel)"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

# Arrow
arrow3 = slide.shapes.add_shape(
    MSO_SHAPE.DOWN_ARROW,
    Inches(6.4), Inches(5.55), Inches(0.5), Inches(0.35)
)
arrow3.fill.solid()
arrow3.fill.fore_color.rgb = COLOR_MUTED
arrow3.line.fill.background()

# Layer 4 & 5 side by side
layer4 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(5.95), Inches(6.0), Inches(0.9)
)
layer4.fill.solid()
layer4.fill.fore_color.rgb = COLOR_WARNING
layer4.line.fill.background()
tf = layer4.text_frame
tf.text = "4. ANALYTICS — MA, Trend"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

layer5 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(6.85), Inches(5.95), Inches(6.0), Inches(0.9)
)
layer5.fill.solid()
layer5.fill.fore_color.rgb = COLOR_PURPLE
layer5.line.fill.background()
tf = layer5.text_frame
tf.text = "5. VISUALIZATION — Streamlit"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(13)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

add_footer(slide, 3)


# ============================================================
# SLIDE 4: LAYER 1 — DATA SOURCE
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "📡 Layer 1: Data Source (API)", "yfinance — Yahoo Finance")
add_section_header(slide, "Sumber Data", COLOR_PRIMARY)

bullets = [
    "• Library: yfinance (Yahoo Finance API)",
    "• Tipe: REST API (gratis, tanpa API key)",
    "• Frekuensi: Setiap 10 detik per saham",
    "• Format: JSON (OHLCV + timestamp)",
]
add_bullet_text(slide, bullets, top=2.6, font_size=14)

# Tabel fields
data = [
    ["Field", "Deskripsi", "Contoh"],
    ["symbol", "Kode saham", "STO.AX"],
    ["name", "Nama perusahaan", "Santos Ltd"],
    ["price", "Harga terakhir", "8.73"],
    ["open/high/low", "OHLC", "8.70 / 8.78 / 8.68"],
    ["volume", "Volume transaksi", "5,274,177"],
]
add_table(slide, data, top=4.5, col_widths=[2.5, 4.5, 5.333])
add_footer(slide, 4)


# ============================================================
# SLIDE 5: LAYER 2 — STREAM PROCESSING
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "⚡ Layer 2: Stream Processing", "Kafka + Spark Streaming")

# Kafka box
kafka_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(2.0), Inches(6.0), Inches(2.5)
)
kafka_box.fill.solid()
kafka_box.fill.fore_color.rgb = COLOR_PRIMARY
kafka_box.line.fill.background()
tf = kafka_box.text_frame
tf.text = "Apache Kafka (Ingestion)"
tf.vertical_anchor = MSO_ANCHOR.TOP
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

kafka_items = [
    "• Versi: 3.6.1 (KRaft mode)",
    "• Port: 9093",
    "• Topic: stock-prices-tl",
    "• Producer: kafka-python-ng",
    "• Throughput: ~5 pesan/10s",
]
for i, item in enumerate(kafka_items):
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

# Spark box
spark_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(6.85), Inches(2.0), Inches(6.0), Inches(2.5)
)
spark_box.fill.solid()
spark_box.fill.fore_color.rgb = COLOR_SECONDARY
spark_box.line.fill.background()
tf = spark_box.text_frame
tf.text = "Apache Spark (Processing)"
tf.vertical_anchor = MSO_ANCHOR.TOP
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

spark_items = [
    "• Versi: 3.5.0 (local mode)",
    "• Trigger: ~2 detik",
    "• Read → Parse → Clean",
    "• Transform → Window (1 menit)",
    "• Write: PostgreSQL (JDBC)",
]
for i, item in enumerate(spark_items):
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

# Flow diagram
flow_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(4.8), Inches(12.333), Inches(2.0)
)
flow_box.fill.solid()
flow_box.fill.fore_color.rgb = COLOR_BG
flow_box.line.color.rgb = COLOR_MUTED
tf = flow_box.text_frame
tf.text = "Fluxu Processing:"
p = tf.paragraphs[0]
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

flow_text = "Kafka → readStream → Parse JSON → Data Cleaning → Transformation → Window Aggregation (1 menit) → Write to PostgreSQL"
p = tf.add_paragraph()
p.text = flow_text
p.font.size = Pt(11)
p.font.color.rgb = COLOR_MUTED
add_footer(slide, 5)


# ============================================================
# SLIDE 6: LAYER 3 — DATA STORAGE
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🗄️ Layer 3: Data Storage", "PostgreSQL 17 — Database: stock_db")

# Tabel 3 tabel
data = [
    ["Tabel", "Isi", "Records"],
    ["stock_prices", "Data mentah per event", "9.000+"],
    ["stock_trends", "Agregasi window 1 menit", "100+"],
    ["stock_analytics", "MA, Volatility, Trend", "5+ (per saham)"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 6.0, 2.833])

# Info tambahan
info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(4.8), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "Fitur Database:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

items = [
    "• Index pada symbol, timestamp untuk query cepat",
    "• BIGSERIAL primary key di setiap tabel",
    "• Timestamp auto-generated (inserted_at)",
    "• Format OHLC lengkap (Open, High, Low, Close)",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(4)
add_footer(slide, 6)


# ============================================================
# SLIDE 7: LAYER 4 — ANALYTICS
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🧠 Layer 4: Big Data Analytics", "Trend Analysis — Moving Average")

# Formula boxes
formula1 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(2.0), Inches(6.0), Inches(1.2)
)
formula1.fill.solid()
formula1.fill.fore_color.rgb = COLOR_PRIMARY
formula1.line.fill.background()
tf = formula1.text_frame
tf.text = "Moving Average"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p = tf.add_paragraph()
p.text = "MA-5 = Rata-rata 5 harga\nMA-20 = Rata-rata 20 harga"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

formula2 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(6.85), Inches(2.0), Inches(6.0), Inches(1.2)
)
formula2.fill.solid()
formula2.fill.fore_color.rgb = COLOR_SUCCESS
formula2.line.fill.background()
tf = formula2.text_frame
tf.text = "Trend Detection"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p = tf.add_paragraph()
p.text = "UP: MA-5 > MA-20 × 1.01\nDOWN: MA-5 < MA-20 × 0.99\nSIDEWAYS: di antaranya"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

# Tabel hasil
data = [
    ["Saham", "MA-5", "MA-20", "Volatility", "Trend"],
    ["STO.AX", "8.60", "8.59", "0.0711", "SIDEWAYS"],
    ["WDS.AX", "32.66", "32.65", "0.2122", "SIDEWAYS"],
    ["FDR.AX", "0.30", "0.30", "0.0015", "DOWN"],
    ["ENI.MI", "23.99", "23.99", "0.0545", "SIDEWAYS"],
    ["ESR.AX", "0.03", "0.03", "0.0005", "SIDEWAYS"],
]
add_table(slide, data, top=3.5, col_widths=[2.0, 2.0, 2.0, 2.5, 2.833])
add_footer(slide, 7)


# ============================================================
# SLIDE 8: LAYER 5 — VISUALIZATION
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "📊 Layer 5: Visualization", "Streamlit Dashboard")

# Komponen
data = [
    ["Komponen", "Fungsi"],
    ["Header & Status", "LIVE indicator, timestamp"],
    ["KPI Cards (4)", "Records, Volume, Windows, Last Data"],
    ["Stock Cards (5)", "Harga terakhir per saham"],
    ["Tab 1: Candlestick", "Pergerakan harga (OHLC)"],
    ["Tab 2: Volume", "Bar + Pie chart"],
    ["Tab 3: Trend", "Agregasi window 1 menit"],
    ["Tab 4: Analytics", "Moving Average (MA-5 vs MA-20)"],
]
add_table(slide, data, top=2.0, col_widths=[4.5, 7.833])

# Info
info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.8), Inches(12.333), Inches(1)
)
tf = info_box.text_frame
tf.text = "Fitur Interaktif: Auto-refresh 10s | Filter saham | Filter waktu | Filter interval"
p = tf.paragraphs[0]
p.font.size = Pt(12)
p.font.color.rgb = COLOR_MUTED
p.alignment = PP_ALIGN.CENTER
add_footer(slide, 8)


# ============================================================
# SLIDE 9: 5 SAHAM
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🇹🇱 5 Saham Terkait Timor-Leste", "Perusahaan dengan operasi di TL")

data = [
    ["#", "Simbol", "Perusahaan", "Bursa", "Sektor"],
    ["1", "STO.AX", "Santos Ltd", "ASX", "Minyak & Gas"],
    ["2", "WDS.AX", "Woodside Energy", "ASX", "Minyak & Gas"],
    ["3", "FDR.AX", "Finder Energy", "ASX", "Minyak & Gas"],
    ["4", "ENI.MI", "Eni S.p.A.", "Borsa Italiana", "Energi Terintegrasi"],
    ["5", "ESR.AX", "Estrella Resources", "ASX", "Mineral & Mining"],
]
add_table(slide, data, top=2.0, col_widths=[0.5, 1.8, 3.5, 3.0, 3.533])

# Info
info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "Mengapa 5 Saham Ini?"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

items = [
    "• Memiliki operasi aktif di Timor-Leste",
    "• Beberapa bermitra dengan TIMOR GAP (perusahaan negara TL)",
    "• Relevan dengan Dana Perminyakan Timor-Leste",
    "• Mencakup seluruh siklus (eksplorasi → produksi)",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(4)
add_footer(slide, 9)


# ============================================================
# SLIDE 10: SANTOS
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🔵 Santos Ltd (STO.AX)", "Operator Bayu-Undan")

data = [
    ["Aspek", "Detail"],
    ["Nama Lengkap", "Santos Limited"],
    ["Didirikan", "1954"],
    ["Kantor Pusat", "Adelaide, Australia"],
    ["Industri", "Minyak, Gas & Batubara"],
    ["Karyawan", "~2.959"],
    ["Revenue 2025", "~$7,9 miliar AUD"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

# Hubungan TL
info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.2), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Hubungan dengan Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Operator Bayu-Undan (ladang gas utama TL)",
    "• 36,5% saham di Bayu-Undan",
    "• Kontribusi ~$25 miliar AS untuk TL (20 tahun)",
    "• Unit bisnis: Northern Australia & Timor-Leste",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 10)


# ============================================================
# SLIDE 11: WOODSIDE
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🟢 Woodside Energy (WDS.AX)", "Operator Greater Sunrise")

data = [
    ["Aspek", "Detail"],
    ["Nama Lengkap", "Woodside Energy Group Ltd"],
    ["Kantor Pusat", "Perth, Australia"],
    ["Industri", "Minyak & Gas"],
    ["Posisi", "Operator Greater Sunrise"],
    ["Saham", "33,44%"],
    ["Mitra", "TIMOR GAP (56,56%), Osaka Gas (10%)"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.2), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Hubungan dengan Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_SUCCESS

items = [
    "• Operator proyek Greater Sunrise",
    "• 33,44% saham, TIMOR GAP sebagai mitra utama",
    "• Kontribusi ~A$5 juta untuk komunitas TL",
    "• Status: Negosiasi PSC sedang berlangsung",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 11)


# ============================================================
# SLIDE 12: FINDER ENERGY
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🟠 Finder Energy (FDR.AX)", "Operator Proyek KTJ")

data = [
    ["Aspek", "Detail"],
    ["Nama Lengkap", "Finder Energy Holdings Limited"],
    ["Kantor Pusat", "Australia"],
    ["Industri", "Eksplorasi & Pengembangan Minyak & Gas"],
    ["Market Cap", "~A$202,3 juta"],
    ["Posisi", "Operator PSC 19-11"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Hubungan dengan Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WARNING

items = [
    "• Operator PSC 19-11 (proyek KTJ: Kuda Tasi & Jahal)",
    "• 2P Reserves: 22,2 juta barel minyak",
    "• Development Plan disetujui ANP Timor-Leste",
    "• Target First Oil: 2027-2028",
    "• Proyek minyak lepas pantai pertama di kedaulatan TL",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 12)


# ============================================================
# SLIDE 13: ENI
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🟣 Eni S.p.A. (ENI.MI)", "Operator PSC TL-SO-22-23")

data = [
    ["Aspek", "Detail"],
    ["Nama Lengkap", "Eni S.p.A."],
    ["Kantor Pusat", "Milan, Italia"],
    ["Industri", "Energi Terintegrasi"],
    ["Kehadiran di TL", "Sejak 2006"],
    ["Karyawan di TL", ">100 orang"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Hubungan dengan Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PURPLE

items = [
    "• Operator PSC TL-SO-22-23 (Blok P) sejak 2023",
    "• Mitra: TIMOR GAP (12,5% hak partisipasi)",
    "• Aktivitas: Survei seismik 3D ~1.500 km² (Q1 2026)",
    "• Kepemilikan historis: Bayu-Undan, Kitan Oil (40%)",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 13)


# ============================================================
# SLIDE 14: ESTRELLA
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🩷 Estrella Resources (ESR.AX)", "Eksplorasi Mangan di TL")

data = [
    ["Aspek", "Detail"],
    ["Nama Lengkap", "Estrella Resources Limited"],
    ["Didirikan", "2011"],
    ["Kantor Pusat", "Perth, Australia"],
    ["Industri", "Mineral & Mining"],
    ["Posisi", "Eksplorasi di TL"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Hubungan dengan Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PINK

items = [
    "• Eksplorasi mangan (manganese) & batu gamping",
    "• 100% interest di proyek Timor-Leste",
    "• Kemitraan: Murak Rai Timor E.P. (perusahaan tambang nasional)",
    "• Status: Tahap eksplorasi (belum produksi)",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 14)


# ============================================================
# SLIDE 15: RINGKASAN
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🇹🇱 Ringkasan: Hubungan dengan Timor-Leste", "Semua 5 saham terkait")

data = [
    ["Saham", "Jenis Hubungan", "Tahap", "Mitra TL"],
    ["STO.AX", "Operator Bayu-Undan", "Produksi berakhir", "TIMOR GAP"],
    ["WDS.AX", "Operator Greater Sunrise", "Negosiasi PSC", "TIMOR GAP (56,56%)"],
    ["FDR.AX", "Operator KTJ (PSC 19-11)", "FID pending", "TIMOR GAP, ANP"],
    ["ENI.MI", "Operator PSC TL-SO-22-23", "Eksplorasi aktif", "TIMOR GAP (12,5%)"],
    ["ESR.AX", "Eksplorasi mangan", "Eksplorasi", "Murak Rai Timor E.P."],
]
add_table(slide, data, top=2.0, col_widths=[1.8, 4.0, 3.0, 3.533])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "💡 Insight Utama:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Semua 5 saham memiliki keterkaitan langsung dengan Timor-Leste",
    "• ENI.MI dan FDR.AX paling aktif (kemitraan dengan TIMOR GAP)",
    "• Mencakup seluruh siklus: eksplorasi, pengembangan, produksi, negosiasi",
    "• Relevan dengan Dana Perminyakan Timor-Leste",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 15)


# ============================================================
# SLIDE 16: KESIMPULAN
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🎯 Kesimpulan", "Pencapaian & Demo Live")

# Two columns
left_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(2.0), Inches(6.0), Inches(4.5)
)
left_box.fill.solid()
left_box.fill.fore_color.rgb = COLOR_BG
left_box.line.color.rgb = COLOR_PRIMARY
tf = left_box.text_frame
tf.text = "✅ Yang Telah Dicapai"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Pipeline end-to-end (API → Dashboard)",
    "• 5 saham terkait Timor-Leste",
    "• 9.000+ records diproses",
    "• Latensi ~3 detik",
    "• Zero error",
    "• Dashboard interaktif dengan 4 chart type",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(4)

right_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(6.85), Inches(2.0), Inches(6.0), Inches(4.5)
)
right_box.fill.solid()
right_box.fill.fore_color.rgb = COLOR_BG
right_box.line.color.rgb = COLOR_SUCCESS
tf = right_box.text_frame
tf.text = "🔧 Teknologi"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_SUCCESS

tech_items = [
    "• Data Source: yfinance API",
    "• Ingestion: Apache Kafka 3.6.1",
    "• Processing: Apache Spark 3.5.0",
    "• Storage: PostgreSQL 17",
    "• Analytics: pandas, numpy",
    "• Visualization: Streamlit + Plotly",
]
for item in tech_items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(4)

# Demo info
demo_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(6.6), Inches(12.333), Inches(0.5)
)
tf = demo_box.text_frame
tf.text = "🎬 Demo Live: http://localhost:8501"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.alignment = PP_ALIGN.CENTER
add_footer(slide, 16)


# ============================================================
# SIMPAN PRESENTASI
# ============================================================
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "Capstone_Presentation.pptx")

prs.save(output_path)

print("=" * 70)
print("✅ PRESENTASI BERHASIL DIBUAT!")
print("=" * 70)
print(f"📁 Lokasi: {output_path}")
print(f"📊 Total slide: {len(prs.slides)}")
print("=" * 70)
print("\nBuka file dengan Microsoft PowerPoint untuk edit.")
print("=" * 70)