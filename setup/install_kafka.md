# Catatan Setup Kafka untuk Proyek Streaming_AnalyticsSahamTL

## Status
- Java: OpenJDK 17.0.20 (Temurin) ✅
- Kafka: 3.6.1 (Scala 2.13) ✅
- Mode: KRaft (isolasi dari proyek lama)
- Port: **9093** (proyek lama pakai 9092)
- Cluster ID: `oUMWQMcaQvajRVvX04neoQ`

## Lokasi
- Kafka: `C:\kafka`
- Config: `C:\kafka\config\kraft\server-saham-tl.properties`
- Data: `C:\kafka\data-saham-tl\kafka-logs`

## Cara Menjalankan Kafka (Terminal 1)
```cmd
cd C:\kafka
bin\windows\kafka-server-start.bat config\kraft\server-saham-tl.properties