import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORICAL_INDICES_URL = "https://www.nseindia.com/products/dynaContent/equities/indices/historicalindices.jsp"
DATA_DIR = os.path.join(BASE_DIR, 'data/')
