## ✅ Fase 6: Stream Processing (Spark → PostgreSQL) - SELESAI
- [x] `spark_streaming.py` berjalan tanpa error
- [x] `stock_prices`: 149 baris (raw data per event)
- [x] `stock_trends`: 6 baris (agregasi window 1 menit)
- [x] Checkpoint `raw` & `agg` berfungsi
- [x] Pipeline API → Kafka → Spark → PostgreSQL 100% berhasil

## ⏳ Fase 7: Analytics (Trend Analysis) - NEXT
## ⏳ Fase 8: Visualization (Streamlit)

## ✅ Recovery #2 - Checkpoint Corrupt (2026-09-14)
- **Masalah:** Checkpoint `agg` corrupt, Spark error `1.delta does not exist`
- **Penyebab:** Spark dihentikan paksa sebelumnya
- **Solusi:** Reset checkpoint `agg`, truncate `stock_trends`, restart Spark
- **Hasil:** Spark auto-recover, memproses backlog 24 baris di Epoch 905
- **Pelajaran:** Selalu hentikan Spark dengan Ctrl+C (tunggu `[OK] Spark Streaming dihentikan`)

## 📋 Checklist Startup Setiap Hari
1. [ ] Start PostgreSQL (start-pg.bat atau pg_ctl)
2. [ ] Start Kafka Server
3. [ ] Start Kafka Producer
4. [ ] Start Spark Streaming
5. [ ] Start Dashboard (streamlit run app.py)

## ⚠️ Catatan Penting: Startup Setiap Hari

Setiap kali laptop restart, jalankan urutan berikut:

### Cara Otomatis (RECOMMENDED):
Double-click: `start-all.bat` (di folder proyek)
→ Akan start PostgreSQL + Kafka + Producer + Spark

Kemudian double-click: `start-dashboard.bat`
→ Akan start Streamlit dashboard

### Cara Manual:
1. CMD 1: Start PostgreSQL
   CreSQL\17\logfile.txt start:\PostgreSQL\17\bin\pg_ctl -D C:\PostgreSQL\17\data -l C:\Postg

2. CMD 2: Start Kafka Server
   cd C:\kafka
   bin\windows\kafka-server-start.bat config\kraft\server-saham-tl.properties

3. CMD 3: Start Kafka Producer
   cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
   venv\Scripts\activate
   cd 2_data_ingestion
   python kafka_producer.py

4. CMD 4: Start Spark Streaming
   cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
   venv\Scripts\activate
   cd 3_stream_processing
   python spark_streaming.py

5. CMD 5: Start Streamlit Dashboard
   cd C:\Users\jacin\Documents\Streaming_AnalyticsSahamTL
   venv\Scripts\activate
   cd 6_visualization
   streamlit run app.py

## ⚠️ Troubleshooting Umum

| Masalah | Solusi |
|---------|--------|
| `'pg_ctl' is not recognized` | Gunakan path lengkap: `C:\PostgreSQL\17\bin\pg_ctl.exe` |
| `postgres.exe blocked by Device Guard` | Jalankan PowerShell Admin: `Get-ChildItem -Path "C:\PostgreSQL\17\bin" -Recurse \| Unblock-File` |
| `Connection to localhost:5432 refused` | PostgreSQL mati. Jalankan `start-pg.bat` |
| Kafka tidak bisa connect | Pastikan Kafka Server jalan di CMD terpisah |
| Spark error `NoBrokersAvailable` | Kafka Server mati atau port salah (pastikan 9093) |

## ✅ Penambahan 2 Saham Baru (2026-09-14) — SELESAI
- **ENI.MI** (Eni S.p.A.) — PSC TL-SO-22-23, partner TIMOR GAP ✅
- **ESR.AX** (Estrella Resources) — proyek mangan & batu gamping di TL ✅
- **Masalah:** Kolom `exchange` VARCHAR(10) terlalu sempit
- **Solusi:** ALTER TABLE → VARCHAR(50)
- **Hasil:** 5 saham aktif di pipeline, dashboard menampilkan lengkap
- **Bonus:** ENI.MI langsung masuk kategori NAIK (+0.25%)

## 📊 Total Saham dalam Pipeline
1. STO.AX — Santos Ltd (Bayu-Undan) — $8.73
2. WDS.AX — Woodside Energy (Greater Sunrise) — $33.08
3. FDR.AX — Finder Energy (KTJ) — $0.30
4. ENI.MI — Eni S.p.A. (PSC TL-SO-22-23) — $24.13 ⬅️ NAIK
5. ESR.AX — Estrella Resources (mangan & batu gamping) — $0.03

## 🎯 Status Proyek: 100% SELESAI
- Pipeline: ✅ API → Kafka → Spark → PostgreSQL → Dashboard
- 5 saham TL: ✅ Berjalan
- Analytics: ✅ MA, Trend, Perubahan Harga
- Visualisasi: ✅ Modern & Interaktif

## ✅ Status Final: 5 Saham Terintegrasi (2026-09-15)
- Total records: 5.059 (stock_prices)
- Total windows: 15 (stock_trends)
- 5 saham: STO.AX, WDS.AX, FDR.AX, ENI.MI, ESR.AX
- Pipeline: 100% berjalan
- Dashboard: 5 saham di semua section

