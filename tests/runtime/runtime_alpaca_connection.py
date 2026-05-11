from dotenv import load_dotenv

load_dotenv()

from src.services.alpaca.client import (
    get_trading_client
)

client = get_trading_client()

account = client.get_account()

print(account)