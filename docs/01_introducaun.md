\# KAPÍTULU 1 — INTRODUSAUN



\## 1.1 Background



Iha era dijitál modernu, volume dadus ne'ebé prodús husi sistema informasaun aumenta ho lalais tebes. Fenómenu ida-ne'e konhesidu hanesan \*\*Big Data\*\* — karakterizadu husi Volume, Velocity, Variety, Veracity, no Value (5V). Setór finanseiru, liu-liu merkadu saham, mak ida husi setór ne'ebé prodús dadus barak tebes iha tempu real-time.



Merkadu saham global opera ho volume transasaun ne'ebé boot no velosidade aas. Investor, trader, no analista presiza informasaun real-time atu halo desizaun investimentu ne'ebé bazeia ba dadus. Maibé, prosesamentu dadus saham real-time presiza teknologia Big Data ne'ebé kapás atu prosesa dadus streaming ho lalais no akurat.



Timor-Leste, hanesan nasaun ne'ebé foin independénsia, iha dependénsia boot ba setór minarai no gás. \*\*Dana Perminyakan (Petroleum Fund)\*\* Timor-Leste mak fundu riku-soin nasaun ne'ebé investe iha merkadu finanseiru global, inklui saham (Global Equities). Kompañia sira hanesan \*\*Santos Ltd\*\*, \*\*Woodside Energy\*\*, no \*\*Finder Energy\*\* iha ligasaun direita ho Timor-Leste tanba sira opera iha projetu minarai no gás iha área Timor-Leste.



\## 1.2 Problem Statement



Problema sira ne'ebé identifika:



1\. \*\*Lack of Real-Time Monitoring System:\*\* La iha sistema ida ne'ebé bele monitoriza movimentu saham kompañia minarai no gás ne'ebé iha ligasaun ho Timor-Leste iha tempu real-time.



2\. \*\*Manual Data Collection:\*\* Prosesu koleksaun dadus saham nafatin manual, la efisiente, no la akurat.



3\. \*\*Delayed Decision Making:\*\* Investor no stake-holder sira la iha aksesu ba informasaun real-time, hodi halo desizaun investimentu ne'ebé atrazadu.



4\. \*\*Lack of Data Analytics:\*\* La iha ferramenta analitiku ne'ebé bele kalkula indikador hanesan Moving Average, volatility, no deteksaun trend automátiku.



\## 1.3 Research Questions



1\. Oinsá dezenvolve sistema Big Data real-time pipeline atu prosesa dadus saham kompañia minarai no gás ne'ebé iha ligasaun ho Timor-Leste?



2\. Oinsá integra teknologia Apache Kafka no Apache Spark atu prosesa dadus streaming ho efisiente?



3\. Oinsá kalkula indikador analitiku hanesan Moving Average no deteksaun trend husi dadus saham real-time?



4\. Oinsá aprezenta rezultadu análize iha dashboard interaktivu ne'ebé bele asesu husi stake-holder sira?



\## 1.4 Project Objectives



\### Objetivu Jeral

Dezenvolve sistema análize streaming merkadu saham real-time ba kompañia minarai no gás ne'ebé iha ligasaun ho Timor-Leste, uza teknologia Big Data.



\### Objetivu Espesífiku

1\. Identifika no implementa fonte dadus online ba saham kompañia minarai no gás.

2\. Dezenvolve pipeline data ingestion uza Apache Kafka.

3\. Implementa stream processing uza Apache Spark Streaming.

4\. Implementa data storage uza PostgreSQL.

5\. Kalkula indikador analitiku: Moving Average (MA-5, MA-20), volatility, no trend.

6\. Dezenvolve dashboard interaktivu uza Streamlit.

7\. Dokumenta no demonstra sistema ho profisional.



### 1.5 Project Scope (In-Scope) — Ganti menjadi:

```markdown
### Iha Scope (In-Scope):
- Fonte dadus: yfinance API (Yahoo Finance) ba 5 saham: STO.AX, WDS.AX, FDR.AX, ENI.MI, ESR.AX
- Data ingestion: Apache Kafka 3.6.1 (KRaft mode)
- Stream processing: Apache Spark 3.5.0 Streaming
- Data storage: PostgreSQL 17 (4 tabel)
- Analytics: Moving Average, Volatility, Trend Detection
- Machine Learning: Linear Regression untuk prediksi harga
- Visualization: Streamlit Dashboard (5 tabs)
- Testing: Functional, Performance, Data Quality, Scalability
- Kontekstu: 5 saham ligasaun ho Timor-Leste


\### La Iha Scope (Out-of-Scope):

\- Trading otomátiku

\- Predisaun ML avançadu (LSTM, Prophet)

\- Mobile application

\- Multi-user authentication

\- Cloud deployment



\## 1.6 Benefit



\### Benefísiu ba Akademik:

\- Aplika teoria Big Data iha problema real

\- Komprende pipeline real-time end-to-end

\- Prátika teknologia indústria (Kafka, Spark, PostgreSQL)



\### Benefísiu ba Timor-Leste:

\- Sistema bele monitoriza saham kompañia minarai ne'ebé opera iha TL

\- Apoiu desizaun investimentu ba Dana Perminyakan

\- Kontribuisaun ba dezenvolvimentu kapasidade dijitál nasaun



\### Benefísiu ba Estudante:

\- Skill práktika iha Data Engineering

\- Portfóliu projetu Big Data

\- Preparasaun ba karreira iha indústria dadus

## 1.7 Rezultadu Finál

Projetu ida-ne'e **100% kompletu** ho:
- ✅ **Pipeline 5 Layer:** API → Kafka → Spark → PostgreSQL → Streamlit
- ✅ **5 Saham TL:** STO.AX, WDS.AX, FDR.AX, ENI.MI, ESR.AX
- ✅ **37.011+ Records** diproses
- ✅ **5 Tab Dashboard:** Real-Time, Volume, Trend, Analytics, Prediction
- ✅ **Machine Learning:** Linear Regression untuk prediksi 1 jam
- ✅ **4 Jenis Testing:** Functional, Performance, Quality, Scalability
- ✅ **11/12 Test PASS** (92% success rate)
