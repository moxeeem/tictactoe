import pytest

from app.tictactoe.constants import (
    FREE_SPACE,
    CROSS,
    ZERO
)

from app.tictactoe.game_logic import (
    get_default_state,
    check_win,
    is_draw,
    find_best_move
)


def test_get_default_state():
    """
    Test that get_default_state() returns a 3x3 matrix filled with FREE_SPACE.
    """
    board = get_default_state()
    assert len(board) == 3
    assert all(len(row) == 3 for row in board)
    for row in board:
        for cell in row:
            assert cell == FREE_SPACE


@pytest.mark.parametrize("board,expected_winner", [
    ([[CROSS, CROSS, CROSS],
      [FREE_SPACE, FREE_SPACE, FREE_SPACE],
      [FREE_SPACE, FREE_SPACE, FREE_SPACE]], CROSS),
    ([[ZERO, ZERO, ZERO],
      [FREE_SPACE, FREE_SPACE, FREE_SPACE],
      [FREE_SPACE, FREE_SPACE, FREE_SPACE]], ZERO),
    ([[ZERO, FREE_SPACE, FREE_SPACE],
      [ZERO, FREE_SPACE, FREE_SPACE],
      [ZERO, FREE_SPACE, FREE_SPACE]], ZERO),
    ([[CROSS, FREE_SPACE, FREE_SPACE],
      [CROSS, FREE_SPACE, FREE_SPACE],
      [CROSS, FREE_SPACE, FREE_SPACE]], CROSS),
    ([[CROSS, FREE_SPACE, FREE_SPACE],
      [FREE_SPACE, CROSS, FREE_SPACE],
      [FREE_SPACE, FREE_SPACE, CROSS]], CROSS),
    ([[ZERO, FREE_SPACE, FREE_SPACE],
      [FREE_SPACE, ZERO, FREE_SPACE],
      [FREE_SPACE, FREE_SPACE, ZERO]], ZERO),
    ([[FREE_SPACE, FREE_SPACE, ZERO],
      [FREE_SPACE, ZERO, FREE_SPACE],
      [ZERO, FREE_SPACE, FREE_SPACE]], ZERO),
    ([[FREE_SPACE, FREE_SPACE, CROSS],
      [FREE_SPACE, CROSS, FREE_SPACE],
      [CROSS, FREE_SPACE, FREE_SPACE]], CROSS),
])
def test_check_win(board, expected_winner):
    """
    Test that check_win() identifies the winner (CROSS or ZERO).
    """
    assert check_win(board) == expected_winner


def test_check_win_no_winner():
    """
    Test that check_win() returns None if there is no winner yet.
    """
    board = [
        [CROSS, ZERO, CROSS],
        [ZERO, CROSS, ZERO],
        [ZERO, CROSS, FREE_SPACE],
    ]
    assert check_win(board) is None


@pytest.mark.parametrize("board,expected_draw", [
    ([[CROSS, ZERO, CROSS],
      [ZERO, ZERO, CROSS],
      [CROSS, CROSS, ZERO]], True),
    ([[CROSS, ZERO, FREE_SPACE],
      [ZERO, CROSS, ZERO],
      [CROSS, CROSS, ZERO]], False),
])
def test_is_draw(board, expected_draw):
    """
    Test that is_draw() returns True for a filled board with no winner,
    otherwise False.
    """
    assert is_draw(board) == expected_draw


def test_find_best_move_no_free_cells():
    """
    Test that find_best_move() returns None if there are no free cells.
    """
    board = [
        [CROSS, ZERO, CROSS],
        [ZERO, ZERO, CROSS],
        [CROSS, CROSS, ZERO]
    ]
    assert find_best_move(board) is None


def test_find_best_move_has_free_cells():
    """
    Test that find_best_move() returns a valid (row, col) for free cells.
    """
    board = [
        [CROSS, ZERO, CROSS],
        [ZERO, FREE_SPACE, CROSS],
        [CROSS, CROSS, ZERO]
    ]
    move = find_best_move(board)
    assert move is not None
    row, col = move
    assert 0 <= row < 3
    assert 0 <= col < 3
    assert board[row][col] == FREE_SPACE
