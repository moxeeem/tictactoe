import logging

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

from tictactoe.constants import (
    FREE_SPACE,
    SELECT_MODE,
    CONTINUE_GAME,
    FINISH_GAME,
    CROSS,
    ZERO
)

from tictactoe.game_logic import (
    get_default_state,
    check_win,
    is_draw,
    find_best_move,
    main_menu_keyboard,
    generate_keyboard
)

logger = logging.getLogger(__name__)


async def start(update: Update,
                context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /start handler - start conversation, show mode menu.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.

    Returns
    -------
    int
        The next state (SELECT_MODE).
    """
    try:
        user_info = f"user={update.effective_user.id}"
        chat_info = f"chat_id={update.effective_chat.id}"
        logger.info(f"/start from {user_info}, {chat_info}")

        if update.message is not None:
            await update.message.reply_text(
                "Привет! Выберите режим игры:",
                reply_markup=main_menu_keyboard()
            )
        return SELECT_MODE
    except Exception as exc:
        logger.warning(f"Ошибка в start(): {exc}")
        if update.message:
            await update.message.reply_text("Ошибка при обработке /start.")
        return ConversationHandler.END


async def mode_selection(update: Update,
                         context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    CallbackQuery for choosing the mode: single or multi.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.

    Returns
    -------
    int
        The next state (CONTINUE_GAME).
    """
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    try:
        chosen_mode = query.data
        chat_id = query.message.chat_id
        logger.info(f"mode_selection: chosen={chosen_mode}, chat_id={chat_id}")

        if chosen_mode == "mode_multi":
            chat_type = update.effective_chat.type
            if chat_type not in (ChatType.GROUP, ChatType.SUPERGROUP):
                await query.message.reply_text(
                    "Мультиплеер невозможен в личном чате или канале!\n"
                    "Добавьте бота в группу, чтобы играть вдвоём."
                )
                return ConversationHandler.END

        if "games" not in context.chat_data:
            context.chat_data["games"] = {}

        context.chat_data["games"][chat_id] = {
            "board": get_default_state(),
            "current_player": CROSS,
            "players": [],
            "mode": None
        }
        game_data = context.chat_data["games"][chat_id]

        user_id = query.from_user.id
        user_name = (query.from_user.username
                     or query.from_user.full_name
                     or "Player1")

        if chosen_mode == "mode_single":
            game_data["mode"] = "single"
            game_data["players"] = [{"id": user_id, "name": user_name}]

            text_single = (
                f"Вы выбрали одиночный режим.\n"
                f"Игрок: @{user_name} (❌) против ИИ (⭕️).\n"
                "Игра начинается!"
            )

            logger.info(f"Single mode started by {user_id} in chat={chat_id}")
            await query.message.edit_text(text_single)

            board = game_data["board"]
            markup = generate_keyboard(board)
            msg = f"Ходит {game_data['current_player']} (вы, @{user_name})."
            await query.message.reply_text(msg, reply_markup=markup)
            return CONTINUE_GAME

        if chosen_mode == "mode_multi":
            game_data["mode"] = "multi"
            game_data["players"].append({"id": user_id, "name": user_name})

            text_multi = (
                f"Вы выбрали мультиплеерный режим.\n"
                f"Первый игрок: @{user_name}.\n\n"
                "Попросите второго игрока в этом же групповом чате "
                "ввести команду /join, чтобы присоединиться к партии.\n\n"
            )
            logger.info(f"Multiplayer started by {user_id} in chat={chat_id}")
            await query.message.edit_text(text_multi)
            return CONTINUE_GAME

        return ConversationHandler.END

    except Exception as exc:
        logger.warning(f"Ошибка в mode_selection(): {exc}")
        await query.message.reply_text("Произошла ошибка при выборе режима.")
        return ConversationHandler.END


async def join(update: Update,
               context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /join handler - second player wants to join the multiplayer game.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.

    Returns
    -------
    int
        The next state (CONTINUE_GAME).
    """
    try:
        chat_id = update.effective_chat.id
        logger.info(f"/join from {update.effective_user.id} in chat={chat_id}")

        games = context.chat_data.get("games", {})
        if chat_id not in games:
            await update.message.reply_text(
                "Нет активной игры. Сначала используйте /start (мультиплеер)."
            )
            return ConversationHandler.END

        game_data = games[chat_id]
        if game_data["mode"] != "multi":
            warn_text = "Сейчас нет активной игры (или режим не мультиплеер)."
            await update.message.reply_text(warn_text)
            return ConversationHandler.END

        if len(game_data["players"]) >= 2:
            await update.message.reply_text("В игре уже есть два игрока.")
            return FINISH_GAME

        user_id = update.effective_user.id
        user_name = (update.effective_user.username
                     or update.effective_user.full_name
                     or "Player2")

        if len(game_data["players"]) == 1:
            first_player_id = game_data["players"][0]["id"]
            if user_id == first_player_id:
                await update.message.reply_text(
                    "Нельзя присоединиться к мультиплееру с тем же аккаунтом!"
                )
                return ConversationHandler.END

        game_data["players"].append({"id": user_id, "name": user_name})
        logger.info(f"Second player joined: user={user_id}, chat_id={chat_id}")

        await update.message.reply_text(
            f"Вы (@{user_name}) присоединились к игре!\n"
            f"Игрок 1: @{game_data['players'][0]['name']}\n"
            f"Игрок 2: @{user_name}\n\n"
            "Игра начинается!"
        )

        board = game_data["board"]
        markup = generate_keyboard(board)
        msg = (
            f"Ходит {game_data['current_player']} "
            f"(игрок 1: @{game_data['players'][0]['name']})."
        )
        await update.message.reply_text(msg, reply_markup=markup)
        return CONTINUE_GAME

    except Exception as exc:
        logger.warning(f"Ошибка в join(): {exc}")
        await update.message.reply_text("Произошла ошибка при /join.")
        return ConversationHandler.END


async def game(update: Update,
               context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    CallbackQuery handler for game moves (clicks on the board).

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.

    Returns
    -------
    int
        The next state (CONTINUE_GAME or FINISH_GAME).
    """
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    try:
        chat_id = query.message.chat_id
        games = context.chat_data.get("games", {})
        game_data = games.get(chat_id)

        if not game_data:
            await query.message.reply_text("Нет игры. Используйте /start.")
            return ConversationHandler.END

        board = game_data["board"]
        current_player = game_data["current_player"]
        players = game_data["players"]
        mode = game_data["mode"]

        data = query.data
        if data == "stop_game":
            logger.info(f"stop_game pressed in chat_id={chat_id}")
            del games[chat_id]
            await query.message.edit_text("Игра завершена. Введите /start.")
            return ConversationHandler.END

        row, col = int(data[0]), int(data[1])
        if board[row][col] != FREE_SPACE:
            await query.message.reply_text("Клетка занята. Выберите другую.")
            return ConversationHandler.END

        if mode == "multi" and len(players) == 2:
            user_id = query.from_user.id
            cross_player_id = players[0]["id"]
            zero_player_id = players[1]["id"]

            if current_player == CROSS and user_id != cross_player_id:
                await query.message.reply_text(
                    "Сейчас ходит ❌ (игрок 1). Дождитесь своей очереди."
                )
                return ConversationHandler.END
            if current_player == ZERO and user_id != zero_player_id:
                await query.message.reply_text(
                    "Сейчас ходит ⭕️ (игрок 2). Дождитесь своей очереди."
                )
                return ConversationHandler.END

        board[row][col] = current_player
        winner = check_win(board)
        if winner:
            logger.info(f"Game over: winner={winner} in chat_id={chat_id}")
            markup = generate_keyboard(board)

            if mode == "multi":
                if winner == CROSS:
                    winner_name = "@" + players[0]["name"]
                else:
                    winner_name = "@" + players[1]["name"]
            else:
                if winner == CROSS:
                    winner_name = f"игрок @{players[0]['name']}"
                else:
                    winner_name = "ИИ"

            await query.message.edit_text(
                text=f"Победил {winner} ({winner_name}). Игра окончена.",
                reply_markup=markup
            )
            return FINISH_GAME

        if is_draw(board):
            logger.info(f"Game over: draw in chat_id={chat_id}")
            markup = generate_keyboard(board)
            await query.message.edit_text(
                text="Ничья! Игра окончена.",
                reply_markup=markup
            )
            return FINISH_GAME

        next_player = ZERO if current_player == CROSS else CROSS
        game_data["current_player"] = next_player

        if mode == "multi" and len(players) == 2:
            markup = generate_keyboard(board)
            if next_player == CROSS:
                name = "@" + players[0]["name"]
            else:
                name = "@" + players[1]["name"]

            await query.message.edit_text(
                text=f"Сейчас ходит {next_player} ({name}).",
                reply_markup=markup
            )
            return CONTINUE_GAME

        ai_symbol = next_player
        human_symbol = CROSS if ai_symbol == ZERO else ZERO

        best_move = find_best_move(board)
        if best_move is not None:
            r_ai, c_ai = best_move
            board[r_ai][c_ai] = ai_symbol

        new_winner = check_win(board)
        if new_winner:
            log = f"Game over: winner={new_winner} in chat_id={chat_id}"
            logger.info(log)
            markup = generate_keyboard(board)
            if new_winner == CROSS:
                winner_name = f"игрок @{players[0]['name']}"
            else:
                winner_name = "ИИ"

            await query.message.edit_text(
                text=f"Победил {new_winner} ({winner_name}). Игра окончена.",
                reply_markup=markup
            )
            return FINISH_GAME

        if is_draw(board):
            logger.info(f"Single game draw in chat_id={chat_id}")
            markup = generate_keyboard(board)
            await query.message.edit_text(
                text="Ничья! Игра окончена.",
                reply_markup=markup
            )
            return FINISH_GAME

        game_data["current_player"] = human_symbol
        markup = generate_keyboard(board)
        await query.message.edit_text(
            text=f"Ваш ход ({human_symbol}), @{players[0]['name']}.",
            reply_markup=markup
        )
        return CONTINUE_GAME

    except Exception as exc:
        logger.warning(f"Ошибка в game(): {exc}")
        await query.message.reply_text("Произошла ошибка в ходе игры.")
        return ConversationHandler.END


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """
    /end handler - forcibly ends the current game.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.

    Returns
    -------
    int
        The next state (ConversationHandler.END).
    """
    try:
        chat_id = update.effective_chat.id
        games = context.chat_data.get("games", {})
        if chat_id in games:
            del games[chat_id]

        if update.message:
            await update.message.reply_text("Игра сброшена. Введите /start.")
        return ConversationHandler.END
    except Exception as exc:
        logger.warning(f"Ошибка в end(): {exc}")
        return ConversationHandler.END


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    /help handler - shows a help message.

    Parameters
    ----------
    update : Update
        The incoming update.
    context : CallbackContext
        The context object.
    Returns
    -------
    None
    """
    text = (
        "Список команд:\n\n"
        "/start — начать игру (выбрать режим).\n"
        "/join — присоединиться к мультиплеерной игре (в группе).\n"
        "/help — показать справку.\n"
        "/end — принудительно завершить игру.\n"
    )
    if update.message:
        await update.message.reply_text(text)
