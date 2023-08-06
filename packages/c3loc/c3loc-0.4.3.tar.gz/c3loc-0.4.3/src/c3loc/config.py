import os
from uuid import UUID

CONFIG = {
    'DB_NAME': os.getenv('DB_NAME', ''),
    'DB_USER': os.getenv('DB_USER', 'c3loc'),
    'DB_PASSWORD': os.getenv('DB_PASSWORD', 'c3letmein'),
    'DB_HOST': os.getenv('DB_HOST', ''),
    'LA_UUID': os.getenv('LA_UUID', UUID(bytes=b'c3wirelesslocanc')),
    'API_RESULT_LIMIT': int(os.getenv('API_RESULT_LIMIT', 100)),
    'LOCATION_UPDATE_MS': 1000,
    'MAX_FRAME_SIZE': 512,
}
