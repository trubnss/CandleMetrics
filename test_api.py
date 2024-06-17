import json

import requests

url = "http://127.0.0.1:8000/candles"

params = {
    "symbol": "ETHUSDT",
    "timeframe": "1d",
    "indicator": "EMA",
    "period": "3",
    "candle_number": "50",
}

response = requests.get(url, params=params)

print(response.status_code)
if response.status_code == 200:
    formatted_json = json.dumps(response.json(), indent=4)
    print(formatted_json)
else:
    print(response.text)
