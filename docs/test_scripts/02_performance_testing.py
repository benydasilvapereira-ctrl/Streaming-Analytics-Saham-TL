"""
PERFORMANCE TESTING
Mengukur: Latency, Throughput, CPU/Memory
"""

import psycopg2
import pandas as pd
import time
import json
from datetime import datetime
import psutil
import os


POSTGRES = {
    'host': 'localhost', 'port': 5432, 'user': 'postgres',
    'password': '6797', 'dbname': 'stock_db'
}


def get_conn():
    return psycopg2.connect(**POSTGRES)


def test_latency():
    """Test latency end-to-end."""
    print("\n" + "=" * 70)
    print("TEST: LATENCY (End-to-End)")
    print("=" * 70)
    
    conn = get_conn()
    
    # Ambil waktu data terakhir dari PostgreSQL
    df = pd.read_sql("""
        SELECT MAX(inserted_at) as last_data
        FROM stock_prices;
    """, conn)
    conn.close()
    
    last_data = pd.to_datetime(df['last_data'].iloc[0])
    now = datetime.now()
    
    # Karena timestamp tanpa timezone, kita kurangi langsung
    latency_seconds = (now - last_data.replace(tzinfo=None)).total_seconds()
    
    print(f"✓ Waktu sekarang: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✓ Data terakhir:  {last_data.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"✓ Latency: {latency_seconds:.2f} detik")
    
    # Validasi (latency < 30 detik dianggap OK)
    status = "PASS" if latency_seconds < 30 else "FAIL"
    print(f"\n[{status}] Latency < 30 detik")
    
    return {
        'test': 'Latency',
        'latency_seconds': round(latency_seconds, 2),
        'status': status
    }


def test_throughput():
    """Test throughput (records per menit)."""
    print("\n" + "=" * 70)
    print("TEST: THROUGHPUT (Records per Menit)")
    print("=" * 70)
    
    conn = get_conn()
    
    # Cek records 5 menit terakhir
    df = pd.read_sql("""
        SELECT COUNT(*) as count
        FROM stock_prices
        WHERE inserted_at >= NOW() - INTERVAL '5 minutes';
    """, conn)
    records_5min = int(df['count'].iloc[0])
    
    # Cek records 1 jam terakhir
    df2 = pd.read_sql("""
        SELECT COUNT(*) as count
        FROM stock_prices
        WHERE inserted_at >= NOW() - INTERVAL '1 hour';
    """, conn)
    records_1hour = int(df2['count'].iloc[0])
    
    conn.close()
    
    throughput_5min = records_5min / 5 if records_5min > 0 else 0
    throughput_1hour = records_1hour / 60 if records_1hour > 0 else 0
    
    print(f"✓ Records 5 menit terakhir: {records_5min}")
    print(f"✓ Records 1 jam terakhir: {records_1hour}")
    print(f"✓ Throughput (5 min avg): {throughput_5min:.1f} records/menit")
    print(f"✓ Throughput (1 hour avg): {throughput_1hour:.1f} records/menit")
    
    # Target: ~30 records/menit (5 saham × 6 events/menit)
    status = "PASS" if throughput_1hour >= 10 else "FAIL"
    print(f"\n[{status}] Throughput ≥ 10 records/menit")
    
    return {
        'test': 'Throughput',
        'records_5min': records_5min,
        'records_1hour': records_1hour,
        'throughput_5min': round(throughput_5min, 1),
        'throughput_1hour': round(throughput_1hour, 1),
        'status': status
    }


def test_cpu_memory():
    """Test CPU/Memory usage."""
    print("\n" + "=" * 70)
    print("TEST: CPU/MEMORY USAGE")
    print("=" * 70)
    
    # Snapshot CPU & Memory
    cpu_percent = psutil.cpu_percent(interval=2)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    print(f"✓ CPU Usage: {cpu_percent:.1f}%")
    print(f"✓ Memory Usage: {memory.percent:.1f}% ({memory.used / (1024**3):.2f} GB / {memory.total / (1024**3):.2f} GB)")
    print(f"✓ Disk Usage: {disk.percent:.1f}%")
    
    # Cek proses Java (Kafka + Spark)
    java_procs = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info', 'cpu_percent']):
        try:
            if 'java' in proc.info['name'].lower():
                mem_mb = proc.info['memory_info'].rss / (1024 * 1024)
                java_procs.append({
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'memory_mb': round(mem_mb, 1),
                    'cpu': proc.info['cpu_percent']
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    print(f"\n✓ Java Processes ({len(java_procs)}):")
    for p in java_procs:
        print(f"    - PID {p['pid']:6} : {p['memory_mb']:7.1f} MB | CPU: {p['cpu']:.1f}%")
    
    # Validasi
    status = "PASS" if cpu_percent < 80 and memory.percent < 80 else "FAIL"
    print(f"\n[{status}] CPU < 80% dan Memory < 80%")
    
    return {
        'test': 'CPU/Memory',
        'cpu_percent': round(cpu_percent, 1),
        'memory_percent': round(memory.percent, 1),
        'memory_used_gb': round(memory.used / (1024**3), 2),
        'disk_percent': round(disk.percent, 1),
        'java_processes': java_procs,
        'status': status
    }


def main():
    print("=" * 70)
    print("PERFORMANCE TESTING — CAPSTONE PROJECT")
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    results = []
    
    results.append(test_latency())
    results.append(test_throughput())
    results.append(test_cpu_memory())
    
    # Ringkasan
    print("\n" + "=" * 70)
    print("RINGKASAN PERFORMANCE TESTING")
    print("=" * 70)
    
    passed = sum(1 for r in results if r['status'] == 'PASS')
    failed = sum(1 for r in results if r['status'] == 'FAIL')
    
    for r in results:
        print(f"{r['test']:<20} : {r['status']}")
    
    print(f"\nPASSED: {passed}/{len(results)}")
    print(f"FAILED: {failed}/{len(results)}")
    
    # Simpan
    output = {
        'timestamp': datetime.now().isoformat(),
        'test_type': 'Performance Testing',
        'total_tests': len(results),
        'passed': passed,
        'failed': failed,
        'results': results
    }
    
    with open('performance_test_result.json', 'w') as f:
        json.dump(output, f, indent=2, default=str)
    
    print("\n✓ Hasil disimpan: performance_test_result.json")
    print("=" * 70)


if __name__ == "__main__":
    main()