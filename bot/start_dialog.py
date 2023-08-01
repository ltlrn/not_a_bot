import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from dotenv import load_dotenv
from os import getenv

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


TOKEN = getenv("TEST_BOT_TOKEN")

MODE_CHOICE = 0
ATTRIBUTES_CHOICE = 1
NAME_CHOICE = 2
CLASS_CHOICE = 3

ADD_USER = 4
START_AGAIN = 5
SHOWING = 6
STOPPING = 7

M = 9
F = 10

END = 8


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        "Здесь будет предложение выбрать регистрацию "
        "или продолжать инкогнито"
    )

    buttons = [
        [
            InlineKeyboardButton(text="Знакомство", callback_data=str(ADD_USER)),
            InlineKeyboardButton(text="Заниматься инкогнито", callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_AGAIN):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        text = "Здесь пространное приветственное сообщение"
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_AGAIN] = False

    return MODE_CHOICE


async def reg_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(text="сударь", callback_data=str(M)),
            InlineKeyboardButton(text="сударыня", callback_data=str(F)),
        ],
        [
            InlineKeyboardButton(text="Оставим это", callback_data=str(MODE_CHOICE)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('Выберем пол', reply_markup=keyboard)

    return ATTRIBUTES_CHOICE


async def reg_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(text="сударь", callback_data=str(M)),
            InlineKeyboardButton(text="сударыня", callback_data=str(F)),
        ],
        [
            InlineKeyboardButton(text="Оставим это", callback_data=str(MODE_CHOICE)),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('Выберем пол', reply_markup=keyboard)

    return ATTRIBUTES_CHOICE


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text="Итакъ...")

    return ConversationHandler.END


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data[FEATURES][user_data[CURRENT_FEATURE]] = update.message.text

    user_data[START_OVER] = True

    return await select_feature(update, context)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Set up top level ConversationHandler (selecting action)
    # Because the states of the third level conversation map to the ones of the second level
    # conversation, we need to make sure the top level conversation can also handle them
    registration_handlers = [
     
    ]

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MODE_CHOICE: [
                CallbackQueryHandler(reg_start, pattern="^" + str(ADD_USER) + "$"),
                CallbackQueryHandler(stop, pattern="^" + str(END) + "$")
            ],
            ATTRIBUTES_CHOICE: [
                # CallbackQueryHandler(reg_start, pattern="^" + str(M) + "$"),
                # CallbackQueryHandler(stop, pattern="^" + str(END) + "$")
            ],

            STOPPING: [
                CommandHandler("start", start),
                CallbackQueryHandler(stop, pattern="^" + str(END) + "$")
            ],
        },
        fallbacks=[
            CommandHandler("stop", stop),
        ],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()