import os

os.environ["TOKEN"] = "ВАШ_ТОКЕН"
TOKEN = os.getenv("TOKEN", "")

SELECT_MODE, CONTINUE_GAME, FINISH_GAME = range(3)

FREE_SPACE = "⬜️"
CROSS = "❌"
ZERO = "⭕️"

DEFAULT_STATE = [[FREE_SPACE for _ in range(3)] for _ in range(3)]
