import random
from copy import deepcopy

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from tictactoe.constants import (
    FREE_SPACE,
    DEFAULT_STATE
)


def get_default_state() -> list[list[str]]:
    """
    Returns the default state of the game board.

    Returns
    -------
    list[list[str]]
        A 3x3 matrix of FREE_SPACE.
    """
    return deepcopy(DEFAULT_STATE)


def check_win(board: list[list[str]]) -> str | None:
    """
    Checks if there is a winner on the board.

    Parameters
    ----------
    board : list[list[str]]
        A 3x3 matrix with CROSS / ZERO / FREE_SPACE.

    Returns
    -------
    str or None
        CROSS or ZERO if there's a winner, otherwise None.
    """
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != FREE_SPACE:
            return board[r][0]
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != FREE_SPACE:
            return board[0][c]
    if board[0][0] == board[1][1] == board[2][2] != FREE_SPACE:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != FREE_SPACE:
        return board[0][2]
    return None


def is_draw(board: list[list[str]]) -> bool:
    """
    Checks if the game ends without a winner.

    Parameters
    ----------
    board : list[list[str]]
        A 3x3 matrix with CROSS / ZERO / FREE_SPACE.

    Returns
    -------
    bool
        True if nobody wins and there are no free cells, False otherwise.
    """
    for row in board:
        if FREE_SPACE in row:
            return False
    return True


def find_best_move(board: list[list[str]]) -> tuple[int, int] | None:
    """
    Finds the best move for the AI - just a random free cell.

    Parameters
    ----------
    board : list[list[str]]
        Current 3x3 board.

    Returns
    -------
    tuple[int, int] or None
        (row, col) of the chosen cell or None if no free cells.
    """
    free_cells = [
        (r, c) for r in range(3) for c in range(3)
        if board[r][c] == FREE_SPACE
        ]
    if not free_cells:
        return None
    return random.choice(free_cells)


def generate_keyboard(state: list[list[str]]) -> InlineKeyboardMarkup:
    """
    Generates an inline keyboard for the gameboard.

    Parameters
    ----------
    state : list[list[str]]
        3x3 board.

    Returns
    -------
    InlineKeyboardMarkup
        Inline keyboard with 3 rows of buttons and a stop button.
    """
    keyboard = []
    for row in range(3):
        row_buttons = []
        for col in range(3):
            row_buttons.append(
                InlineKeyboardButton(
                    text=state[row][col],
                    callback_data=f"{row}{col}"
                )
            )
        keyboard.append(row_buttons)

    stop_button = [
        InlineKeyboardButton("Завершить игру", callback_data="stop_game")
    ]
    keyboard.append(stop_button)
    return InlineKeyboardMarkup(keyboard)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Generates a main menu keyboard.

    Returns
    -------
    InlineKeyboardMarkup
        Inline keyboard with mode selection.
    """
    buttons = [
        [
            InlineKeyboardButton("Одиночный режим (🤖)",
                                 callback_data="mode_single"),
            InlineKeyboardButton("Мультиплеер (👥)",
                                 callback_data="mode_multi"),
        ]
    ]
    return InlineKeyboardMarkup(buttons)
