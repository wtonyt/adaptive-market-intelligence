from dotenv import load_dotenv

load_dotenv()

from src.services.alpaca.positions import (
    get_all_positions
)

positions = get_all_positions()

print(positions)