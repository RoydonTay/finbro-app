import finnhub

from dotenv import load_dotenv
import os

load_dotenv()

# Setup client
finnhub_client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))

# Stock candles
res = finnhub_client.stock_candles('AAPL', 'D', 1590988249, 1591852249)
print(res)