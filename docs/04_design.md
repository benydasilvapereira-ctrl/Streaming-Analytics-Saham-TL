\# KAPÍTULU 4 — SISTEMA DESIGN NO IMPLEMENTATION



\## 4.1 System Architecture



\### 4.1.1 Arquitetura Jeral

┌─────────────────────────────────────────────────────────────┐
│  DATA SOURCES (API)                                          │
│  yfinance → 5 Saham TL (STO.AX, WDS.AX, FDR.AX,             │
│                          ENI.MI, ESR.AX)                    │
└──────────────────────────┬──────────────────────────────────┘
                           │ JSON (10s interval)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA INGESTION (Apache Kafka)                               │
│  Producer → Topic: stock-prices-tl → Broker:9093            │
└──────────────────────────┬──────────────────────────────────┘
                           │ Stream
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  STREAM PROCESSING (Apache Spark Streaming)                  │
│  Parse JSON → Clean → Transform → Window Aggregation        │
└──────────────────────────┬──────────────────────────────────┘
                           │ Batch write
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  DATA STORAGE (PostgreSQL)                                   │
│  stock_prices | stock_trends | stock_analytics |            │
│  stock_predictions                                          │
└──────────────────────────┬──────────────────────────────────┘
                           │ Query
                           ▼
┌─────────────────────────────────────────────────────────────┐
│  VISUALIZATION (Streamlit) + ML                              │
│  5 Tabs: Real-Time, Volume, Trend, Analytics, Prediction    │
└─────────────────────────────────────────────────────────────┘

\### 4.1.2 Karakteristika Big Data (5V)

### 4.1.2 Karakteristika Big Data (5V)
- **Volume:** 37.011+ records, terus bertambah
- **Velocity:** Streaming real-time setiap 10 detik
- **Variety:** JSON, structured, semi-structured
- **Veracity:** Data cleaning (filter null, negatif)
- **Value:** Insight ba investimentu 5 saham TL + ML prediction



\## 4.2 Data Flow Diagram (DFD)



\### 4.2.1 Context Diagram (Level 0)

┌─────────────┐ ┌──────────────────┐

│ Yahoo │ Stock Data (API) │ │

│ Finance │ ────────────────────▶│ Capstone │

│ (yfinance)│ │ System │

└─────────────┘ │ (Big Data │

│ Pipeline) │

┌─────────────┐ Dashboard View │ │

│ User │ ◀────────────────────└──────────────────┘

│ (Investor) │

└─────────────┘





\### 4.2.2 Level 1 DFD

\[Yahoo Finance]

│

│ API Data

▼

┌─────────┐

│ 1.0 │──── Raw JSON ────┐

│ Fetch │ │

│ Data │ ▼

└─────────┘ ┌─────────────┐

│ 2.0 │

│ Kafka │

│ Ingestion │

└──────┬──────┘

│

│ Stream

▼

┌─────────────┐

│ 3.0 │

│ Spark │

│ Processing │

└──────┬──────┘

│

┌───────────────┼───────────────┐

│ │ │

▼ ▼ ▼

┌──────────┐ ┌──────────┐ ┌──────────┐

│4.0 Store │ │5.0 Aggre │ │6.0 Analy │

│Raw Data │ │Windowing │ │MA/Trend │

└──────────┘ └──────────┘ └──────────┘

│ │ │

└───────────────┼───────────────┘

│

▼

┌─────────────┐

│ 7.0 │

│ Dashboard │

│ Streamlit │

└─────────────┘





\## 4.3 Database Design



\### 4.3.1 Entity Relationship Diagram (ERD)

┌─────────────────────────┐

│ stock\_prices │

│─────────────────────────│

│ PK id │

│ symbol │

│ name │

│ exchange │

│ price │

│ open, high, low │

│ volume │

│ event\_timestamp │

│ source │

│ fetched\_at │

│ inserted\_at │

└─────────────────────────┘



┌─────────────────────────┐

│ stock\_trends │

│─────────────────────────│

│ PK id │

│ symbol │

│ window\_start │

│ window\_end │

│ avg\_price │

│ max\_price │

│ min\_price │

│ total\_volume │

│ data\_points │

│ created\_at │

└─────────────────────────┘



┌─────────────────────────┐
│ stock\_analytics        │
│─────────────────────────│
│ PK id                   │
│ symbol                  │
│ computed\_at            │
│ ma\_5                   │
│ ma\_20                  │
│ volatility              │
│ trend                   │
│ latest\_price           │   
│ price\_change\_pct      │
│ data\_points            │
└─────────────────────────┘

┌─────────────────────────┐
│  stock_predictions      │
│─────────────────────────│
│ PK id                   │
│    symbol               │
│    prediction_time      │
│    target_time          │
│    predicted_price      │
│    actual_price         │
│    model_name           │
│    accuracy             │
│    created_at           │
└─────────────────────────┘



\### 4.3.2 Table Specifications



\*\*Tabel `stock\_prices`:\*\*



| Kolom | Tipe | Deskrisaun |

|-------|------|------------|

| id | BIGSERIAL PK | Auto-increment ID |

| symbol | VARCHAR(20) | Kódigu saham |

| name | VARCHAR(100) | Naran kompañia |

| exchange | VARCHAR(10) | Bursa (ASX) |

| price | NUMERIC(12,4) | Prezu atual |

| open | NUMERIC(12,4) | Prezu open |

| high | NUMERIC(12,4) | Prezu high |

| low | NUMERIC(12,4) | Prezu low |

| volume | BIGINT | Volume |

| event\_timestamp | BIGINT | Epoch ms |

| source | VARCHAR(20) | 'yfinance' |

| fetched\_at | TIMESTAMP | Waktu fetch |

| inserted\_at | TIMESTAMP | Waktu insert |



\## 4.4 Processing Pipeline



\### 4.4.1 Flow Detail

Kafka Topic (stock-prices-tl)

│

▼

readStream(format="kafka")

│

▼

Parse JSON (from\_json)

│

▼

Data Cleaning



filter price > 0



filter symbol != null

│

▼

Transformation



convert timestamp



rename columns

│

┌────┴────┐

│ │

▼ ▼

Write to Window Aggregation

stock\_ (1 minute)

prices │

▼

Write to stock\_trends





\### 4.4.2 Window Aggregation

\- \*\*Window Type:\*\* Tumbling (fixed, non-overlapping)

\- \*\*Duration:\*\* 1 minutu

\- \*\*Watermark:\*\* 30 segundu (tolerância late data)

\- \*\*Group By:\*\* window + symbol



\### 4.4.3 Analytics Pipeline

stock\_prices (query 50 latest per symbol)

│

▼

Compute MA-5 (np.mean)

│

▼

Compute MA-20

│

▼

Compute Volatility (np.std)

│

▼

Determine Trend

│

▼

Save to stock\_analytics





\## 4.5 Dashboard Design



\### 4.5.1 Layout Structure

┌────────────────────────────────────────────────┐

│ HEADER (Gradient Blue-Teal) │

│ 📈 Real-Time Stock Market Dashboard │

│ Subtitle + LIVE indicator + Timestamp │

├────────────────────────────────────────────────┤

│ KPI CARDS (4 cards horizontal) │

│ \[Records] \[Volume] \[Windows] \[Last Data] │

├────────────────────────────────────────────────┤

│ STOCK CARDS (3 cards per saham) │

│ \[STO.AX] \[WDS.AX] \[FDR.AX] │

├────────────────────────────────────────────────┤

│ TABS │

│ \[Harga] \[Volume] \[Trend] \[Analytics] │

│ ┌──────────────────────────────────────────┐ │

│ │ Chart Content (Plotly) │ │

│ └──────────────────────────────────────────┘ │

├────────────────────────────────────────────────┤

│ DATA TABLE (30 rows) │

├────────────────────────────────────────────────┤

│ FOOTER (Tech Stack, Pipeline, Context) │

└────────────────────────────────────────────────┘





\### 4.5.2 Sidebar Controls

\- Auto-refresh toggle

\- Refresh interval slider (5-60s)

\- Time range selectbox (50-1000 points)

\- Symbol multiselect

\- Info panel



\### 4.5.3 Chart Specifications



| Tab | Chart Type | Data Source | Fitur |
|-----|-----------|-------------|-------|
| 1 | Candlestick/Area/Line/OHLC | stock_prices | Pergerakan harga (5 saham) |
| 1 | Bar Chart | stock_prices | Volume per candle |
| 2 | Bar Chart | stock_prices | Total volume per saham |
| 2 | Pie Chart | stock_prices | Distribusi data |
| 3 | Line Chart | stock_trends | Avg price per window |
| 4 | Bar Chart | stock_analytics | MA-5 vs MA-20 |
| 5 | Bar Chart | stock_predictions | Prediksi vs Aktual |
| 5 | Table | stock_predictions | Detail prediksi |



### 4.5.4 Color Scheme
- **Primary:** Blue `#3b82f6` (header, section)
- **Secondary:** Teal `#06b6d4` (accent)
- **Success:** Emerald `#10b981` (UP trend)
- **Warning:** Amber `#f59e0b` (SIDEWAYS)
- **Danger:** Red `#ef4444` (DOWN)
- **Purple:** `#8b5cf6` (ML prediction)
- **Pink:** `#ec4899` (Estrella)



\## 4.6 File Structure

Streaming_AnalyticsSahamTL/
├── .env
├── requirements.txt
├── start-all.bat
├── stop-all.bat
├── start-dashboard.bat
├── docs/
│   ├── 00_cover.md
│   ├── 01_introducaun.md
│   ├── 02_literatura.md
│   ├── 03_metodologia.md
│   ├── 04_design.md
│   ├── 05_resultadu.md
│   ├── 05_resultadu_ml.md
│   ├── 06_konkluzaun.md
│   ├── 07_testing.md
│   ├── test_scripts/
│   │   ├── 01_functional_testing.py
│   │   ├── 02_performance_testing.py
│   │   ├── 03_data_quality_testing.py
│   │   └── 04_scalability_testing.py
│   └── screenshots/
├── setup/
├── 1_data_sources/
├── 2_data_ingestion/
├── 3_stream_processing/
├── 4_data_storage/
├── 5_data_analytics/
├── 6_visualization/
├── 7_machine_learning/
│   ├── train_model.py
│   ├── predict.py
│   ├── models/
│   └── run_prediction.bat
├── checkpoint/
└── logs/



\## 4.7 Implementation Notes



\### 4.7.1 Version Compatibility

\- Python 3.11.8 (bukan 3.13 — PySpark 3.5.0 belum support)

\- Java 17 (kompatibel ho Spark 3.5.0)

\- Kafka 3.6.1 + Spark 3.5.0 (sinkron)

\- Hadoop native files (winutils.exe + hadoop.dll)



\### 4.7.2 Isolation Strategy

\- Kafka projeitu foun iha port 9093 (projeitu tuan 9092)

\- Folder data: `data-saham-tl` (separate)

\- venv projeitu ida-ne'e separadu husi Python global



\### 4.7.3 Security

\- Password PostgreSQL iha `.env` (la iha code)

\- `.gitignore` ba file sensitivu

\- Smart App Control Windows whitelist PostgreSQL



