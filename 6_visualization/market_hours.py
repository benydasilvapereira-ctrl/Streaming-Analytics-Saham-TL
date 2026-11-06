"""
Market Hours Configuration
Menentukan status buka/tutup pasar saham.
"""

from datetime import datetime, time
import pytz

MARKETS = {
    'ASX': {
        'name': 'Australian Securities Exchange',
        'timezone': 'Australia/Sydney',
        'open_time': time(10, 0),
        'close_time': time(16, 0),
        'days': [0, 1, 2, 3, 4],
    },
    'Borsa Italiana': {
        'name': 'Borsa Italiana (Milan)',
        'timezone': 'Europe/Rome',
        'open_time': time(9, 0),
        'close_time': time(17, 30),
        'days': [0, 1, 2, 3, 4],
    },
}


def get_market_status(market_name):
    market = MARKETS.get(market_name)
    if not market:
        return 'UNKNOWN'
    tz = pytz.timezone(market['timezone'])
    now = datetime.now(tz)
    if now.weekday() not in market['days']:
        return 'CLOSED'
    current_time = now.time()
    if market['open_time'] <= current_time <= market['close_time']:
        return 'OPEN'
    return 'CLOSED'


def get_market_info(market_name):
    market = MARKETS.get(market_name)
    if not market:
        return {'status': 'UNKNOWN', 'name': market_name}
    tz = pytz.timezone(market['timezone'])
    now = datetime.now(tz)
    return {
        'status': get_market_status(market_name),
        'name': market['name'],
        'timezone': market['timezone'],
        'local_time': now.strftime('%H:%M %Z'),
        'open': market['open_time'].strftime('%H:%M'),
        'close': market['close_time'].strftime('%H:%M'),
    }