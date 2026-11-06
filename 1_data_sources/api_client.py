import yfinance as yf
import time
from datetime import datetime
from config import TIMOR_LESTE_STOCKS, POLL_INTERVAL_SECONDS


def fetch_stock_price(stock_info):
    """
    Mengambil harga saham terbaru menggunakan yfinance.
    
    Args:
        stock_info (dict): Dictionary berisi 'symbol', 'name', 'exchange'
    
    Returns:
        dict: Data saham dalam format JSON, atau None jika gagal
    """
    symbol = stock_info['symbol']
    
    try:
        ticker = yf.Ticker(symbol)
        # Ambil data 1 hari terakhir (cukup untuk mendapatkan harga terbaru)
        data = ticker.history(period="1d", interval="1m")
        
        if data.empty:
            print(f"[WARN] Tidak ada data untuk {symbol}")
            return None
        
        # Ambil baris terakhir (harga terbaru)
        latest = data.iloc[-1]
        
        return {
            'symbol': symbol,
            'name': stock_info['name'],
            'exchange': stock_info['exchange'],
            'price': round(float(latest['Close']), 4),
            'open': round(float(latest['Open']), 4),
            'high': round(float(latest['High']), 4),
            'low': round(float(latest['Low']), 4),
            'volume': int(latest['Volume']),
            'timestamp': int(time.time() * 1000),
            'source': 'yfinance',
            'fetched_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"[ERROR] Gagal fetch {symbol}: {e}")
        return None


def fetch_all_timor_stocks():
    """Mengambil data semua saham yang relevan dengan Timor-Leste."""
    results = []
    
    for stock_info in TIMOR_LESTE_STOCKS:
        print(f"[INFO] Fetching {stock_info['symbol']} ({stock_info['name']})...")
        stock_data = fetch_stock_price(stock_info)
        
        if stock_data:
            results.append(stock_data)
            print(f"[OK] {stock_data['symbol']:10} = ${stock_data['price']:.2f} "
                  f"(Vol: {stock_data['volume']:,})")
        else:
            print(f"[FAIL] Gagal fetch {stock_info['symbol']}")
        
        # Jeda antar request untuk menghindari rate limit Yahoo Finance
        time.sleep(2)
    
    return results


if __name__ == '__main__':
    print("=" * 70)
    print("TEST YFINANCE CLIENT - Stock Timor-Leste")
    print("=" * 70)
    print(f"[INFO] Jumlah saham: {len(TIMOR_LESTE_STOCKS)}")
    print()
    
    stocks = fetch_all_timor_stocks()
    
    print("=" * 70)
    print(f"Total saham berhasil di-fetch: {len(stocks)}")
    print("-" * 70)
    print(f"{'Symbol':<10} | {'Name':<20} | {'Price':>8} | {'Volume':>12}")
    print("-" * 70)
    for s in stocks:
        print(f"{s['symbol']:<10} | {s['name']:<20} | ${s['price']:>7.2f} | {s['volume']:>12,}")
    print("=" * 70)