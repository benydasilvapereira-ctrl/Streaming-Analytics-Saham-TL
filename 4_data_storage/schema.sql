-- Tabel untuk menyimpan data saham mentah (dari Kafka)
CREATE TABLE IF NOT EXISTS stock_prices (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    name VARCHAR(100),
    exchange VARCHAR(50),
    price NUMERIC(12, 4),
    open NUMERIC(12, 4),
    high NUMERIC(12, 4),
    low NUMERIC(12, 4),
    volume BIGINT,
    event_timestamp BIGINT,
    source VARCHAR(20),
    fetched_at TIMESTAMP,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stock_prices_symbol ON stock_prices(symbol);
CREATE INDEX IF NOT EXISTS idx_stock_prices_event_ts ON stock_prices(event_timestamp);
CREATE INDEX IF NOT EXISTS idx_stock_prices_inserted_at ON stock_prices(inserted_at);

-- Tabel untuk hasil agregasi (trend analytics)
CREATE TABLE IF NOT EXISTS stock_trends (
    id BIGSERIAL PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    avg_price NUMERIC(12, 4),
    max_price NUMERIC(12, 4),
    min_price NUMERIC(12, 4),
    total_volume BIGINT,
    data_points INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_stock_trends_symbol ON stock_trends(symbol);
CREATE INDEX IF NOT EXISTS idx_stock_trends_window ON stock_trends(window_start, window_end);

\echo 'Tabel berhasil dibuat:'
\dt