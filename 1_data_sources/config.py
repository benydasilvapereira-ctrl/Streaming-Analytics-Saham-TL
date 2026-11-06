import os
from dotenv import load_dotenv

# Load environment variables dari file .env
load_dotenv()

# FCS API Configuration
FCS_API_KEY = os.getenv('FCS_API_KEY')
FCS_API_BASE = 'https://api-v4.fcsapi.com'
FCS_STOCK_ENDPOINT = f'{FCS_API_BASE}/stock/list'

# Kafka Configuration
KAFKA_BROKER = os.getenv('KAFKA_BROKER', 'localhost:9093')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'stock-prices-tl')

# Saham yang relevan dengan Timor-Leste (format Yahoo Finance)
# STO.AX = Santos Ltd (operator Bayu-Undan)
# WDS.AX = Woodside Energy (operator Greater Sunrise)
# FDR.AX = Finder Energy (proyek KTJ)
# ENI.MI = Eni S.p.A. (PSC TL-SO-22-23 / Block P, partner TIMOR GAP)
# ESR.AX = Estrella Resources (proyek mangan & batu gamping di TL)
TIMOR_LESTE_STOCKS = [
    {'symbol': 'STO.AX', 'name': 'Santos Ltd', 'exchange': 'ASX'},
    {'symbol': 'WDS.AX', 'name': 'Woodside Energy', 'exchange': 'ASX'},
    {'symbol': 'FDR.AX', 'name': 'Finder Energy', 'exchange': 'ASX'},
    {'symbol': 'ENI.MI', 'name': 'Eni S.p.A.', 'exchange': 'Borsa Italiana'},
    {'symbol': 'ESR.AX', 'name': 'Estrella Resources', 'exchange': 'ASX'},
]

# Interval polling (detik) — Free tier: maksimal 10 request/menit
POLL_INTERVAL_SECONDS = 10