from google import genai 
from google.genai import types
import os
import alpaca_trade_api as tradeapi
from config import *


client = genai.Client()

model_name = "gemini-2.5-flash"

chat = client.chats.create(model=model_name)
"""
while True:
    message = input(">>> ")
    if message.lower() == "exit":
        break
    response = chat.send_message(message)
    print(f"--- {response.text}")
"""
api = tradeapi.REST(key, secret_key, base_url, api_version="v2")

def fetch_portfolio():
    positions = api.list_positions()
    portfolio = []
    for pos in positions:
        portfolio.append({
            "symbol": pos.symbol,
            "qty": pos.qty,
            "avg_entry_price": pos.avg_entry_price,
            "current_price": pos.current_price,
            "unrealized_pl": pos.unrealized_pl
        })
    return portfolio

def fetch_open_orders():
    orders = api.list_orders(status='open')
    open_orders = []
    for order in orders:
        open_orders.append({
            "symbol": order.symbol,
            "qty": order.qty,
            "limit_price": order.limit_price,
            "side": order.side,
            "status": order.status
        })
    return open_orders



def analyze_message(message):
    portfolio_data = fetch_portfolio()
    open_orders = fetch_open_orders()

    pre_prompt = f"""
You are a portfolio manager. Here is the user's portfolio data: {portfolio_data}
Here are the user's open orders: {open_orders}
Give short answers about the portfolio and orders based on the user's questions.

    """
    response = chat.send_message(pre_prompt + message)
    return response.text