"""
Generate PowerPoint Presentation (Versaun Tetun)
Projetu Capstone: Real-Time Stock Market Streaming Analytics
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime
import os


# ============================================================
# KONFIGURASAUN KÓR
# ============================================================
COLOR_PRIMARY = RGBColor(0x3b, 0x82, 0xf6)      # Azúl
COLOR_SECONDARY = RGBColor(0x06, 0xb6, 0xd4)    # Teal
COLOR_SUCCESS = RGBColor(0x10, 0xb9, 0x81)      # Verde
COLOR_WARNING = RGBColor(0xf5, 0x9e, 0x0b)      # Oranje
COLOR_DANGER = RGBColor(0xef, 0x44, 0x44)       # Mean
COLOR_PURPLE = RGBColor(0x8b, 0x5c, 0xf6)       # Violeta
COLOR_PINK = RGBColor(0xec, 0x48, 0x99)         # Rosa
COLOR_DARK = RGBColor(0x1e, 0x29, 0x3b)         # Slate nakukun
COLOR_MUTED = RGBColor(0x64, 0x74, 0x8b)        # Slate muted
COLOR_WHITE = RGBColor(0xff, 0xff, 0xff)
COLOR_BG = RGBColor(0xf8, 0xfa, 0xfc)           # Slate naroman


# ============================================================
# FUNSAUN AJUDANTE
# ============================================================
def add_gradient_header(slide, title, subtitle=""):
    """Aumenta header ho gradient azúl-teal."""
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        Inches(13.333), Inches(1.5)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = COLOR_PRIMARY
    header.line.fill.background()
    
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
    """Aumenta section header ho kór."""
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
    """Aumenta bullet list."""
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
    """Aumenta tabela."""
    rows = len(data)
    cols = len(data[0])
    
    table_shape = slide.shapes.add_table(
        rows, cols,
        Inches(left), Inches(top),
        Inches(width), Inches(0.4 * rows)
    )
    table = table_shape.table
    
    if col_widths:
        for i, w in enumerate(col_widths):
            table.columns[i].width = Inches(w)
    
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = table.cell(r, c)
            cell.text = str(val)
            
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
    """Aumenta footer ho numeru slide."""
    footer = slide.shapes.add_textbox(
        Inches(0.5), Inches(7.0),
        Inches(12.333), Inches(0.3)
    )
    tf = footer.text_frame
    tf.text = f"Análize Merkadu Saham Real-Time | Slide {slide_num}/{total}"
    p = tf.paragraphs[0]
    p.font.size = Pt(9)
    p.font.color.rgb = COLOR_MUTED
    p.alignment = PP_ALIGN.RIGHT


# ============================================================
# INISIALIZASAUN APREZENTASAUN
# ============================================================
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]


# ============================================================
# SLIDE 1: TÍTULU
# ============================================================
slide = prs.slides.add_slide(blank_layout)

bg = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE,
    Inches(0), Inches(0),
    Inches(13.333), Inches(7.5)
)
bg.fill.solid()
bg.fill.fore_color.rgb = COLOR_PRIMARY
bg.line.fill.background()

title_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(2.0),
    Inches(12.333), Inches(1.5)
)
tf = title_box.text_frame
tf.text = "Análize Streaming Merkadu Saham Real-Time"
p = tf.paragraphs[0]
p.font.size = Pt(38)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

sub_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(3.5),
    Inches(12.333), Inches(0.6)
)
tf = sub_box.text_frame
tf.text = "Uza Apache Kafka no Apache Spark"
p = tf.paragraphs[0]
p.font.size = Pt(24)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(4.8),
    Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "Análize Real-Time Saham ne'ebé iha Ligasaun ho Timor-Leste"
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
p.text = f"Naran: [Naran Ita] | NIM: [NIM] | {datetime.now().year}"
p.font.size = Pt(12)
p.font.color.rgb = COLOR_WHITE
p.alignment = PP_ALIGN.CENTER
p.space_before = Pt(20)


# ============================================================
# SLIDE 2: AJENDA
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "📋 Ajenda Aprezentasaun", "Parte 8 Prinsipál")

ajenda = [
    "1. Overview Pipeline — Arkitetura Big Data end-to-end",
    "2. Data Source (API) — Fonte dadus & métodu koleksaun",
    "3. Stream Processing — Kafka & Spark Streaming",
    "4. Data Storage — PostgreSQL & eskema database",
    "5. Big Data Analytics — Análize Trend & Moving Average",
    "6. Visualization — Dashboard Streamlit",
    "7. Saham 5 ne'ebé iha Ligasaun ho Timor-Leste",
    "8. Demu & Konkluzaun",
]
add_bullet_text(slide, ajenda, top=2.6, font_size=16)
add_footer(slide, 2)


# ============================================================
# SLIDE 3: PIPELINE OVERVIEW
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🏗️ Arkitetura Big Data Pipeline", "Layer 5 Prinsipál")

# Layer 1
layer1 = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(1.9), Inches(12.333), Inches(0.9)
)
layer1.fill.solid()
layer1.fill.fore_color.rgb = COLOR_PRIMARY
layer1.line.fill.background()
tf = layer1.text_frame
tf.text = "1. DATA SOURCE (API) — yfinance → Saham 5 TL"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

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
tf.text = "3. DATA STORAGE — PostgreSQL (tabela 3)"
tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE

arrow3 = slide.shapes.add_shape(
    MSO_SHAPE.DOWN_ARROW,
    Inches(6.4), Inches(5.55), Inches(0.5), Inches(0.35)
)
arrow3.fill.solid()
arrow3.fill.fore_color.rgb = COLOR_MUTED
arrow3.line.fill.background()

# Layer 4 & 5
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
add_section_header(slide, "Fonte Dadus", COLOR_PRIMARY)

bullets = [
    "• Biblioteka: yfinance (Yahoo Finance API)",
    "• Tipu: REST API (gratis, la presiza API key)",
    "• Frekuénsia: Kada 10 segundu per saham",
    "• Format: JSON (OHLCV + timestamp)",
]
add_bullet_text(slide, bullets, top=2.6, font_size=14)

data = [
    ["Kampu", "Deskrisaun", "Ezemplu"],
    ["symbol", "Kódigu saham", "STO.AX"],
    ["name", "Naran kompañia", "Santos Ltd"],
    ["price", "Prezu ikus", "8.73"],
    ["open/high/low", "OHLC", "8.70 / 8.78 / 8.68"],
    ["volume", "Volume transasaun", "5,274,177"],
]
add_table(slide, data, top=4.5, col_widths=[2.5, 4.5, 5.333])
add_footer(slide, 4)


# ============================================================
# SLIDE 5: LAYER 2 — STREAM PROCESSING
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "⚡ Layer 2: Stream Processing", "Kafka + Spark Streaming")

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
    "• Versaun: 3.6.1 (KRaft mode)",
    "• Portu: 9093",
    "• Topic: stock-prices-tl",
    "• Producer: kafka-python-ng",
    "• Throughput: ~5 mensajen/10s",
]
for item in kafka_items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

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
    "• Versaun: 3.5.0 (local mode)",
    "• Trigger: ~2 segundu",
    "• Read → Parse → Clean",
    "• Transform → Window (1 minutu)",
    "• Write: PostgreSQL (JDBC)",
]
for item in spark_items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_WHITE
    p.space_before = Pt(4)

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

flow_text = "Kafka → readStream → Parse JSON → Data Cleaning → Transformation → Window Aggregation (1 minutu) → Write to PostgreSQL"
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

data = [
    ["Tabela", "Konteúdu", "Rekorde"],
    ["stock_prices", "Dadus mentah per eventu", "9.000+"],
    ["stock_trends", "Agregasaun window 1 minutu", "100+"],
    ["stock_analytics", "MA, Volatility, Trend", "5+ (per saham)"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 6.0, 2.833])

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
    "• Index iha symbol, timestamp ba query lalais",
    "• BIGSERIAL primary key iha kada tabela",
    "• Timestamp auto-generated (inserted_at)",
    "• Format OHLC kompletu (Open, High, Low, Close)",
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
add_gradient_header(slide, "🧠 Layer 4: Big Data Analytics", "Análize Trend — Moving Average")

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
p.text = "MA-5 = Média 5 prezu ikus\nMA-20 = Média 20 prezu ikus"
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
tf.text = "Deteksaun Trend"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p = tf.add_paragraph()
p.text = "UP: MA-5 > MA-20 × 1.01\nDOWN: MA-5 < MA-20 × 0.99\nSIDEWAYS: iha leten"
p.font.size = Pt(11)
p.font.color.rgb = COLOR_WHITE

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
add_gradient_header(slide, "📊 Layer 5: Visualization", "Dashboard Streamlit")

data = [
    ["Komponente", "Funsaun"],
    ["Header & Status", "Indikador LIVE, timestamp"],
    ["KPI Cards (4)", "Records, Volume, Windows, Last Data"],
    ["Stock Cards (5)", "Prezu ikus per saham"],
    ["Tab 1: Candlestick", "Pergerakan prezu (OHLC)"],
    ["Tab 2: Volume", "Bar + Pie chart"],
    ["Tab 3: Trend", "Agregasaun window 1 minutu"],
    ["Tab 4: Analytics", "Moving Average (MA-5 vs MA-20)"],
]
add_table(slide, data, top=2.0, col_widths=[4.5, 7.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.8), Inches(12.333), Inches(1)
)
tf = info_box.text_frame
tf.text = "Fitur Interaktivu: Auto-refresh 10s | Filtru saham | Filtru tempu | Filtru interval"
p = tf.paragraphs[0]
p.font.size = Pt(12)
p.font.color.rgb = COLOR_MUTED
p.alignment = PP_ALIGN.CENTER
add_footer(slide, 8)


# ============================================================
# SLIDE 9: SAHAM 5
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🇹🇱 Saham 5 ne'ebé iha Ligasaun ho TL", "Kompañia ho operasaun iha TL")

data = [
    ["#", "Símbolu", "Kompañia", "Bursa", "Setór"],
    ["1", "STO.AX", "Santos Ltd", "ASX", "Minarai & Gás"],
    ["2", "WDS.AX", "Woodside Energy", "ASX", "Minarai & Gás"],
    ["3", "FDR.AX", "Finder Energy", "ASX", "Minarai & Gás"],
    ["4", "ENI.MI", "Eni S.p.A.", "Borsa Italiana", "Energia Integradu"],
    ["5", "ESR.AX", "Estrella Resources", "ASX", "Mineral & Mining"],
]
add_table(slide, data, top=2.0, col_widths=[0.5, 1.8, 3.5, 3.0, 3.533])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "Tanba Sa Saham 5 ne'e?"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_DARK

items = [
    "• Iha operasaun ativu iha Timor-Leste",
    "• Balun parseiru ho TIMOR GAP (kompañia estadu TL)",
    "• Relevante ho Dana Perminyakan Timor-Leste",
    "• Kobre siklu tomak (esplorasaun → produsaun)",
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
add_gradient_header(slide, "🔵 Santos Ltd (STO.AX)", "Operadór Bayu-Undan")

data = [
    ["Aspektu", "Detallu"],
    ["Naran Kompletu", "Santos Limited"],
    ["Estabelesidu", "1954"],
    ["Kantu Prinsipál", "Adelaide, Australia"],
    ["Indústria", "Minarai, Gás & Katraas"],
    ["Funzionáriu", "~2.959"],
    ["Revenue 2025", "~$7,9 biliaun AUD"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.2), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Ligasaun ho Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Operadór Bayu-Undan (ladain gás prinsipál TL)",
    "• 36,5% saham iha Bayu-Undan",
    "• Kontribuisaun ~$25 biliaun AS ba TL (20 tinan)",
    "• Unidade negósiu: Northern Australia & Timor-Leste",
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
add_gradient_header(slide, "🟢 Woodside Energy (WDS.AX)", "Operadór Greater Sunrise")

data = [
    ["Aspektu", "Detallu"],
    ["Naran Kompletu", "Woodside Energy Group Ltd"],
    ["Kantu Prinsipál", "Perth, Australia"],
    ["Indústria", "Minarai & Gás"],
    ["Pozisaun", "Operadór Greater Sunrise"],
    ["Saham", "33,44%"],
    ["Parseiru", "TIMOR GAP (56,56%), Osaka Gas (10%)"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.2), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Ligasaun ho Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_SUCCESS

items = [
    "• Operadór projetu Greater Sunrise",
    "• 33,44% saham, TIMOR GAP hanesan parseiru prinsipál",
    "• Kontribuisaun ~A$5 juta ba komunidade TL",
    "• Status: Negosiasaun PSC hela",
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
add_gradient_header(slide, "🟠 Finder Energy (FDR.AX)", "Operadór Projetu KTJ")

data = [
    ["Aspektu", "Detallu"],
    ["Naran Kompletu", "Finder Energy Holdings Limited"],
    ["Kantu Prinsipál", "Australia"],
    ["Indústria", "Esplorasaun & Dezenvolvimentu Minarai & Gás"],
    ["Market Cap", "~A$202,3 juta"],
    ["Pozisaun", "Operadór PSC 19-11"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Ligasaun ho Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_WARNING

items = [
    "• Operadór PSC 19-11 (projetu KTJ: Kuda Tasi & Jahal)",
    "• 2P Reserves: 22,2 juta barel minarai",
    "• Development Plan aprova husi ANP Timor-Leste",
    "• Target First Oil: 2027-2028",
    "• Projetu minarai lepas pantai primeiru iha kedaulatan TL",
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
add_gradient_header(slide, "🟣 Eni S.p.A. (ENI.MI)", "Operadór PSC TL-SO-22-23")

data = [
    ["Aspektu", "Detallu"],
    ["Naran Kompletu", "Eni S.p.A."],
    ["Kantu Prinsipál", "Milan, Itália"],
    ["Indústria", "Energia Integradu"],
    ["Prezénsa iha TL", "Husi 2006"],
    ["Funzionáriu iha TL", ">100 ema"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Ligasaun ho Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PURPLE

items = [
    "• Operadór PSC TL-SO-22-23 (Bloku P) husi 2023",
    "• Parseiru: TIMOR GAP (12,5% hak partisipasaun)",
    "• Atividade: Survei seismik 3D ~1.500 km² (Q1 2026)",
    "• Propriedade históriku: Bayu-Undan, Kitan Oil (40%)",
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
add_gradient_header(slide, "🩷 Estrella Resources (ESR.AX)", "Esplorasaun Mangan iha TL")

data = [
    ["Aspektu", "Detallu"],
    ["Naran Kompletu", "Estrella Resources Limited"],
    ["Estabelesidu", "2011"],
    ["Kantu Prinsipál", "Perth, Australia"],
    ["Indústria", "Mineral & Mining"],
    ["Pozisaun", "Esplorasaun iha TL"],
]
add_table(slide, data, top=2.0, col_widths=[3.5, 8.833])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "🔗 Ligasaun ho Timor-Leste:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PINK

items = [
    "• Esplorasaun mangan (manganese) & batu gamping",
    "• 100% interest iha projetu Timor-Leste",
    "• Kemitraan: Murak Rai Timor E.P. (kompañia tambang nasionál)",
    "• Status: Etapa esplorasaun (seidauk produsaun)",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 14)


# ============================================================
# SLIDE 15: REZUMU
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🇹🇱 Rezumu: Ligasaun ho TL", "Saham 5 hotu iha ligasaun")

data = [
    ["Saham", "Tipu Ligasaun", "Etapa", "Parseiru TL"],
    ["STO.AX", "Operadór Bayu-Undan", "Produsaun remata", "TIMOR GAP"],
    ["WDS.AX", "Operadór Greater Sunrise", "Negosiasaun PSC", "TIMOR GAP (56,56%)"],
    ["FDR.AX", "Operadór KTJ (PSC 19-11)", "FID hela", "TIMOR GAP, ANP"],
    ["ENI.MI", "Operadór PSC TL-SO-22-23", "Esplorasaun ativu", "TIMOR GAP (12,5%)"],
    ["ESR.AX", "Esplorasaun mangan", "Esplorasaun", "Murak Rai Timor E.P."],
]
add_table(slide, data, top=2.0, col_widths=[1.8, 4.0, 3.0, 3.533])

info_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(5.0), Inches(12.333), Inches(2)
)
tf = info_box.text_frame
tf.text = "💡 Insight Prinsipál:"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Saham 5 hotu iha ligasaun direita ho Timor-Leste",
    "• ENI.MI no FDR.AX ativu liu (kemitraan ho TIMOR GAP)",
    "• Kobre siklu tomak: esplorasaun, dezenvolvimentu, produsaun",
    "• Relevante ho Dana Perminyakan Timor-Leste",
]
for item in items:
    p = tf.add_paragraph()
    p.text = item
    p.font.size = Pt(11)
    p.font.color.rgb = COLOR_DARK
    p.space_before = Pt(3)
add_footer(slide, 15)


# ============================================================
# SLIDE 16: KONKLUZAUN
# ============================================================
slide = prs.slides.add_slide(blank_layout)
add_gradient_header(slide, "🎯 Konkluzaun", "Alkançamentu & Demu Live")

left_box = slide.shapes.add_shape(
    MSO_SHAPE.ROUNDED_RECTANGLE,
    Inches(0.5), Inches(2.0), Inches(6.0), Inches(4.5)
)
left_box.fill.solid()
left_box.fill.fore_color.rgb = COLOR_BG
left_box.line.color.rgb = COLOR_PRIMARY
tf = left_box.text_frame
tf.text = "✅ Saida ne'ebé Alkançadu"
p = tf.paragraphs[0]
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY

items = [
    "• Pipeline end-to-end (API → Dashboard)",
    "• Saham 5 ne'ebé iha ligasaun ho TL",
    "• 9.000+ rekorde prosesa",
    "• Laténsia ~3 segundu",
    "• Zero error",
    "• Dashboard interaktivu ho tipu chart 4",
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
tf.text = "🔧 Teknolojia"
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

demo_box = slide.shapes.add_textbox(
    Inches(0.5), Inches(6.6), Inches(12.333), Inches(0.5)
)
tf = demo_box.text_frame
tf.text = "🎬 Demu Live: http://localhost:8501"
p = tf.paragraphs[0]
p.font.size = Pt(14)
p.font.bold = True
p.font.color.rgb = COLOR_PRIMARY
p.alignment = PP_ALIGN.CENTER
add_footer(slide, 16)


# ============================================================
# SIMPAN APREZENTASAUN
# ============================================================
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "Capstone_Presentation_Tetun.pptx")

prs.save(output_path)

print("=" * 70)
print("✅ APREZENTASAUN BERHASIL DIBUAT!")
print("=" * 70)
print(f"📁 Lokasaun: {output_path}")
print(f"📊 Total slide: {len(prs.slides)}")
print("=" * 70)
print("\nLoke file ho Microsoft PowerPoint atu edita.")
print("=" * 70)