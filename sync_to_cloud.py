import psycopg2
import time
from datetime import datetime

# === KONFIGURASI ===
# PostgreSQL Lokal (Laptop)
LOCAL_DB = {
    'host': 'localhost', 'port': 5432, 'user': 'postgres',
    'password': '6797', 'dbname': 'stock_db'
}

# Supabase (Cloud) - GANTI DENGAN CONNECTION STRING ANDA
SUPABASE_URI = "postgresql://postgres:SahamTL2026!@db.abcdefghijklm.supabase.co:5432/postgres"

def sync_data():
    try:
        # 1. Koneksi ke Database Lokal
        local_conn = psycopg2.connect(**LOCAL_DB)
        local_cur = local_conn.cursor()

        # Ambil ID terakhir yang ada di Supabase untuk menghindari duplikasi
        cloud_conn = psycopg2.connect(SUPABASE_URI)
        cloud_cur = cloud_conn.cursor()
        cloud_cur.execute("SELECT MAX(id) FROM stock_prices;")
        last_id = cloud_cur.fetchone()[0] or 0

        # 2. Ambil data baru dari lokal
        local_cur.execute("""
            SELECT id, symbol, name, exchange, price, open, high, low, volume,
                   event_timestamp, source, fetched_at, inserted_at
            FROM stock_prices
            WHERE id > %s
            ORDER BY id ASC
            LIMIT 500;
        """, (last_id,))
        rows = local_cur.fetchall()

        if not rows:
            print(f"[{datetime.now()}] Tidak ada data baru.")
            return

        # 3. Kirim ke Supabase
        insert_query = """
            INSERT INTO stock_prices
            (id, symbol, name, exchange, price, open, high, low, volume,
             event_timestamp, source, fetched_at, inserted_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cloud_cur.executemany(insert_query, rows)
        cloud_conn.commit()
        print(f"[{datetime.now()}] Berhasil sinkronisasi {len(rows)} baris.")

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        if 'local_conn' in locals(): local_conn.close()
        if 'cloud_conn' in locals(): cloud_conn.close()

if __name__ == "__main__":
    print("Memulai sinkronisasi data ke Supabase...")
    while True:
        sync_data()
        time.sleep(30)  # Cek data baru setiap 30 detik