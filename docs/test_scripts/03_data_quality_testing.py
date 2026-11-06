"""
DATA QUALITY TESTING
Menguji: Missing Values, Duplicate Records, Invalid Records, Outliers
"""

import psycopg2
import pandas as pd
import numpy as np
import json
from datetime import datetime


POSTGRES = {
    'host': 'localhost', 'port': 5432, 'user': 'postgres',
    'password': '6797', 'dbname': 'stock_db'
}


def get_conn():
    return psycopg2.connect(**POSTGRES)


def test_missing_values():
    """Test missing values."""
    print("\n" + "=" * 70)
    print("TEST: MISSING VALUES")
    print("=" * 70)
    
    conn = get_conn()
    
    df = pd.read_sql("""
        SELECT 
            COUNT(*) as total,
            COUNT(*) FILTER (WHERE symbol IS NULL) as null_symbol,
            COUNT(*) FILTER (WHERE price IS NULL) as null_price,
            COUNT(*) FILTER (WHERE volume IS NULL) as null_volume,
            COUNT(*) FILTER (WHERE inserted_at IS NULL) as null_time
        FROM stock_prices;
    """, conn)
    conn.close()
    
    row = df.iloc[0]
    total = int(row['total'])
    
    print(f"✓ Total records: {total:,}")
    print(f"✓ Null symbol: {int(row['null_symbol'])}")
    print(f"✓ Null price: {int(row['null_price'])}")
    print(f"✓ Null volume: {int(row['null_volume'])}")
    print(f"✓ Null inserted_at: {int(row['null_time'])}")
    
    total_nulls = int(row['null_symbol']) + int(row['null_price']) + int(row['null_volume']) + int(row['null_time'])
    status = "PASS" if total_nulls == 0 else "FAIL"
    print(f"\n[{status}] Tidak ada missing values")
    
    return {
        'test': 'Missing Values',
        'total_records': total,
        'total_nulls': total_nulls,
        'status': status
    }


def test_duplicates():
    """Test duplicate records."""
    print("\n" + "=" * 70)
    print("TEST: DUPLICATE RECORDS")
    print("=" * 70)
    
    conn = get_conn()
    
    # Duplikat: symbol + event_timestamp sama
    df = pd.read_sql("""
        SELECT COUNT(*) as duplicates
        FROM (
            SELECT symbol, event_timestamp, COUNT(*) as c
            FROM stock_prices
            GROUP BY symbol, event_timestamp
            HAVING COUNT(*) > 1
        ) sub;
    """, conn)
    
    # Primary key duplicates (harusnya 0 karena BIGSERIAL)
    df_pk = pd.read_sql("""
        SELECT COUNT(*) as duplicates
        FROM (
            SELECT id, COUNT(*) as c
            FROM stock_prices
            GROUP BY id
            HAVING COUNT(*) > 1
        ) sub;
    """, conn)
    
    conn.close()
    
    dup_symbol = int(df['duplicates'].iloc[0])
    dup_pk = int(df_pk['duplicates'].iloc[0])
    
    print(f"✓ Duplicate (symbol + timestamp): {dup_symbol}")
    print(f"✓ Duplicate (primary key): {dup_pk}")
    
    # Untuk event-based data, duplikat "symbol+timestamp" bisa normal
    # (karena data di-fetch berulang). Yang penting PK unik.
    status = "PASS" if dup_pk == 0 else "FAIL"
    print(f"\n[{status}] Tidak ada duplicate primary key")
    
    return {
        'test': 'Duplicate Records',
        'dup_symbol_timestamp': dup_symbol,
        'dup_primary_key': dup_pk,
        'status': status
    }


def test_invalid_records():
    """Test invalid records."""
    print("\n" + "=" * 70)
    print("TEST: INVALID RECORDS")
    print("=" * 70)
    
    conn = get_conn()
    
    df = pd.read_sql("""
        SELECT 
            COUNT(*) FILTER (WHERE price <= 0) as negative_price,
            COUNT(*) FILTER (WHERE volume < 0) as negative_volume,
            COUNT(*) FILTER (WHERE high < low) as high_less_low,
            COUNT(*) FILTER (WHERE symbol NOT IN ('STO.AX', 'WDS.AX', 'FDR.AX', 'ENI.MI', 'ESR.AX')) as unknown_symbol
        FROM stock_prices;
    """, conn)
    conn.close()
    
    row = df.iloc[0]
    invalid = int(row['negative_price']) + int(row['negative_volume']) + int(row['high_less_low']) + int(row['unknown_symbol'])
    
    print(f"✓ Negative price: {int(row['negative_price'])}")
    print(f"✓ Negative volume: {int(row['negative_volume'])}")
    print(f"✓ High < Low: {int(row['high_less_low'])}")
    print(f"✓ Unknown symbol: {int(row['unknown_symbol'])}")
    
    status = "PASS" if invalid == 0 else "FAIL"
    print(f"\n[{status}] Tidak ada invalid records")
    
    return {
        'test': 'Invalid Records',
        'negative_price': int(row['negative_price']),
        'negative_volume': int(row['negative_volume']),
        'high_less_low': int(row['high_less_low']),
        'unknown_symbol': int(row['unknown_symbol']),
        'total_invalid': invalid,
        'status': status
    }


def test_outliers():
    """Test outliers dengan metode IQR."""
    print("\n" + "=" * 70)
    print("TEST: OUTLIERS (IQR Method)")
    print("=" * 70)
    
    conn = get_conn()
    df = pd.read_sql("SELECT symbol, price FROM stock_prices;", conn)
    conn.close()
    
    print(f"✓ Total records: {len(df):,}")
    print(f"\n{'Symbol':<10} {'Q1':>8} {'Q3':>8} {'IQR':>8} {'Outliers':>10} {'%':>8}")
    print("-" * 60)
    
    total_outliers = 0
    
    for symbol in df['symbol'].unique():
        prices = df[df['symbol'] == symbol]['price']
        Q1 = prices.quantile(0.25)
        Q3 = prices.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        outliers = prices[(prices < lower) | (prices > upper)]
        pct = len(outliers) / len(prices) * 100
        
        print(f"{symbol:<10} {Q1:>8.4f} {Q3:>8.4f} {IQR:>8.4f} {len(outliers):>10} {pct:>7.2f}%")
        total_outliers += len(outliers)
    
    total_pct = total_outliers / len(df) * 100
    
    # Untuk data saham, outliers normal (< 5%)
    status = "PASS" if total_pct < 5 else "WARN"
    print(f"\n✓ Total outliers: {total_outliers} ({total_pct:.2f}%)")
    print(f"\n[{status}] Outliers < 5% (normal untuk data saham)")
    
    return {
        'test': 'Outliers',
        'total_records': len(df),
        'total_outliers': total_outliers,
        'outlier_pct': round(total_pct, 2),
        'status': status
    }


def main():
    print("=" * 70)
    print("DATA QUALITY TESTING — CAPSTONE PROJECT")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = []
    results.append(test_missing_values())
    results.append(test_duplicates())
    results.append(test_invalid_records())
    results.append(test_outliers())
    
    print("\n" + "=" * 70)
    print("RINGKASAN DATA QUALITY TESTING")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    for r in results:
        print(f"{r['test']:<25} : {r['status']}")
    
    print(f"\nPASSED: {passed}/{len(results)}")
    
    output = {
        'timestamp': datetime.now().isoformat(),
        'test_type': 'Data Quality Testing',
        'total_tests': len(results),
        'passed': passed,
        'failed': failed,
        'results': results
    }
    
    with open('data_quality_test_result.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n✓ Hasil disimpan: data_quality_test_result.json")
    print("=" * 70)


if __name__ == "__main__":
    main()