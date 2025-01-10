import logging

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from tictactoe.constants import TOKEN, SELECT_MODE, CONTINUE_GAME, FINISH_GAME
from tictactoe.handlers import (
    start,
    mode_selection,
    join,
    game,
    end,
    help_command
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            SELECT_MODE: [
                CallbackQueryHandler(mode_selection, pattern="^mode_.*$")
            ],
            CONTINUE_GAME: [
                CallbackQueryHandler(game, pattern="^(stop_game|[0-2][0-2])$"),
                CommandHandler("join", join),
            ],
            FINISH_GAME: [
                CallbackQueryHandler(game, pattern="^(stop_game|[0-2][0-2])$")
            ],
        },
        fallbacks=[CommandHandler("end", end)],

        per_chat=True,
        per_user=False
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("end", end))

    logger.info("Bot is running!")
    application.run_polling()


if __name__ == "__main__":
    main()
