"""
Machine Learning — Linear Regression untuk Prediksi Harga Saham
Training model dari data historis di PostgreSQL.

Cara menjalankan:
    cd 7_machine_learning
    python train_model.py

Output:
    - models/[SYMBOL]_model.pkl (model Linear Regression)
    - Print metrics (MAE, RMSE, R², MAPE)
"""

import pandas as pd
import numpy as np
import psycopg2
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from datetime import datetime
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

# Symbol yang akan di-train
SYMBOLS_TO_TRAIN = ['STO.AX', 'WDS.AX', 'FDR.AX', 'ENI.MI', 'ESR.AX']

# Path model
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODEL_DIR, exist_ok=True)


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


def fetch_data(symbol):
    """
    Ambil data historis untuk 1 simbol.
    Mengambil 10.000 data terbaru agar model belajar dari data yang lebih 'hidup' (tidak flat).
    """
    sql = f"""
        SELECT 
            symbol,
            price,
            volume,
            inserted_at
        FROM stock_prices
        WHERE symbol = '{symbol}'
        ORDER BY inserted_at DESC
        LIMIT 10000;
    """
    conn = get_connection()
    df = pd.read_sql(sql, conn)
    conn.close()
    
    # Urutkan kembali dari lama ke baru (krusial untuk time-series)
    df = df.sort_values('inserted_at').reset_index(drop=True)
    return df


# ============================================================
# FEATURE ENGINEERING
# ============================================================
def create_features(df):
    """Buat fitur untuk ML dari data mentah."""
    df = df.copy()
    
    # Fitur 1: Moving Average
    df['ma_5'] = df['price'].rolling(window=5).mean()
    df['ma_20'] = df['price'].rolling(window=20).mean()
    
    # Fitur 2: Waktu
    df['hour'] = df['inserted_at'].dt.hour
    df['minute'] = df['inserted_at'].dt.minute
    df['day_of_week'] = df['inserted_at'].dt.dayofweek
    
    # Fitur 3: Lag (harga sebelumnya)
    df['price_lag_1'] = df['price'].shift(1)
    df['price_lag_2'] = df['price'].shift(2)
    
    # Fitur 4: Volume lag
    df['volume_lag_1'] = df['volume'].shift(1)
    
    # Target: Harga 1 jam ke depan
    # Karena data masuk tiap 10 detik, 1 jam = 3600 detik = 360 baris.
    df['target'] = df['price'].shift(-360)
    
    # Drop NaN (dari rolling & shift)
    df = df.dropna().reset_index(drop=True)
    
    return df


# ============================================================
# TRAINING
# ============================================================
def train_symbol(symbol):
    """Train Linear Regression untuk 1 simbol."""
    print(f"\n{'='*70}")
    print(f"TRAINING MODEL: {symbol}")
    print(f"{'='*70}")
    
    # 1. Fetch data
    print(f"[1] Mengambil data dari PostgreSQL...")
    df = fetch_data(symbol)
    print(f"    Total data diambil: {len(df):,} records")
    
    if len(df) < 500:
        print(f"    [SKIP] Data tidak cukup (butuh minimal 500 records)")
        return None
    
    # 2. Feature engineering
    print(f"[2] Membuat fitur...")
    df = create_features(df)
    print(f"    Setelah feature engineering & drop NaN: {len(df):,} records")
    
    if len(df) < 100:
        print(f"    [SKIP] Data setelah cleaning tidak cukup untuk dilatih")
        return None
    
    # 3. Tentukan fitur (X) dan target (y)
    feature_cols = [
        'price', 'volume', 'ma_5', 'ma_20',
        'hour', 'minute', 'day_of_week',
        'price_lag_1', 'price_lag_2', 'volume_lag_1'
    ]
    
    X = df[feature_cols]
    y = df['target']
    
    # 4. Split data: 80% train, 20% test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )
    
    print(f"[3] Split data:")
    print(f"    Training: {len(X_train):,} records")
    print(f"    Testing:  {len(X_test):,} records")
    
    # 5. Train Linear Regression
    print(f"[4] Training Linear Regression...")
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # 6. Evaluasi
    print(f"[5] Evaluasi model...")
    y_pred_test = model.predict(X_test)
    
    # Metrics
    mae = mean_absolute_error(y_test, y_pred_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    r2 = r2_score(y_test, y_pred_test)
    
    # MAPE (hindari pembagian dengan nol)
    y_test_safe = np.where(y_test == 0, 0.0001, y_test)
    mape = np.mean(np.abs((y_test - y_pred_test) / y_test_safe)) * 100
    
    print(f"\n    {'='*50}")
    print(f"    METRICS — {symbol}")
    print(f"    {'='*50}")
    print(f"    MAE  (Mean Absolute Error)      : ${mae:.4f}")
    print(f"    RMSE (Root Mean Squared Error)  : ${rmse:.4f}")
    print(f"    R²   (R-squared)                : {r2:.4f}")
    print(f"    MAPE (Mean Absolute Pct Error)  : {mape:.2f}%")
    print(f"    {'='*50}")
    
    # Interpretasi R²
    if r2 > 0.9:
        quality = "SANGAT BAIK ⭐⭐⭐⭐⭐"
    elif r2 > 0.7:
        quality = "BAIK ⭐⭐⭐⭐"
    elif r2 > 0.5:
        quality = "CUKUP ⭐⭐⭐"
    elif r2 > 0.3:
        quality = "LEMAH ⭐⭐"
    else:
        quality = "SANGAT LEMAH (Data terlalu flat / Pasar Tutup) ⭐"
    
    print(f"    Kualitas Model: {quality}")
    
    # 7. Simpan model
    model_path = os.path.join(MODEL_DIR, f"{symbol.replace('.', '_')}_model.pkl")
    joblib.dump(model, model_path)
    print(f"\n[6] Model disimpan: {model_path}")
    
    return {
        'symbol': symbol,
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'mape': mape,
        'n_train': len(X_train),
        'n_test': len(X_test),
    }


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 70)
    print("MACHINE LEARNING — LINEAR REGRESSION")
    print("Prediksi Harga Saham Real-Time")
    print("=" * 70)
    print(f"Waktu: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Symbols: {SYMBOLS_TO_TRAIN}")
    print("=" * 70)
    
    results = []
    
    for symbol in SYMBOLS_TO_TRAIN:
        try:
            result = train_symbol(symbol)
            if result:
                results.append(result)
        except Exception as e:
            print(f"\n[ERROR] Gagal train {symbol}: {e}")
            continue
    
    # Summary
    if results:
        print("\n" + "=" * 70)
        print("RINGKASAN HASIL TRAINING")
        print("=" * 70)
        print(f"{'Symbol':<10} {'MAE':>8} {'RMSE':>8} {'R²':>8} {'MAPE':>8}")
        print("-" * 70)
        for r in results:
            print(f"{r['symbol']:<10} ${r['mae']:>6.4f} ${r['rmse']:>6.4f} {r['r2']:>7.4f} {r['mape']:>6.2f}%")
        print("=" * 70)
        
        # Best model
        best = max(results, key=lambda x: x['r2'])
        print(f"\n🏆 Model TERBAIK: {best['symbol']} (R² = {best['r2']:.4f})")
        print("=" * 70)
    
    print("\n[DONE] Training selesai! Silakan jalankan predict.py")
    print("=" * 70)


if __name__ == "__main__":
    main()