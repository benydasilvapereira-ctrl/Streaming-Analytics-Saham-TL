"""
SCALABILITY TESTING
Mengukur processing time untuk berbagai volume data.
"""

import psycopg2
import pandas as pd
import time
import json
from datetime import datetime


POSTGRES = {
    'host': 'localhost', 'port': 5432, 'user': 'postgres',
    'password': '6797', 'dbname': 'stock_db'
}


def get_conn():
    return psycopg2.connect(**POSTGRES)


def test_volume(conn, limit):
    """Test processing time untuk volume tertentu."""
    sql = f"""
        SELECT symbol, price, volume, inserted_at
        FROM stock_prices
        ORDER BY inserted_at DESC
        LIMIT {limit};
    """
    
    start = time.time()
    df = pd.read_sql(sql, conn)
    elapsed = time.time() - start
    
    return {
        'limit': limit,
        'records_returned': len(df),
        'time_seconds': round(elapsed, 4),
        'records_per_sec': round(len(df) / elapsed, 2) if elapsed > 0 else 0
    }


def test_aggregation(conn, limit):
    """Test aggregation query time."""
    sql = f"""
        SELECT 
            symbol,
            AVG(price) as avg_price,
            MAX(price) as max_price,
            MIN(price) as min_price,
            SUM(volume) as total_volume,
            COUNT(*) as data_points
        FROM (
            SELECT symbol, price, volume
            FROM stock_prices
            ORDER BY inserted_at DESC
            LIMIT {limit}
        ) sub
        GROUP BY symbol;
    """
    
    start = time.time()
    df = pd.read_sql(sql, conn)
    elapsed = time.time() - start
    
    return {
        'limit': limit,
        'groups': len(df),
        'time_seconds': round(elapsed, 4)
    }


def main():
    print("=" * 70)
    print("SCALABILITY TESTING — CAPSTONE PROJECT")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    conn = get_conn()
    
    # Total records tersedia
    df = pd.read_sql("SELECT COUNT(*) as total FROM stock_prices;", conn)
    total_records = int(df['total'].iloc[0])
    
    print(f"\n✓ Total records tersedia: {total_records:,}")
    
    # Test volumes
    volumes = [1000, 5000, 10000, 50000, 100000, 500000, 1000000]
    volumes = [v for v in volumes if v <= total_records]
    
    # Jika data < 1M, kita pakai data yang ada
    if total_records < 1000000:
        volumes = [1000, 5000, 10000, 50000, min(100000, total_records), total_records]
        volumes = sorted(set([v for v in volumes if v <= total_records]))
    
    print(f"✓ Volume yang akan di-test: {volumes}")
    
    # Test 1: Query Performance
    print("\n" + "=" * 70)
    print("TEST 1: QUERY PERFORMANCE (SELECT)")
    print("=" * 70)
    print(f"\n{'Volume':>10} {'Records':>10} {'Time (s)':>10} {'Recs/sec':>12}")
    print("-" * 50)
    
    query_results = []
    for v in volumes:
        result = test_volume(conn, v)
        query_results.append(result)
        print(f"{v:>10,} {result['records_returned']:>10,} {result['time_seconds']:>10.4f} {result['records_per_sec']:>12,.0f}")
    
    # Test 2: Aggregation Performance
    print("\n" + "=" * 70)
    print("TEST 2: AGGREGATION PERFORMANCE (GROUP BY)")
    print("=" * 70)
    print(f"\n{'Volume':>10} {'Groups':>10} {'Time (s)':>10}")
    print("-" * 40)
    
    agg_results = []
    for v in volumes:
        result = test_aggregation(conn, v)
        agg_results.append(result)
        print(f"{v:>10,} {result['groups']:>10} {result['time_seconds']:>10.4f}")
    
    conn.close()
    
    # Test 3: Scaling Analysis
    print("\n" + "=" * 70)
    print("TEST 3: SCALING ANALYSIS")
    print("=" * 70)
    
    if len(query_results) >= 2:
        first = query_results[0]
        last = query_results[-1]
        
        # Cek apakah linear scaling
        ratio_volume = last['limit'] / first['limit']
        ratio_time = last['time_seconds'] / first['time_seconds'] if first['time_seconds'] > 0 else 0
        
        print(f"✓ Volume ratio: {ratio_volume:.1f}x")
        print(f"✓ Time ratio: {ratio_time:.2f}x")
        
        if ratio_time < ratio_volume * 1.5:
            scaling = "LINEAR ✓"
            status = "PASS"
        elif ratio_time < ratio_volume * 3:
            scaling = "NEAR-LINEAR"
            status = "PASS"
        else:
            scaling = "NON-LINEAR"
            status = "WARN"
        
        print(f"✓ Scaling: {scaling}")
        print(f"\n[{status}] Scalability test")
    else:
        status = "WARN"
        print("[WARN] Tidak cukup data untuk scaling analysis")
    
    # Simpan hasil
    output = {
        'timestamp': datetime.now().isoformat(),
        'test_type': 'Scalability Testing',
        'total_records_available': total_records,
        'query_results': query_results,
        'aggregation_results': agg_results,
        'status': status
    }
    
    with open('scalability_test_result.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n✓ Hasil disimpan: scalability_test_result.json")
    print("=" * 70)


if __name__ == "__main__":
    main()