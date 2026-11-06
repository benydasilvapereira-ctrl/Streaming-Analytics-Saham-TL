\# KAPÍTULU 5 — RESULTADU NO DISKUSAUN



\## 5.1 Rezultadu Sistema



\### 5.1.1 Status Pipeline End-to-End



Sistema Big Data pipeline ne'ebé dezenvolve \*\*100% funsiona\*\* ho komponente hotu berjalan:



| Komponen | Status | Bukti |

|----------|:------:|-------|

| Data Sources (yfinance API) | ✅ | 3 saham TL (STO.AX, WDS.AX, FDR.AX) |

| Data Ingestion (Apache Kafka) | ✅ | Topic `stock-prices-tl` aktif di port 9093 |

| Stream Processing (Spark) | ✅ | 1.655+ epoch, tanpa error |

| Data Storage (PostgreSQL) | ✅ | 3 tabel aktif |

| Visualization (Streamlit) | ✅ | Dashboard di http://localhost:8501 |

| Analytics (MA, Trend) | ✅ | Indikador kalkuladu otomátiku |



### 5.1.2 Data Collected (Hasil Akhir)

| Tabel | Jumlah Rekorde | Deskrisaun |
|-------|:--------------:|-----------|
| `stock_prices` | **37.011** | Dadus mentah per event |
| `stock_trends` | **28.188** | Agregasaun window 1 menit |
| `stock_analytics` | **273** | Indikador analitiku (MA, trend) |
| `stock_predictions` | **20** | Hasil prediksi ML |

**Data Rate:**
- **Interval:** 10 segundu per saham
- **Total:** ~13 events/minutu
- **Per saham:** ~2,6 events/minutu


\### 5.1.3 Distribusi Data



| Saham | Kompania | Records |
|-------|----------|--------:|
| ENI.MI | Eni S.p.A. | 6.537 |
| ESR.AX | Estrella Resources | 6.590 |
| FDR.AX | Finder Energy | 7.959 |
| STO.AX | Santos Ltd | 7.926 |
| WDS.AX | Woodside Energy | 7.953 |
| **Total** | | **37.011** |



Distribusi relatif balans entre saham sira.



\## 5.2 Rezultadu Analytics



\### 5.2.1 Moving Average (MA-5, MA-20)



\*\*Hasil ba kada saham:\*\*



| Saham | MA-5 | MA-20 | Trend | Volatility |
|-------|:----:|:-----:|:-----:|:----------:|
| STO.AX | 8.54 | 8.55 | SIDEWAYS | 0.0711 |
| WDS.AX | 31.50 | 31.60 | SIDEWAYS | 0.2122 |
| FDR.AX | 0.285 | 0.290 | DOWN | 0.0015 |
| ENI.MI | 24.41 | 24.37 | SIDEWAYS | 0.0545 |
| ESR.AX | 0.026 | 0.027 | SIDEWAYS | 0.0005 |



\*\*Analisis:\*\*

\- Nilai MA-5 = MA-20 karena \*\*pasar saham ASX tutup\*\* durante teste

\- Trend `SIDEWAYS` menunjukka harga stabil

\- Volatility 0 mengkonfirma la iha flutuasaun



\*\*⚠️ Catatan:\*\* Bainhira pasar ASX loke (10:00-16:00 AEST), MA-5 no MA-20 sei diferente no trend sei muda.



\### 5.2.2 Trend Detection



Algoritmu deteksaun trend:


**Interpretasaun:**
- **UP** — Trend aumenta (bullish)
- **DOWN** — Trend tun (bearish)
- **SIDEWAYS** — Harga stabil (konsolidasaun)

### 5.2.3 Window Aggregation

**Hasil agregasaun 1 minutu (conto):**

| Symbol | Window Start | Avg Price | Max | Min | Total Volume | Data Points |
|--------|--------------|-----------|-----|-----|--------------|:-----------:|
| STO.AX | 14:38:00 | $8.59 | $8.59 | $8.59 | 13,393,144 | 4 |
| WDS.AX | 14:38:00 | $32.86 | $32.86 | $32.86 | 1,600 | 4 |
| FDR.AX | 14:38:00 | $0.31 | $0.31 | $0.31 | 21,260 | 4 |

**Insight:**
- Total volume agregadu per window
- Data points menunjukka konsisténsia eventu
- Max = Min = Avg durante pasa tutup

## 5.3 Rezultadu Dashboard

### 5.3.1 KPI Cards

| KPI | Nilai (sample) |
|-----|:--------------:|
| Total Records | 2.161 |
| Total Volume | 419,255,840+ |
| Aggregation Windows | 82 |
| Last Data Timestamp | Real-time |

### 5.3.2 Charts

**Tab 1 — Harga Real-Time:**
- Line chart 3 saham (STO.AX, WDS.AX, FDR.AX)
- Markers per data point
- Hover tooltip interaktivu

**Tab 2 — Volume & Distribusi:**
- Bar chart volume per saham
- Pie chart distribusi data

**Tab 3 — Agregasaun Window:**
- Line chart avg price per window
- Tabel detail agregasaun

**Tab 4 — Analytics:**
- Bar chart MA-5 vs MA-20
- Trend badge per saham
- Tabel indikador analytics

### 5.3.3 Fitur Interaktivu

| Fitur | Deskrisaun |
|-------|-----------|
| Auto-refresh | Update otomátiku 5-60 detik |
| Time Range | Filtru 50-1000 data points |
| Symbol Filter | Multiselect saham |
| Tabs | 4 tab ho chart oioin |
| Hover | Tooltip detallu |
| Zoom/Pan | Interaktivu |

## 5.4 Performa Sistema

### 5.4.1 Laténsia End-to-End

**Ukuran laténsia husi source to dashboard:**

| Fase | Laténsia Estimadu |
|------|-------------------|
| yfinance API fetch | ~500ms |
| Kafka producer → topic | ~10ms |
| Kafka → Spark read | ~2 detik (trigger) |
| Spark process → PostgreSQL | ~200ms |
| Dashboard query | ~100ms |
| **Total end-to-end** | **~3 detik** |

### 5.4.2 Throughput

| Metrik | Nilai |
|--------|-------|
| Events per minute | ~30 |
| Events per hour | ~1.800 |
| Records processed (cumulative) | 2.161 |
| Spark batch trigger | ~2 detik |

### 5.4.3 Resource Usage

| Resource | Usage |
|----------|-------|
| CPU (Spark local mode) | ~40-60% (multi-core) |
| Memory (Spark) | ~1-2 GB |
| Memory (Kafka) | ~500 MB |
| Memory (PostgreSQL) | ~200 MB |
| Disk (Kafka logs) | ~100 MB |

## 5.5 Diskusaun

### 5.5.1 Tantangan ne'ebé Hasil

**Tantangan 1: Python Version Mismatch**
- **Problema:** PySpark 3.5.0 la suporta Python 3.13
- **Solusaun:** Kriа venv foun ho Python 3.11.8
- **Pelajaran:** Verifika kompatibilidade versaun antes hahu

**Tantangan 2: Kafka Python Library**
- **Problema:** `kafka-python` 2.0.2 la funciona ho Python 3.13
- **Solusaun:** Uza `kafka-python-ng` (fork ativu)
- **Pelajaran:** Uza biblioteka ne'ebé maintido

**Tantangan 3: Hadoop Native Files**
- **Problema:** Spark presiza `winutils.exe` no `hadoop.dll` iha Windows
- **Solusaun:** Download husi repositoriu winutils (Hadoop 3.3.4)
- **Pelajaran:** Windows presiza file native ba Spark

**Tantangan 4: Checkpoint Corrupt**
- **Problema:** Checkpoint `agg` corrupt bainhira Spark hentikan paksa
- **Solusaun:** Reset checkpoint + truncate tabel
- **Pelajaran:** Hentikan Spark ho Ctrl+C, la'ós paksa

**Tantangan 5: Smart App Control Block**
- **Problema:** Windows Smart App Control bloke `postgres.exe`
- **Solusaun:** `Unblock-File` iha PowerShell Admin
- **Pelajaran:** Binary ZIP husi internet presiza unblock

### 5.5.2 Pontu Forte Sistema

1. **End-to-End Integration** — 6 komponente integradus
2. **Real-Time Processing** — Laténsia ~3 detik
3. **Scalable** — Bele aumenta saham no volume
4. **Fault Tolerant** — Checkpoint & recovery
5. **Visualization Modern** — Dashboard interaktivu
6. **Analytics Integration** — MA, volatility, trend

### 5.5.3 Limitasaun

1. **Local Mode Spark** — La uza cluster distribuídu
2. **Free API Limit** — yfinance iha delay ~15 min
3. **Single Broker Kafka** — La iha replication
4. **Manual Start** — La iha auto-start service
5. **Fixed Window** — Deit 1 minutu, la configurable

### 5.5.4 Komparasaun ho Sistema Seluk

| Aspektu | Sistema Ida-ne'e | Tradisional Monitoring |
|---------|:----------------:|:----------------------:|
| Real-Time | ✅ Streaming | ❌ Manual polling |
| Scalability | ✅ Horizontal | ❌ Vertical |
| Analytics | ✅ Automated | ❌ Manual Excel |
| Laténsia | ~3 detik | ~oras |
| Cost | Gratis (open source) | Lisensa karu |

## 5.6 Machine Learning — Prediksi Harga Saham

### 5.6.1 Model Linear Regression

**Fitur (10):** price, volume, ma_5, ma_20, hour, minute, day_of_week, price_lag_1, price_lag_2, volume_lag_1

**Target:** Harga 1 jam ke depan

### 5.6.2 Rezultadu Training

| Symbol | Records | Training | Testing | MAE | RMSE | R² | MAPE |
|--------|:-------:|:--------:|:-------:|:---:|:----:|:--:|:----:|
| STO.AX | 5.534 | 4.364 | 1.091 | $0.0764 | $0.0815 | -29.27 | 0.89% |
| WDS.AX | 5.550 | 4.376 | 1.095 | $0.0245 | $0.0322 | **0.5629** | 0.08% |
| FDR.AX | 5.551 | 4.377 | 1.095 | $0.0020 | $0.0049 | **0.6624** | 0.72% |
| ENI.MI | 4.176 | 3.277 | 820 | $0.0814 | $0.1045 | -0.3096 | 0.34% |
| ESR.AX | 4.287 | 3.366 | 842 | $0.0016 | $0.0020 | -2.7676 | 6.11% |

### 5.6.3 Hasil Prediksi

| Symbol | Harga Skrg | Prediksi | Perubahan | Trend |
|--------|:----------:|:--------:|:---------:|:-----:|
| STO.AX | $8.56 | $8.67 | +1.33% | 📈 NAIK |
| WDS.AX | $31.72 | $31.74 | +0.05% | ➡️ STABIL |
| FDR.AX | $0.285 | $0.284 | -0.53% | 📉 TURUN |
| ENI.MI | $24.11 | $23.99 | -0.50% | 📉 TURUN |
| ESR.AX | $0.026 | $0.030 | +13.46% | 📈 NAIK |

### 5.6.4 Dashboard Integration

Tab 5 "Prediction (ML)" menampilkan:
- Stock Prediction Cards (5 saham)
- Bar Chart Perbandingan (Harga Skrg vs Prediksi)
- Table Detail Prediksi
- Summary Metrics

## 5.7 Rezultadu Testing

### 5.7.1 Functional Testing — 4/4 PASS

| Test | Status |
|------|:------:|
| Data Masuk | ✅ PASS |
| Data Diproses | ✅ PASS |
| Data Disimpan | ✅ PASS |
| Dashboard Funsiona | ✅ PASS |

### 5.7.2 Performance Testing — 2/3 PASS

| Metric | Target | Aktual | Status |
|--------|--------|--------|:------:|
| Latency | < 30 detik | 2,12 detik | ✅ |
| Throughput | ≥ 10/menit | 13,3/menit | ✅ |
| CPU/Memory | < 80% | CPU 78,8%, Mem 94,1% | ⚠️ |

### 5.7.3 Data Quality Testing — 4/4 PASS

| Test | Hasil | Status |
|------|-------|:------:|
| Missing Values | 0 | ✅ |
| Duplicate | 0 | ✅ |
| Invalid | 0 | ✅ |
| Outliers | 0% | ✅ |

### 5.7.4 Scalability Testing — PASS

| Volume | Time (s) | Recs/sec |
|--------|:--------:|---------:|
| 1.000 | 0,0132 | 75.830 |
| 5.000 | 0,0508 | 98.428 |
| 10.000 | 0,0657 | 152.127 |
| 37.011 | 0,3047 | 121.462 |

**Scaling:** LINEAR ✅