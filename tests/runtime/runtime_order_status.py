from dotenv import load_dotenv

load_dotenv()

from src.services.alpaca.order_status import (
    get_order
)

order_id = "becdb223-f936-485a-9575-bfaab3312e42"

order = get_order(order_id)

print(order)