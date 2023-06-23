import logging
from os import getenv

from test_util import GREETINGS

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler, 
    ContextTypes,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters
)
from urllib3.util.retry import Retry

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)
load_dotenv()

TOKEN = getenv("TEST_BOT_TOKEN")
CAT = getenv("CAT_URL")
DOG = getenv("DOG_URL")


def get_a_pet(api: str) -> str:
    response = requests.get(api).json()[0]
    url = response.get("url")

    return url


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Get user that sent /start and log his name

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    chat = update.effective_chat
    name = update.message.chat.first_name

    buttons = ReplyKeyboardMarkup(
        [
            ['/task', '/cat', '/dog'],
        ],
        resize_keyboard=True
    )

    await context.bot.send_message(
        chat_id=chat.id,
        text=GREETINGS[0] % name,
        reply_markup=buttons,
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"id: {update.effective_chat.id}, text: {update.message.text}",
    )


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить задачу из api."""
    url = "http://195.2.93.26/api/tasks/1/"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url).json()
    question = response.get("question")
    answer = response.get("answer")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=question)

    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text("Start handler, Choose a route", reply_markup=reply_markup)
    # Tell ConversationHandler that we're in state `FIRST` now
    return START_ROUTES


async def catificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция - котификатор."""
    url = get_a_pet(CAT)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


async def dogificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Собакирование."""
    url = get_a_pet(DOG)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


# ------------------------------------------------------------------------------

async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update

    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.

    await query.edit_message_text(text="Start handler, Choose a route", reply_markup=reply_markup)

    return START_ROUTES


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="First CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES

async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Second CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES

async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    """Show new choice of buttons. This is the end point of the conversation."""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("LETS DO IT AGAIN", callback_data=str(ONE)),
            InlineKeyboardButton("I WANNA STOP RIGHT NOW", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Third CallbackQueryHandler. Do want to start over?", reply_markup=reply_markup
    )
    # Transfer to conversation state `SECOND`

    return END_ROUTES

async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Fourth CallbackQueryHandler, Choose a route", reply_markup=reply_markup
    )
    return START_ROUTES

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text="See you next time!")

    return ConversationHandler.END


if __name__ == "__main__":
    # Instead of running single handlers in a non-blocking way, we can tell
    # the Application to run the whole call of Application.process_update concurrently:
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler("start", start)
    cat_handler = CommandHandler("cat", catificate)
    dog_handler = CommandHandler("dog", dogificate)

    task_handler = CommandHandler("task", task)

    # Stages
    START_ROUTES, END_ROUTES = range(2)
    # Callback data
    ONE, TWO, THREE, FOUR = range(4)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("task", task)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
            ],

            END_ROUTES: [
                CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
            ],
        },
        fallbacks=[CommandHandler("task", task)],
    )

    # echo of non-empty, non-command messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # may be "add_handlerS" instead?

    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(cat_handler)
    app.add_handler(dog_handler)

    app.add_handler(conv_handler)

    app.run_polling()
