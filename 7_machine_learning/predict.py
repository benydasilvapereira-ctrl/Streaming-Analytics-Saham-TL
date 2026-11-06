"""
Machine Learning — Prediksi Harga Saham 1 Jam ke Depan
Menggunakan model Linear Regression yang sudah di-train.

Cara menjalankan:
    cd 7_machine_learning
    python predict.py

Output:
    - Tabel stock_predictions di PostgreSQL
"""

import pandas as pd
import numpy as np
import psycopg2
from datetime import datetime, timedelta
import joblib
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)


# ============================================================
# KONFIGURASI
# ============================================================
POSTGRES_HOST = "localhost"
POSTGRES_PORT = 5432
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "6797"
POSTGRES_DB = "stock_db"

SYMBOLS = ['STO.AX', 'WDS.AX', 'FDR.AX', 'ENI.MI', 'ESR.AX']

MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')


# ============================================================
# DATABASE FUNCTIONS
# ============================================================
def get_connection():
    return psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB
    )


def fetch_recent_data(symbol, limit=100):
    """Ambil data terbaru untuk 1 simbol."""
    sql = f"""
        SELECT 
            symbol,
            price,
            volume,
            inserted_at
        FROM stock_prices
        WHERE symbol = '{symbol}'
        ORDER BY inserted_at DESC
        LIMIT {limit};
    """
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    df = df.sort_values('inserted_at').reset_index(drop=True)
    return df


def save_prediction(prediction_data):
    """Simpan hasil prediksi ke tabel stock_predictions."""
    sql = """
        INSERT INTO stock_predictions 
        (symbol, prediction_time, target_time, predicted_price, model_name)
        VALUES (%s, %s, %s, %s, %s);
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql, (
        prediction_data['symbol'],
        prediction_data['prediction_time'],
        prediction_data['target_time'],
        prediction_data['predicted_price'],
        prediction_data['model_name']
    ))
    conn.commit()
    cur.close()
    conn.close()


# ============================================================
# FEATURE ENGINEERING (Sama persis dengan training)
# ============================================================
def create_features(df):
    """Buat fitur untuk prediksi."""
    df = df.copy()
    
    # Moving Average
    df['ma_5'] = df['price'].rolling(window=5).mean()
    df['ma_20'] = df['price'].rolling(window=20).mean()
    
    # Waktu
    df['hour'] = df['inserted_at'].dt.hour
    df['minute'] = df['inserted_at'].dt.minute
    df['day_of_week'] = df['inserted_at'].dt.dayofweek
    
    # Lag
    df['price_lag_1'] = df['price'].shift(1)
    df['price_lag_2'] = df['price'].shift(2)
    df['volume_lag_1'] = df['volume'].shift(1)
    
    # Drop NaN
    df = df.dropna().reset_index(drop=True)
    
    return df


# ============================================================
# PREDICT
# ============================================================
def predict_symbol(symbol):
    """Prediksi harga 1 jam ke depan untuk 1 simbol."""
    print(f"\n{'='*70}")
    print(f"PREDIKSI: {symbol}")
    print(f"{'='*70}")
    
    # 1. Load model
    model_path = os.path.join(MODEL_DIR, f"{symbol.replace('.', '_')}_model.pkl")
    
    if not os.path.exists(model_path):
        print(f"    [SKIP] Model tidak ditemukan: {model_path}")
        return None
    
    model = joblib.load(model_path)
    print(f"[1] Model loaded.")
    
    # 2. Fetch data terbaru
    print(f"[2] Mengambil data terbaru...")
    df = fetch_recent_data(symbol, limit=100)
    
    if len(df) < 30:
        print(f"    [SKIP] Data tidak cukup: {len(df)} records")
        return None
    
    current_price = float(df['price'].iloc[-1])
    print(f"    Harga terakhir: ${current_price:.4f}")
    
    # 3. Feature engineering
    df = create_features(df)
    
    if len(df) < 1:
        print(f"    [SKIP] Data setelah feature engineering kosong")
        return None
    
    # 4. Ambil baris terakhir untuk prediksi
    last_row = df.iloc[-1:].copy()
    
    feature_cols = [
        'price', 'volume', 'ma_5', 'ma_20',
        'hour', 'minute', 'day_of_week',
        'price_lag_1', 'price_lag_2', 'volume_lag_1'
    ]
    
    X = last_row[feature_cols]
    
    # 5. Prediksi
    predicted_price = float(model.predict(X)[0])
    
    # Pastikan harga tidak minus (karena fluktuasi model ekstrem)
    if predicted_price <= 0:
        predicted_price = current_price * 0.99 
    
    change = predicted_price - current_price
    change_pct = (change / current_price) * 100 if current_price > 0 else 0
    
    prediction_time = datetime.now()
    target_time = prediction_time + timedelta(hours=1)
    
    print(f"\n[3] HASIL PREDIKSI:")
    print(f"    Harga sekarang   : ${current_price:.4f}")
    print(f"    Harga prediksi   : ${predicted_price:.4f}")
    print(f"    Perubahan        : {'+' if change >= 0 else ''}{change:.4f} ({'+' if change_pct >= 0 else ''}{change_pct:.2f}%)")
    print(f"    Target waktu     : {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 6. Simpan ke database
    prediction_data = {
        'symbol': symbol,
        'prediction_time': prediction_time,
        'target_time': target_time,
        'predicted_price': round(predicted_price, 4),
        'model_name': 'LinearRegression'
    }
    
    save_prediction(prediction_data)
    print(f"[4] Prediksi disimpan ke database.")
    
    return prediction_data


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("MACHINE LEARNING — PREDIKSI HARGA SAHAM")
    print("Linear Regression — 1 Jam ke Depan")
    print("=" * 70)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Symbols: {SYMBOLS}")
    print("=" * 70)
    
    results = []
    
    for symbol in SYMBOLS:
        try:
            result = predict_symbol(symbol)
            if result:
                results.append(result)
        except Exception as e:
            print(f"\n[ERROR] Gagal prediksi {symbol}: {e}")
            continue
    
    # Summary
    if results:
        print("\n" + "=" * 70)
        print("RINGKASAN PREDIKSI")
        print("=" * 70)
        print(f"{'Symbol':<10} {'Harga Skrg':>12} {'Prediksi':>12} {'Perubahan':>12}")
        print("-" * 70)
        
        for r in results:
            df_current = fetch_recent_data(r['symbol'], limit=1)
            current = df_current['price'].iloc[-1] if len(df_current) > 0 else 0
            change_pct = ((r['predicted_price'] - current) / current * 100) if current > 0 else 0
            
            print(f"{r['symbol']:<10} ${current:>10.4f} ${r['predicted_price']:>10.4f} {'+' if change_pct >= 0 else ''}{change_pct:>10.2f}%")
        
        print("=" * 70)
    
    print("\n[DONE] Prediksi selesai!")
    print("=" * 70)


if __name__ == "__main__":
    main()