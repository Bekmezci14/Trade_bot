
from config import *
import alpaca_trade_api as tradeapi


api = tradeapi.REST(key, secret_key, base_url, api_version="v2")

def get_data(symbol):
    try:
        barset = api.get_latest_trade(symbol)
        return {"price": barset.price}
    except Exception as e:
        return {"price": -1}
    
print(get_data("AAPL")) 


#print(api.get_trades(["AAPL", "GOOGL", "MSFT"]))