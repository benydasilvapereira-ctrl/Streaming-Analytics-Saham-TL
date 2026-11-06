"""
Kafka Producer untuk mengirim data saham Timor-Leste ke Kafka topic.

Cara menjalankan:
    cd 2_data_ingestion
    python kafka_producer.py

Pastikan:
1. Kafka server berjalan di port 9093
2. Topic 'stock-prices-tl' sudah dibuat
3. Virtual environment sudah aktif
"""

import json
import time
import sys
import os
from datetime import datetime

# Tambahkan parent directory ke sys.path agar bisa import dari 1_data_sources
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '1_data_sources'))

from kafka import KafkaProducer
# from kafka.errors import NoBrokersAvailable

from config import KAFKA_BROKER, KAFKA_TOPIC, POLL_INTERVAL_SECONDS
from api_client import fetch_stock_price, TIMOR_LESTE_STOCKS


def create_producer():
    """Membuat KafkaProducer dengan konfigurasi yang sesuai."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=[KAFKA_BROKER],
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3,
            linger_ms=10,
            request_timeout_ms=10000,
            api_version=(3, 6, 1),          # ⬅️ Paksa versi API Kafka 3.6.1
            api_version_auto_timeout_ms=10000,
        )
        print(f"[OK] Terhubung ke Kafka broker: {KAFKA_BROKER}")
        return producer
    except Exception as e:
        print(f"[FATAL] Tidak bisa terhubung ke Kafka broker: {KAFKA_BROKER}")
        print(f"[ERROR] Detail: {type(e).__name__}: {e}")
        print("Pastikan Kafka server berjalan. Cek dengan: netstat -ano | findstr :9093")
        return None

def send_stock_data(producer, stock_data):
    """
    Mengirim satu data saham ke Kafka topic.
    
    Args:
        producer: KafkaProducer instance
        stock_data (dict): Data saham dari api_client
    
    Returns:
        bool: True jika berhasil
    """
    try:
        symbol = stock_data['symbol']
        
        # Kirim dengan key=symbol agar semua data saham yang sama
        # masuk ke partisi yang sama (menjaga urutan)
        future = producer.send(
            KAFKA_TOPIC,
            key=symbol,
            value=stock_data
        )
        
        # Tunggu konfirmasi
        metadata = future.get(timeout=10)
        
        print(f"[SENT] {symbol:10} | Partition: {metadata.partition} | "
              f"Offset: {metadata.offset} | Price: ${stock_data['price']}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Gagal kirim {stock_data.get('symbol', '?')}: {e}")
        return False


def main():
    """Loop utama: fetch data dari API, kirim ke Kafka."""
    print("=" * 70)
    print("KAFKA PRODUCER - Stock Timor-Leste Streaming")
    print("=" * 70)
    print(f"Kafka Broker : {KAFKA_BROKER}")
    print(f"Kafka Topic  : {KAFKA_TOPIC}")
    print(f"Stocks       : {[s['symbol'] for s in TIMOR_LESTE_STOCKS]}")
    print(f"Interval     : {POLL_INTERVAL_SECONDS} detik")
    print("=" * 70)
    print("Tekan Ctrl+C untuk berhenti\n")
    
    producer = create_producer()
    if not producer:
        sys.exit(1)
    
    cycle = 0
    total_sent = 0
    total_failed = 0
    
    try:
        while True:
            cycle += 1
            print(f"\n--- Cycle #{cycle} | {datetime.now().strftime('%H:%M:%S')} ---")
            
            for stock_info in TIMOR_LESTE_STOCKS:
                stock_data = fetch_stock_price(stock_info)
                
                if stock_data:
                    if send_stock_data(producer, stock_data):
                        total_sent += 1
                    else:
                        total_failed += 1
                else:
                    print(f"[SKIP] {stock_info['symbol']} - tidak ada data")
                    total_failed += 1
                
                # Jeda antar request API (menghindari rate limit Yahoo)
                time.sleep(2)
            
            print(f"[STATS] Total terkirim: {total_sent} | Gagal: {total_failed}")
            print(f"[WAIT] Menunggu {POLL_INTERVAL_SECONDS} detik sebelum cycle berikutnya...")
            time.sleep(POLL_INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Dihentikan oleh user (Ctrl+C)")
    finally:
        producer.flush()
        producer.close()
        print(f"[STATS] Total pesan terkirim: {total_sent}")
        print(f"[STATS] Total gagal: {total_failed}")
        print("[OK] Kafka producer ditutup dengan bersih")


if __name__ == '__main__':
    main()