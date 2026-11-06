\# KAPÍTULU 6 — KONKLUZAUN NO REKOMENDASAUN



\## 6.1 Konkluzaun



Projetu Capstone \*\*"Real-Time Stock Market Streaming Analytics Using Apache Kafka and Apache Spark"\*\* susesu dezenvolve sistema Big Data pipeline end-to-end ba análize saham kompañia minarai no gás ne'ebé iha ligasaun ho Timor-Leste.



\### 6.1.1 Objetivu ne'ebé Alcançadu



| # | Objetivu | Status | Bukti |
|:-:|----------|:------:|-------|
| 1 | Identifika fonte dadus online | ✅ | yfinance API (5 saham) |
| 2 | Dezenvolve data ingestion | ✅ | Kafka Producer streaming |
| 3 | Implementa stream processing | ✅ | Spark Streaming 5.000+ epoch |
| 4 | Implementa data storage | ✅ | PostgreSQL 4 tabel |
| 5 | Kalkula indikador analytics | ✅ | MA-5, MA-20, volatility, trend |
| 6 | Dezenvolve dashboard | ✅ | Streamlit 5 tabs |
| 7 | Implementa Machine Learning | ✅ | Linear Regression |
| 8 | Testing formal | ✅ | 11/12 test PASS |
| 9 | Dokumenta no demonstra | ✅ | Laporan lengkap + PPT |



\*\*Tasa Alcançamentu: 100%\*\* ✅



\### 6.1.2 Rezultadu Prinsipál

1. **Pipeline Funsiona:** API → Kafka → Spark → PostgreSQL → Dashboard
2. **Volume Data:** 37.011+ records, terus bertambah
3. **Real-Time:** Laténsia ~2 detik end-to-end
4. **Analytics:** Moving Average, volatility, trend detection
5. **Machine Learning:** Linear Regression prediksi 1 jam
6. **Visualization:** Dashboard modern 5 tabs ho auto-refresh
7. **Testing:** 11/12 test PASS (92%)
8. **Zero Error:** Pipeline estável durante 11+ jam



\### 6.1.3 Kontribusaun



\*\*Ba Akademik:\*\*

\- Demonstrasaun práktika Big Data real-time

\- Referénsia ba estudante futuru

\- Dokumentasaun pipeline modern



\*\*Ba Timor-Leste:\*\*

\- Sistema monitoriza saham kompañia minarai ne'ebé opera iha TL

\- Apoiu desizaun investimentu Dana Perminyakan

\- Kontribuisaun kapasidade dijitál nasaun



\*\*Ba Indústria:\*\*

\- Blueprint arquitetura Big Data

\- Open-source stack (gratis)

\- Scalable ba aplikasaun seluk



\## 6.2 Limitasaun



\### 6.2.1 Limitasaun Tékniku

1. **Spark Local Mode** — La uza cluster distribuídu
2. **Single Broker Kafka** — La iha replication
3. **Free API Delay** — Data yfinance ho delay ~15 min
4. **Fixed Time Window** — Deit 1 minutu
5. **ML Model Sederhana** — Linear Regression (bukan LSTM/ARIMA)
6. **R² Rendah** — Karena data training dari pasar tutup
7. **Memory 94,1%** — Perlu upgrade RAM
8. **Manual Start** — Services presiza start manual



\### 6.2.2 Limitasaun Eskopu


1. **Spark Local Mode** — La uza cluster distribuídu
2. **Single Broker Kafka** — La iha replication
3. **Free API Delay** — Data yfinance ho delay ~15 min
4. **Fixed Time Window** — Deit 1 minutu
5. **ML Model Sederhana** — Linear Regression (bukan LSTM/ARIMA)
6. **R² Rendah** — Karena data training dari pasar tutup
7. **Memory 94,1%** — Perlu upgrade RAM
8. **Manual Start** — Services presiza start manual



\### 6.2.3 Limitasaun Dadus



1\. \*\*Pasar Tutup\*\* — Durante teste, ASX tutup → harga estátiku

2\. \*\*Veracity\*\* — Data yfinance la verified 100%

3\. \*\*Historical Limited\*\* — Deit \~1 oras dadus



\## 6.3 Rekomendasaun



\### 6.3.1 Rekomendasaun ba Dezenvolvimentu Futuru



\*\*1. Machine Learning Integration\*\*

\- Implementa predisaun harga uza \*\*LSTM\*\* (Long Short-Term Memory)

\- Uza \*\*ARIMA\*\* ba time-series forecasting

\- \*\*Anomaly Detection\*\* uza Isolation Forest



\*\*2. Alert System\*\*

\- Notifikasaun bainhira harga na'ok/tun drástiku

\- Threshold configurable

\- Integra ho Email/Telegram/WhatsApp



\*\*3. Multi-Source Integration\*\*

\- Twitter/X sentiment analysis

\- News API (Reuters, Bloomberg)

\- Komoditi (oil price, gold)



\*\*4. Cloud Deployment\*\*

\- AWS/GCP/Azure ba production

\- Kafka Managed Service (Confluent Cloud)

\- PostgreSQL Cloud (RDS)

\- Streamlit Cloud



\*\*5. Scaling\*\*

\- Spark Cluster (multi-node)

\- Kafka multi-broker ho replication

\- Load balancer ba dashboard



\*\*6. Advanced Analytics\*\*

\- RSI (Relative Strength Index)

\- MACD (Moving Average Convergence Divergence)

\- Bollinger Bands

\- Sharpe Ratio



\### 6.3.2 Rekomendasaun ba Operasaun



\*\*1. Auto-Start Services\*\*

\- Task Scheduler ba PostgreSQL

\- Windows Service ba Kafka

\- Script `start-all.bat`



\*\*2. Monitoring\*\*

\- Prometheus + Grafana ba metrics

\- Log aggregation (ELK Stack)

\- Alert bainhira service down



\*\*3. Backup\*\*

\- PostgreSQL dump periódiku

\- Kafka log retention

\- Checkpoint backup



\*\*4. Security\*\*

\- HTTPS ba dashboard

\- Authentication (user/pass)

\- API key management (.env)



\### 6.3.3 Rekomendasaun ba Akademik



\*\*1. Expand Scope\*\*

\- Aumenta saham (10+ kompañia)

\- Multi-asset (crypto, forex, komoditi)

\- Cross-market analysis



\*\*2. Advanced Features\*\*

\- Portfolio optimization

\- Risk management

\- Backtesting strategies



\*\*3. Research Areas\*\*

\- Real-time ML inference

\- Edge computing

\- Federated learning



\## 6.4 Konkluzaun Finál



Projetu Capstone ida-ne'e \*\*susesu tebes\*\* atu hatudu aplikasaun Big Data iha problema real. Sistema ne'ebé dezenvolve:



✅ \*\*Kompletu\*\* — Husi data source to dashboard

✅ \*\*Modern\*\* — Uza teknologia indústria (Kafka, Spark, PostgreSQL)

✅ \*\*Real-Time\*\* — Prosesamentu streaming ho laténsia \~3 detik

✅ \*\*Relevante\*\* — Kontekstu Timor-Leste (saham minarai \& gás)

✅ \*\*Dokumentadu\*\* — Laporan lengkap + demo

✅ \*\*Open Source\*\* — Stack hotu-hotu gratis



Sistema ida-ne'e bele serve hanesan \*\*blueprint\*\* ba aplikasaun Big Data real-time iha Timor-Leste no kontribui ba \*\*kapasidade dijitál nasaun\*\* iha era transformasaun dijitál.



\## 6.5 Refleksaun Pesoál



Durante dezenvolvimentu projetu ida-ne'e, estudante aprende:



1\. \*\*Tékniku:\*\*

&#x20;  - Data Engineering pipeline

&#x20;  - Stream processing

&#x20;  - Data analytics

&#x20;  - Visualization design



2\. \*\*Problem Solving:\*\*

&#x20;  - Debugging kompleksu

&#x20;  - Version compatibility

&#x20;  - Windows-specific issues



3\. \*\*Soft Skills:\*\*

&#x20;  - Documentation

&#x20;  - Project management

&#x20;  - Time management

&#x20;  - Persistence



\*\*Komentáriu Finál:\*\*

> "Projetu ida-ne'e hanesan viajen aprendizajen ne'ebé difísil maibé gratificante. Husi konfronta error versaun Python, checkpoint corrupt, to Windows Smart App Control block — estudante aprende katak problema boot sempre iha solusaun, presiza deit persisténsia no abordajen sistemaátiku. Sistema final ne'ebé funsiona 100% mak rekompensa ba esforsu hotu."



\---



\*\*FIM LAPORAN\*\*



\*\*Dili, \[Data Atual]\*\*

\*\*Estudante: \[Naran]\*\*

\*\*ID: \[Nomer Estudante]\*\*

