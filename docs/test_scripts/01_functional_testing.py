"""
FUNCTIONAL TESTING
Menguji 4 aspek fungsional:
1. Data masuk?
2. Data diproses dengan benar?
3. Data disimpan dengan benar?
4. Dashboard berfungsi?
"""

import psycopg2
import pandas as pd
from datetime import datetime
import json


POSTGRES = {
    'host': 'localhost', 'port': 5432, 'user': 'postgres',
    'password': '6797', 'dbname': 'stock_db'
}


def get_conn():
    return psycopg2.connect(**POSTGRES)


def test_1_data_masuk():
    """Test 1: Apakah data masuk ke sistem?"""
    print("\n" + "=" * 70)
    print("TEST 1: DATA MASUK (Data Ingestion)")
    print("=" * 70)
    
    conn = get_conn()
    
    # Cek apakah ada data di stock_prices
    df = pd.read_sql("SELECT COUNT(*) as total FROM stock_prices;", conn)
    total = int(df['total'].iloc[0])
    
    # Cek data terbaru (dalam 5 menit terakhir)
    df_recent = pd.read_sql("""
        SELECT COUNT(*) as recent 
        FROM stock_prices 
        WHERE inserted_at >= NOW() - INTERVAL '5 minutes';
    """, conn)
    recent = int(df_recent['recent'].iloc[0])
    
    # Cek distribusi per saham
    df_symbols = pd.read_sql("""
        SELECT symbol, COUNT(*) as count 
        FROM stock_prices 
        GROUP BY symbol 
        ORDER BY symbol;
    """, conn)
    
    conn.close()
    
    print(f"✓ Total records: {total:,}")
    print(f"✓ Records dalam 5 menit terakhir: {recent}")
    print(f"✓ Distribusi per saham:")
    for _, row in df_symbols.iterrows():
        print(f"    {row['symbol']:10} : {row['count']:,} records")
    
    # Validasi
    status = "PASS" if total > 0 and recent > 0 else "FAIL"
    print(f"\n[{status}] Data masuk ke sistem")
    
    return {
        'test': 'Data Masuk',
        'total_records': total,
        'recent_5min': recent,
        'symbols': len(df_symbols),
        'status': status
    }


def test_2_data_diproses():
    """Test 2: Apakah data diproses dengan benar?"""
    print("\n" + "=" * 70)
    print("TEST 2: DATA DIPROSES (Stream Processing)")
    print("=" * 70)
    
    conn = get_conn()
    
    # Cek stock_trends (agregasi window)
    df_trends = pd.read_sql("SELECT COUNT(*) as total FROM stock_trends;", conn)
    total_trends = int(df_trends['total'].iloc[0])
    
    # Cek window unik
    df_windows = pd.read_sql("""
        SELECT COUNT(DISTINCT window_start) as windows FROM stock_trends;
    """, conn)
    windows = int(df_windows['windows'].iloc[0])
    
    # Cek agregasi valid (avg antara min & max)
    df_valid = pd.read_sql("""
        SELECT COUNT(*) as invalid
        FROM stock_trends
        WHERE avg_price < min_price OR avg_price > max_price;
    """, conn)
    invalid = int(df_valid['invalid'].iloc[0])
    
    # Cek data_points > 0
    df_dp = pd.read_sql("""
        SELECT COUNT(*) as empty_windows
        FROM stock_trends
        WHERE data_points <= 0;
    """, conn)
    empty = int(df_dp['empty_windows'].iloc[0])
    
    conn.close()
    
    print(f"✓ Total trend records: {total_trends}")
    print(f"✓ Aggregation windows: {windows}")
    print(f"✓ Invalid agregasi (avg < min / avg > max): {invalid}")
    print(f"✓ Empty windows (data_points <= 0): {empty}")
    
    # Validasi
    status = "PASS" if total_trends > 0 and invalid == 0 and empty == 0 else "FAIL"
    print(f"\n[{status}] Data diproses dengan benar")
    
    return {
        'test': 'Data Diproses',
        'total_trends': total_trends,
        'windows': windows,
        'invalid': invalid,
        'empty': empty,
        'status': status
    }


def test_3_data_disimpan():
    """Test 3: Apakah data disimpan dengan benar?"""
    print("\n" + "=" * 70)
    print("TEST 3: DATA DISIMPAN (Data Storage)")
    print("=" * 70)
    
    conn = get_conn()
    
    # Cek 4 tabel utama
    df_tables = pd.read_sql("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
          AND table_name IN ('stock_prices', 'stock_trends', 'stock_analytics', 'stock_predictions')
        ORDER BY table_name;
    """, conn)
    
    tables = df_tables['table_name'].tolist()
    
    # Cek struktur stock_prices
    df_cols = pd.read_sql("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'stock_prices'
        ORDER BY ordinal_position;
    """, conn)
    
    # Cek data tersimpan di setiap tabel
    counts = {}
    for table in ['stock_prices', 'stock_trends', 'stock_analytics', 'stock_predictions']:
        df = pd.read_sql(f"SELECT COUNT(*) as c FROM {table};", conn)
        counts[table] = int(df['c'].iloc[0])
    
    conn.close()
    
    print(f"✓ Tabel ditemukan: {len(tables)}")
    for t in tables:
        print(f"    - {t}: {counts.get(t, 0):,} records")
    
    print(f"\n✓ Struktur stock_prices ({len(df_cols)} kolom):")
    for _, row in df_cols.head(10).iterrows():
        print(f"    - {row['column_name']:20} : {row['data_type']}")
    
    # Validasi
    status = "PASS" if len(tables) == 4 and all(c > 0 for c in counts.values()) else "FAIL"
    print(f"\n[{status}] Data disimpan dengan benar")
    
    return {
        'test': 'Data Disimpan',
        'tables': len(tables),
        'counts': counts,
        'status': status
    }


def test_4_dashboard():
    """Test 4: Apakah dashboard berfungsi?"""
    print("\n" + "=" * 70)
    print("TEST 4: DASHBOARD FUNGSI")
    print("=" * 70)
    
    conn = get_conn()
    
    # Cek data untuk KPI Cards
    df_kpi = pd.read_sql("""
        SELECT 
            (SELECT COUNT(*) FROM stock_prices) as total_records,
            (SELECT SUM(volume) FROM stock_prices) as total_volume,
            (SELECT COUNT(DISTINCT window_start) FROM stock_trends) as total_windows,
            (SELECT MAX(inserted_at) FROM stock_prices) as last_data;
    """, conn)
    
    # Cek data untuk Stock Cards (harga terakhir per saham)
    df_stocks = pd.read_sql("""
        SELECT DISTINCT ON (symbol)
            symbol, price, volume, inserted_at
        FROM stock_prices
        ORDER BY symbol, inserted_at DESC;
    """, conn)
    
    # Cek data untuk Prediction (ML)
    df_pred = pd.read_sql("""
        SELECT COUNT(*) as total FROM stock_predictions;
    """, conn)
    predictions = int(df_pred['total'].iloc[0])
    
    conn.close()
    
    kpi = df_kpi.iloc[0]
    print(f"✓ KPI Cards siap:")
    print(f"    - Total Records: {int(kpi['total_records']):,}")
    print(f"    - Total Volume: {int(kpi['total_volume']):,}")
    print(f"    - Aggregation Windows: {int(kpi['total_windows'])}")
    print(f"    - Last Data: {kpi['last_data']}")
    
    print(f"\n✓ Stock Cards ({len(df_stocks)} saham):")
    for _, row in df_stocks.iterrows():
        print(f"    - {row['symbol']:10} : ${row['price']:.4f} (Vol: {int(row['volume']):,})")
    
    print(f"\n✓ Prediction Cards: {predictions} saham")
    
    # Validasi
    status = "PASS" if int(kpi['total_records']) > 0 and len(df_stocks) == 5 else "FAIL"
    print(f"\n[{status}] Dashboard berfungsi")
    
    return {
        'test': 'Dashboard',
        'kpi_ready': True,
        'stocks': len(df_stocks),
        'predictions': predictions,
        'status': status
    }


def main():
    print("=" * 70)
    print("FUNCTIONAL TESTING — CAPSTONE PROJECT")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = []
    
    # Jalankan 4 test
    results.append(test_1_data_masuk())
    results.append(test_2_data_diproses())
    results.append(test_3_data_disimpan())
    results.append(test_4_dashboard())
    
    # Ringkasan
    print("\n" + "=" * 70)
    print("RINGKASAN FUNCTIONAL TESTING")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    print(f"{'Test':<25} {'Status':<10}")
    print("-" * 40)
    for r in results:
        print(f"{r['test']:<25} {r['status']:<10}")
    print("-" * 40)
    print(f"PASSED: {passed}/{len(results)}")
    print(f"FAILED: {failed}/{len(results)}")
    
    # Simpan hasil ke JSON
    output = {
        'timestamp': datetime.now().isoformat(),
        'test_type': 'Functional Testing',
        'total_tests': len(results),
        'passed': passed,
        'failed': failed,
        'results': results
    }
    
    with open('functional_test_result.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n✓ Hasil disimpan: functional_test_result.json")
    print("=" * 70)


if __name__ == "__main__":
    main()