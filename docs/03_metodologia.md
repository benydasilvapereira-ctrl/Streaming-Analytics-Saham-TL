# KAPÍTULU 3 — METODOLOGIA

## 3.1 Metodologia Jeral

Projetu ida-ne'e uza **Project-Based Learning** ho abordajen **agile** — dezenvolvimentu inkremental iha fase sira:

1. **Fase 1:** Setup Environment (Python, Kafka, PostgreSQL)
2. **Fase 2:** Data Sources (yfinance API)
3. **Fase 3:** Data Ingestion (Kafka Producer)
4. **Fase 4:** Stream Processing (Spark Streaming)
5. **Fase 5:** Data Storage (PostgreSQL)
6. **Fase 6:** Data Analytics (MA, Volatility, Trend)
7. **Fase 7:** Machine Learning (Linear Regression)
8. **Fase 8:** Visualization (Streamlit Dashboard)
9. **Fase 9:** Testing (Functional, Performance, Quality, Scalability)

## 3.2 Data Source

### 3.2.1 Fonte Dadus
- **Platform:** Yahoo Finance (via `yfinance` Python library)
- **API:** REST API (gratis, la presiza API key)
- **Update Frequency:** Real-time (delay ~15 min ba free tier)

### 3.2.2 Saham ne'ebé Analiza (5 Saham)

| Simbol | Kompañia | Setór | Ligasaun ho TL |
|--------|----------|-------|----------------|
| STO.AX | Santos Ltd | Minarai & Gás | Operator Bayu-Undan, 36,5% saham |
| WDS.AX | Woodside Energy | Minarai & Gás | Operator Greater Sunrise, 33,44% saham |
| FDR.AX | Finder Energy | Minarai & Gás | Operator projeitu KTJ |
| ENI.MI | Eni S.p.A. | Energia Integradu | PSC TL-SO-22-23, partner TIMOR GAP |
| ESR.AX | Estrella Resources | Mineral & Mining | Mangan & batu gamping di TL |

### 3.2.3 Data Fields

- `symbol` — Kódigu saham (STO.AX)
- `name` — Naran kompañia
- `exchange` — Bursa (ASX)
- `price` — Prezu atual
- `open`, `high`, `low` — Prezu OHLC
- `volume` — Volume transasaun
- `timestamp` — Tempu eventu
- `source` — Fonte dadus (yfinance)
- `fetched_at` — Waktu fetch husi API

## 3.3 Data Collection

### 3.3.1 Metodu
Uza `yfinance` library ba fetch dadus husi Yahoo Finance API:

```python
import yfinance as yf
ticker = yf.Ticker("STO.AX")
data = ticker.history(period="1d", interval="1m")
3.3.2 Frekuénsia
Interval: 10 segundu

Saham per cycle: 5 (STO.AX, WDS.AX, FDR.AX, ENI.MI, ESR.AX)

Total events: ~13 events/minutu

3.3.3 Rate Limiting
Jeda 2 segundu entre request ba kada saham atu evita rate limit Yahoo Finance.

3.3.4 Statístika Koleksaun (Hasil Finál)
Metrik	Nilai
Total records	37.011
Records per saham	~7.400
Data rate	~13 records/menit
Data type	≥ 2 (OHLCV + timestamp)
3.4 Data Ingestion (Apache Kafka)
3.4.1 Arsitektura
Broker: Kafka 3.6.1 (KRaft mode)

Port: 9093 (izolasaun husi projeitu tuan)

Topic: stock-prices-tl

3.4.2 Producer Flow
yfinance API → fetch_stock_price() → JSON encode → Kafka Topic

3.4.3 Message Format
json
{
  "symbol": "STO.AX",
  "name": "Santos Ltd",
  "exchange": "ASX",
  "price": 8.73,
  "open": 8.70,
  "high": 8.78,
  "low": 8.68,
  "volume": 5274177,
  "timestamp": 1789396531116,
  "source": "yfinance",
  "fetched_at": "2026-09-16T14:15:31"
}

3.4.4 Kafka Configuration
bootstrap_servers: localhost:9093

acks: all (tunggu konfirmasaun)

retries: 3

api_version: (3, 6, 1)

key_serializer: symbol

value_serializer: JSON

3.4.5 Statístika Kafka (Hasil Finál)
Metrik	Nilai
Topic	stock-prices-tl
Offset terakhir	~11.000+
Throughput	~5 mensajen/10s
3.5 Data Storage (PostgreSQL)
3.5.1 Database Schema
Tabel 1: stock_prices (Raw Data)

Kolom	Tipe	Deskrisaun
id	BIGSERIAL PK	Auto-increment ID
symbol	VARCHAR(20)	Kódigu saham
name	VARCHAR(100)	Naran kompañia
exchange	VARCHAR(50)	Bursa (ASX / Borsa Italiana)
price	NUMERIC(12,4)	Prezu atual
open	NUMERIC(12,4)	Prezu open
high	NUMERIC(12,4)	Prezu high
low	NUMERIC(12,4)	Prezu low
volume	BIGINT	Volume
event_timestamp	BIGINT	Epoch ms
source	VARCHAR(20)	'yfinance'
fetched_at	TIMESTAMP	Waktu fetch
inserted_at	TIMESTAMP	Waktu insert
Tabel 2: stock_trends (Aggregation)

Kolom	Tipe	Deskrisaun
id	BIGSERIAL PK	Auto-increment ID
symbol	VARCHAR(20)	Kódigu saham
window_start	TIMESTAMP	Inísiu window
window_end	TIMESTAMP	Remata window
avg_price	NUMERIC(12,4)	Média prezu
max_price	NUMERIC(12,4)	Prezu max
min_price	NUMERIC(12,4)	Prezu min
total_volume	BIGINT	Total volume
data_points	INTEGER	Jumlah event
created_at	TIMESTAMP	Waktu insert
Tabel 3: stock_analytics (Analytics)

Kolom	Tipe	Deskrisaun
id	BIGSERIAL PK	Auto-increment ID
symbol	VARCHAR(20)	Kódigu saham
computed_at	TIMESTAMP	Waktu komputasaun
ma_5	NUMERIC(12,4)	Moving Average 5
ma_20	NUMERIC(12,4)	Moving Average 20
volatility	NUMERIC(12,4)	Standar deviasaun
trend	VARCHAR(20)	UP/DOWN/SIDEWAYS
latest_price	NUMERIC(12,4)	Prezu ikus
price_change_pct	NUMERIC(8,4)	Mudansa %
data_points	INTEGER	Jumlah data
Tabel 4: stock_predictions (Machine Learning)

Kolom	Tipe	Deskrisaun
id	BIGSERIAL PK	Auto-increment ID
symbol	VARCHAR(20)	Kódigu saham
prediction_time	TIMESTAMP	Waktu prediksi
target_time	TIMESTAMP	Target waktu (1 jam)
predicted_price	NUMERIC(12,4)	Prezu prediksi
actual_price	NUMERIC(12,4)	Prezu aktual
model_name	VARCHAR(50)	'LinearRegression'
accuracy	NUMERIC(8,4)	Akurasi
created_at	TIMESTAMP	Waktu insert

3.5.2 Index Strategy
Index pada symbol ba query lalais

Index pada event_timestamp ba time-series query

Index pada window_start ba agregasaun

Index pada target_time ba prediksi

3.5.3 Connection
Host: localhost
Port: 5432
User: postgres
Password: [configured di .env]
Database: stock_db

3.5.4 Statístika Database (Hasil Finál)
Tabel	Records
stock_prices	37.011
stock_trends	28.188
stock_analytics	273
stock_predictions	20
3.6 Data Processing (Apache Spark)
3.6.1 Arsitektura
Engine: PySpark 3.5.0

Mode: Local Mode (local[*] — uza hotu CPU core)

Trigger: Default (~2 segundu)
3.6.2 Processing Steps
Step 1: Read Stream from Kafka

python
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9093") \
    .option("subscribe", "stock-prices-tl") \
    .load()
Step 2: Parse JSON

python
parsed = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), STOCK_SCHEMA).alias("data")) \
    .select("data.*")
Step 3: Data Cleaning

python
cleaned = parsed \
    .filter(col("price").isNotNull() & (col("price") > 0)) \
    .filter(col("symbol").isNotNull())
Step 4: Transformation

python
transformed = cleaned \
    .withColumn("event_time", to_timestamp(from_unixtime(col("timestamp") / 1000)))
Step 5: Window Aggregation (1 minutu)

python
aggregated = cleaned \
    .withWatermark("event_time", "30 seconds") \
    .groupBy(window(col("event_time"), "1 minute"), col("symbol")) \
    .agg(avg("price").alias("avg_price"), ...)
Step 6: Write to PostgreSQL

python
query = cleaned.writeStream \
    .foreachBatch(write_to_postgres("stock_prices")) \
    .outputMode("append") \
    .option("checkpointLocation", ".../checkpoint/raw") \
    .start()
3.6.3 Checkpoint Strategy
checkpoint/raw — Ba stock_prices (persistent, dengan checkpoint)

checkpoint/agg — Ba stock_trends (tanpa checkpoint, outputMode="update")
3.6.4 Statístika Spark (Hasil Finál)
Metrik	Nilai
Epoch stock_prices	5.000+
Epoch stock_trends	2.300+
Processing time per batch	~2 detik
Total records processed	37.011+
3.7 Data Analytics
3.7.1 Moving Average (MA)
Formula:

text
MA_n = (P1 + P2 + ... + Pn) / n
MA-5 — Rata-rata 5 prezu ikus

MA-20 — Rata-rata 20 prezu ikus

3.7.2 Volatility
Formula:

text
Volatility = StdDev(prices)
Uza NumPy np.std().

3.7.3 Trend Detection
Logic:

python
if ma_5 > ma_20 * 1.01:
    trend = "UP"
elif ma_5 < ma_20 * 0.99:
    trend = "DOWN"
else:
    trend = "SIDEWAYS"
3.7.4 Price Change %
Formula:

text
Change% = ((MA-5 - MA-20) / MA-20) * 100
3.7.5 Script Analytics
File: 5_data_analytics/trend_analysis.py

Output: Tabel stock_analytics

Frequensi: Manual / bisa diotomatisasi via Task Scheduler

3.7.6 Hasil Analytics (5 Saham)
Saham	MA-5	MA-20	Trend	Volatility
STO.AX	8.54	8.55	SIDEWAYS	0.0711
WDS.AX	31.50	31.60	SIDEWAYS	0.2122
FDR.AX	0.285	0.290	DOWN	0.0015
ENI.MI	24.41	24.37	SIDEWAYS	0.0545
ESR.AX	0.026	0.027	SIDEWAYS	0.0005

3.8 Machine Learning
3.8.1 Model
Algoritmu: Linear Regression

Library: scikit-learn

Fitur (10): price, volume, ma_5, ma_20, hour, minute, day_of_week, price_lag_1, price_lag_2, volume_lag_1

Target: Harga 1 jam ke depan

3.8.2 Training
Data: 25.098 records (5 saham)

Split: 80% training (19.760), 20% testing (4.943)

Metrics: MAE, RMSE, R², MAPE

File: 7_machine_learning/train_model.py

Output: 5 model .pkl di 7_machine_learning/models/

3.8.3 Prediksi
Input: 100 records terbaru

Output: Prediksi harga 1 jam ke depan

Storage: Tabel stock_predictions

File: 7_machine_learning/predict.py

Frequensi: Setiap 5 menit (via run_prediction_loop.bat)

3.8.4 Hasil Training
Symbol	R²	MAPE	Kualitas
STO.AX	-29.27	0.89%	⭐
WDS.AX	0.5629	0.08%	⭐⭐⭐
FDR.AX	0.6624	0.72%	⭐⭐⭐
ENI.MI	-0.31	0.34%	⭐
ESR.AX	-2.77	6.11%	⭐
3.8.5 Hasil Prediksi
Symbol	Harga Skrg	Prediksi	Perubahan
STO.AX	$8.56	$8.67	+1.33%
WDS.AX	$31.72	$31.74	+0.05%
FDR.AX	$0.285	$0.284	-0.53%
ENI.MI	$24.11	$23.99	-0.50%
ESR.AX	$0.026	$0.030	+13.46%
3.9 Visualization (Streamlit Dashboard)
3.9.1 Platform
Framework: Streamlit 1.31.0

Charts: Plotly 5.18.0

Port: 8501

3.9.2 Dashboard Components (5 Tabs)
Header — Gradient modern

KPI Cards (4) — Records, Volume, Windows, Last Data

Stock Cards (5) — Harga terakhir per saham

Price Change — Perubahan vs 10 menit lalu

Tab 1: Harga Real-Time — Candlestick/Area/Line/OHLC

Tab 2: Volume & Distribusi — Bar + Pie chart

Tab 3: Agregasi Window — Trend line + table

Tab 4: Analytics (MA) — Bar chart MA-5 vs MA-20

Tab 5: Prediction (ML) — Bar chart + table prediksi

Data Table — 30 baris terakhir

3.9.3 Fitur Interaktif
🔄 Auto-refresh (5-60 detik)

🎯 Filter saham (multiselect)

⏱️ Filter waktu (1-12 jam)

📊 Filter interval candle (1-30 menit)

🚦 Market status (OPEN/CLOSED)

3.9.4 Market Hours Feature
File: 6_visualization/market_hours.py

Fungsi: Deteksi status buka/tutup pasar

Pasar: ASX (10:00-16:00 AEST), Borsa Italiana (09:00-17:30 CET)

3.10 Testing Strategy
3.10.1 Functional Testing
Data masuk? (Data Ingestion)

Data diproses? (Stream Processing)

Data disimpan? (Data Storage)

Dashboard funsiona? (Visualization)

Script: docs/test_scripts/01_functional_testing.py

3.10.2 Performance Testing
Latency (end-to-end)

Throughput (records/menit)

CPU/Memory usage

Script: docs/test_scripts/02_performance_testing.py

3.10.3 Data Quality Testing
Missing values

Duplicate records

Invalid records

Outliers (IQR method)

Script: docs/test_scripts/03_data_quality_testing.py

3.10.4 Scalability Testing
Query performance (1K → 37K records)

Aggregation performance

Scaling analysis (linear?)

Script: docs/test_scripts/04_scalability_testing.py

3.10.5 Hasil Testing (Ringkasan)
Testing	PASS	FAIL	Status
Functional	4	0	✅
Performance	2	1	⚠️
Data Quality	4	0	✅
Scalability	1	0	✅
Total	11	1	92%
3.11 Development Tools
Kategoria	Ferramenta
Programming	Python 3.11.8
Editor	VS Code, Notepad
Version Control	Git, GitHub
Terminal	Windows CMD, PowerShell
Container	(La uza — native install)
Data Source	yfinance, Yahoo Finance
Messaging	Apache Kafka 3.6.1
Processing	Apache Spark 3.5.0
Storage	PostgreSQL 17.11
Analytics	pandas, numpy
Machine Learning	scikit-learn, joblib
Visualization	Streamlit, Plotly
Java Runtime	OpenJDK 17.0.20
3.12 Etapa Desenvolvimentu (Sesuai Manual)
Etapa	Atividade	Output	Status
1	Identifikasaun problema	Problem Statement	✅
2	Literature Review	Referénsia	✅
3	Projetu Proposal	Proposal	✅
4	Identifikasaun fonte dadus	Fontes Dadus	✅
5	Data Collection	Raw Data	✅
6	Data Ingestion	Kafka Pipeline	✅
7	Data Storage	Database/Data Lake	✅
8	Data Processing	Spark Pipeline	✅
9	Data Analytics	Analytics Result	✅
10	Machine Learning	ML Model	✅
11	Dashboard	Visualization	✅
12	System Integration	Working System	✅
13	Testing	Test Result	✅
14	Documentation	Final Report	✅