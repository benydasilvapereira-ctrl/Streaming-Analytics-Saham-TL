"""
Trend Analysis - Moving Average, Volatility, Trend Detection

Membaca data dari tabel stock_prices,
menghitung indikator analitik,
lalu menyimpan ke tabel stock_analytics.
"""

import psycopg2
import pandas as pd
import numpy as np
from datetime import datetime


# ==================== KONFIGURASI ====================
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "6797"
POSTGRES_DB = "stock_db"


def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )


def analyze_symbol(conn, symbol):
    """Analisis satu simbol saham."""
    sql = """
        SELECT price, inserted_at
        FROM stock_prices
        WHERE symbol = %s
        ORDER BY inserted_at DESC
        LIMIT 50;
    """
    df = pd.read_sql(sql, conn, params=(symbol,))

    if len(df) < 5:
        return None

    df = df.sort_values('inserted_at').reset_index(drop=True)
    prices = df['price'].values

    ma_5 = float(np.mean(prices[-5:])) if len(prices) >= 5 else None
    ma_20 = float(np.mean(prices[-20:])) if len(prices) >= 20 else None
    volatility = float(np.std(prices)) if len(prices) > 1 else 0

    latest_price = float(prices[-1])
    price_change_pct = 0
    trend = "SIDEWAYS"

    if ma_5 is not None and ma_20 is not None:
        if ma_5 > ma_20 * 1.01:
            trend = "UP"
        elif ma_5 < ma_20 * 0.99:
            trend = "DOWN"
        else:
            trend = "SIDEWAYS"

        price_change_pct = ((ma_5 - ma_20) / ma_20) * 100

    return {
        'symbol': symbol,
        'ma_5': round(ma_5, 4) if ma_5 else None,
        'ma_20': round(ma_20, 4) if ma_20 else None,
        'volatility': round(volatility, 4),
        'trend': trend,
        'latest_price': round(latest_price, 4),
        'price_change_pct': round(price_change_pct, 4),
        'data_points': len(prices)
    }


def save_analytics(conn, analytics_list):
    """Simpan hasil analytics ke tabel stock_analytics."""
    sql = """
        INSERT INTO stock_analytics 
        (symbol, ma_5, ma_20, volatility, trend, latest_price, price_change_pct, data_points)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur = conn.cursor()
    for a in analytics_list:
        cur.execute(sql, (
            a['symbol'], a['ma_5'], a['ma_20'],
            a['volatility'], a['trend'],
            a['latest_price'], a['price_change_pct'], a['data_points']
        ))
    conn.commit()
    cur.close()


def main():
    print("=" * 70)
    print("TREND ANALYSIS - Moving Average & Volatility")
    print("=" * 70)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    conn = get_connection()

    df_symbols = pd.read_sql("SELECT DISTINCT symbol FROM stock_prices ORDER BY symbol;", conn)
    symbols = df_symbols['symbol'].tolist()

    print(f"\nSimbol ditemukan: {symbols}\n")

    analytics_list = []
    for symbol in symbols:
        print(f"[ANALYZE] {symbol}...")
        result = analyze_symbol(conn, symbol)
        if result:
            analytics_list.append(result)
            print(f"  MA-5:  {result['ma_5']}")
            print(f"  MA-20: {result['ma_20']}")
            print(f"  Volatility: {result['volatility']}")
            print(f"  Trend: {result['trend']}")
            print(f"  Price: ${result['latest_price']} ({result['price_change_pct']:+.2f}%)")
            print(f"  Data points: {result['data_points']}\n")
        else:
            print(f"  [SKIP] Data tidak cukup\n")

    if analytics_list:
        print(f"[SAVE] Menyimpan {len(analytics_list)} hasil analytics...")
        save_analytics(conn, analytics_list)
        print("[OK] Data tersimpan di tabel stock_analytics\n")

    conn.close()

    print("=" * 70)
    print("[DONE] Trend analysis selesai")
    print("=" * 70)


if __name__ == "__main__":
    main()