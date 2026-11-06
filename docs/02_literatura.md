\# KAPÍTULU 2 — LITERATURE REVIEW



\## 2.1 Big Data



\*\*Big Data\*\* refere ba konjuntu dadus ne'ebé boot tebes no kompleksu, ne'ebé la bele prosesa uza ferramenta tradisional. Karakteristika Big Data konhesidu hanesan \*\*5V\*\*:



1\. \*\*Volume\*\* — Dadus boot husi terabyte to petabyte

2\. \*\*Velocity\*\* — Dadus prodús ho lalais, presiza prosesamentu real-time

3\. \*\*Variety\*\* — Dadus iha format oioin: structured, semi-structured, unstructured

4\. \*\*Veracity\*\* — Kualidade no konfiabilidade dadus

5\. \*\*Value\*\* — Dadus iha nilai informasaun ne'ebé importante



Iha setór finanseiru, Big Data uza atu analiza movimentu merkadu, detekta fraude, no predisaun trend.



\*\*Implementasaun iha Projetu:\*\*

\- \*\*Volume:\*\* 37.011+ records (stock\_prices)

\- \*\*Velocity:\*\* Streaming real-time setiap 10 detik

\- \*\*Variety:\*\* JSON (Kafka), Structured (PostgreSQL)

\- \*\*Veracity:\*\* Data cleaning (filter null, negatif)

\- \*\*Value:\*\* Insight ba investimentu saham TL



\## 2.2 Data Streaming



\*\*Data Streaming\*\* mak prosesu dadus kontinuamente bainhira dadus prodús. Kontráriu ba batch processing ne'ebé prosesa dadus iha grupu.



\*\*Karakteristika:\*\*

\- \*\*Continuous\*\* — Dadus flui kontinuamente

\- \*\*Real-time / Near-real-time\*\* — Prosesamentu lais

\- \*\*Unbounded\*\* — La iha limit ba dadus

\- \*\*Event-driven\*\* — Reage ba eventu



\*\*Teknologia streaming modernu:\*\* Apache Kafka, Apache Flink, Apache Spark Streaming, Amazon Kinesis.



\*\*Implementasaun iha Projetu:\*\*

\- Pipeline prosesa dadus kontinuamente husi API

\- Laténsia \~2 detik end-to-end

\- Data rate \~13 records/menit



\## 2.3 Apache Kafka



\*\*Apache Kafka\*\* mak plataforma distribuída ba streaming eventu, dezenvolvida husi LinkedIn no doa ba Apache Software Foundation. Kafka uza arquitetura \*\*publish-subscribe\*\* ho komponente:



\- \*\*Producer\*\* — Kirim mensajen ba topic

\- \*\*Topic\*\* — Kanal ba mensajen

\- \*\*Consumer\*\* — Lee mensajen husi topic

\- \*\*Broker\*\* — Server Kafka

\- \*\*Partition\*\* — Divizaun topic ba paralelizmu



Kafka suporta \*\*KRaft mode\*\* (Kafka Raft) — la presiza Apache Zookeeper, simplifika arquitetura no redús laténsia.



\*\*Implementasaun iha Projetu:\*\*

\- \*\*Versi:\*\* Kafka 3.6.1 (KRaft mode)

\- \*\*Port:\*\* 9093 (izolasaun husi projetu tuan)

\- \*\*Topic:\*\* `stock-prices-tl`

\- \*\*Producer:\*\* Python (`kafka-python-ng`)

\- \*\*Throughput:\*\* \~5 mensajen/10 segundu



\## 2.4 Apache Spark



\*\*Apache Spark\*\* mak engine prosesamentu distribuída ne'ebé suporta batch no streaming. Spark Streaming (Structured Streaming) permite prosesamentu dadus real-time ho API DataFrame/Dataset.



\*\*Komponente Spark:\*\*

\- \*\*Spark Core\*\* — Engine básiku

\- \*\*Spark SQL\*\* — Prosesamentu structured data

\- \*\*Spark Streaming\*\* — Prosesamentu streaming

\- \*\*MLlib\*\* — Machine learning

\- \*\*GraphX\*\* — Graph processing



\*\*Structured Streaming\*\* iha projetu ida-ne'e uza:

\- Baca husi Kafka (`readStream`)

\- Parse JSON

\- Data cleaning (filter null, negativu)

\- Window aggregation (1 minutu)

\- Write ba PostgreSQL (`foreachBatch`)



\*\*Implementasaun iha Projetu:\*\*

\- \*\*Versi:\*\* PySpark 3.5.0 (local mode)

\- \*\*Trigger:\*\* \~2 detik per micro-batch

\- \*\*Processing:\*\* Parse JSON → Clean → Transform → Aggregate

\- \*\*Checkpoint:\*\* `raw` (persistent), `agg` (no checkpoint)



\## 2.5 Data Analytics



\*\*Data Analytics\*\* mak prosesu examina dadus atu hetan insight. Tipu analytics:



1\. \*\*Descriptive Analytics\*\* — Saida ne'ebé akontese?

2\. \*\*Diagnostic Analytics\*\* — Tanba sa akontese?

3\. \*\*Predictive Analytics\*\* — Saida ne'ebé sei akontese?

4\. \*\*Prescriptive Analytics\*\* — Saida ne'ebé tenke halo?



\*\*Indikador ne'ebé uza iha projetu:\*\*



\### 2.5.1 Moving Average (MA)

Formula: 
MA_n = (P1 + P2 + ... + Pn) / n

- **MA-5** — Rata-rata 5 prezu ikus (tren jangka badak)
- **MA-20** — Rata-rata 20 prezu ikus (tren jangka naruk)

### 2.5.2 Volatility
Formula: 
Volatility = StdDev(prices)
Uza NumPy `np.std()`.

### 2.5.3 Trend Detection
Logic:
```python
if ma_5 > ma_20 * 1.01:
    trend = "UP"        # Bullish
elif ma_5 < ma_20 * 0.99:
    trend = "DOWN"      # Bearish
else:
    trend = "SIDEWAYS"  # Konsolidasaun

2.5.4 Price Change %
Formula:
Change% = ((MA-5 - MA-20) / MA-20) * 100

2.6 Machine Learning
Machine Learning mak subsétór AI ne'ebé permite sistema aprende husi dadus. Iha kontekstu finanseiru, ML uza ba:

Predisaun harga — Linear Regression, ARIMA, LSTM

Klasifikasaun — UP/DOWN/SIDEWAYS

Clustering — Grup saham similar

Anomaly Detection — Detekta transasaun suspeita

Linear Regression — algoritmu básiku ML:
y = β0 + β1×x1 + β2×x2 + ... + βn×xn

mplementasaun iha Projetu:

Model: Linear Regression (scikit-learn)

Fitur (10): price, volume, ma_5, ma_20, hour, minute, day_of_week, price_lag_1, price_lag_2, volume_lag_1

Target: Harga 1 jam ke depan

Training Data: 25.098 records (5 saham)

Metrics: MAE, RMSE, R², MAPE

Hasil Prediksi:

Saham	Harga Skrg	Prediksi	Perubahan
STO.AX	$8.56	$8.67	+1.33%
WDS.AX	$31.72	$31.74	+0.05%
FDR.AX	$0.285	$0.284	-0.53%
ENI.MI	$24.11	$23.99	-0.50%
ESR.AX	$0.026	$0.030	+13.46%

2.7 Data Visualization
Data Visualization mak reprezentasaun vizuál husi dadus atu fasilita kompreensaun.

Teknologia Visualizasaun:

Streamlit — Framework Python ba dashboard

Plotly — Library chart interaktivu

Matplotlib — Library chart statik

Implementasaun iha Projetu:

Platform: Streamlit 1.31 + Plotly 5.18

5 Tabs:

Tab 1: Candlestick/Area/Line/OHLC
Tab 2: Volume & Distribusi
Tab 3: Agregasaun Window
Tab 4: Analytics (MA)
Tab 5: Prediction (ML)
Auto-refresh: 10 detik

Fitur: Filter saham, waktu, interval

2.8 Related Projects
2.8.1 Real-Time Stock Market Analysis (2023)
Projetu ne'ebé uza Kafka + Spark Streaming atu analiza saham AS. Rezultadu: pipeline efisiente maibé la iha analytics avançadu.

2.8.2 Cryptocurrency Real-Time Analytics (2024)
Sistema monitoriza crypto ho Kafka + Spark + Grafana. Foku iha visualizasaun real-time.

2.8.3 Smart Agriculture Monitoring (2024)
Uza IoT sensor + Kafka + Spark ba monitoriza plantasaun. Kontribuisaun: integrasaun IoT.

2.8.4 Stock Prediction with ML (2025)
Uza LSTM ba predisaun harga saham. Akurasi ~85% tapi presiza data training boot.

2.8.5 Diferença Projetu Ida-ne'e
Foku Timor-Leste: Saham kompañia minarai no gás ne'ebé opera iha TL

Full Stack: API → Kafka → Spark → PostgreSQL → Streamlit

Analytics Integration: MA, volatility, trend + ML prediction

Modern Dashboard: 5 tabs interaktivu ho auto-refresh

Testing Formal: Functional, Performance, Quality, Scalability

2.9 Teknologia Komparativu
2.9.1 Message Broker
Aspektu	Kafka	RabbitMQ	AWS Kinesis
Throughput	Aas tebes	Médiu	Aas
Laténsia	Baixo (ms)	Baixo	Baixo
Persisténsia	Sim (disk)	Opcional	Sim
Scalability	Excelente	Médiu	Excelente
Open Source	✅ Sim	✅ Sim	❌ La
Konkluzaun: Kafka mak eskolla ideal ba projetu ne'ebé presiza throughput aas no open-source.

2.9.2 Stream Processing
Aspektu	Spark Streaming	Flink	Storm
Laténsia	~2 detik	~ms	~ms
Kompleksidade	Médiu	Aas	Médiu
Ekosistema	Boot	Boot	Médiu
ML Integration	MLlib	FlinkML	—
Konkluzaun: Spark Streaming mak eskolla ideal ba projetu ida-ne'e.

2.9.3 Database
Aspektu	PostgreSQL	MySQL	MongoDB
Tipe	Relational	Relational	NoSQL
ACID	✅ Sim	✅ Sim	Parcial
JSON Support	✅ Sim	✅ Sim	✅ Sim
Open Source	✅ Sim	✅ Sim	✅ Sim
Konkluzaun: PostgreSQL mak eskolla ideal ba data structured.

2.10 Referénsia
Apache Kafka Documentation. (2024). https://kafka.apache.org/

Apache Spark Documentation. (2024). https://spark.apache.org/

PostgreSQL Documentation. (2024). https://www.postgresql.org/

Streamlit Documentation. (2024). https://streamlit.io/

scikit-learn Documentation. (2024). https://scikit-learn.org/

Yahoo Finance API. (2024). https://finance.yahoo.com/

Dean, J., & Ghemawat, S. (2008). MapReduce: Simplified Data Processing on Large Clusters. Communications of the ACM.

Zaharia, M., et al. (2016). Apache Spark: A Unified Engine for Big Data Processing. Communications of the ACM.

Kreps, J., et al. (2011). Kafka: a Distributed Messaging System for Log Processing. NetDB.

Timor-Leste Petroleum Fund. (2024). Banco Central de Timor-Leste.

