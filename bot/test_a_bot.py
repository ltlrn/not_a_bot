import logging
from os import getenv

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, Update, MenuButton, MenuButtonCommands)

from telegram.ext import (ApplicationBuilder, CallbackQueryHandler,
                          CommandHandler, ContextTypes, ConversationHandler,
                          MessageHandler, filters)
from urllib3.util.retry import Retry

from callbacks import (END_ROUTES, FOUR, FIVE, SIX, ONE, START_ROUTES, THREE, TWO,
                       four, one, back, apply, three, two)
from test_util import GREETINGS

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
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
    # await context.bot.set_chat_menu_button(MenuButtonCommands)

    user = update.message.from_user
    logger.info("User %s started the conversation.", user.first_name)

    chat = update.effective_chat
    name = update.message.chat.first_name

    buttons = ReplyKeyboardMarkup(
        [
            ["/task", "/cat", "/dog"],
        ],
        resize_keyboard=True,
    )

    menu_button_1 = MenuButton(str)

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
    url = "http://195.2.93.26/api/tasks/2/"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url).json()
    question = response.get("question")
    answer = response.get("answer")

    context.user_data['answer'] = answer
    context.user_data['choices'] = []

    await context.bot.send_message(chat_id=update.effective_chat.id, text=question)

    keyboard = [
        [
            InlineKeyboardButton("I", callback_data=str(ONE)),
            InlineKeyboardButton("II", callback_data=str(TWO)),
            InlineKeyboardButton("III", callback_data=str(THREE)),
            InlineKeyboardButton("IV", callback_data=str(FOUR)),
            InlineKeyboardButton("⟵", callback_data=str(FIVE)),
            InlineKeyboardButton("☑️", callback_data=str(SIX)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(
        "Отвѣты внизу, одинъ изъ нихъ вѣренъ - дерзайте! ",
        reply_markup=reply_markup
        ),
        
        # reply_markup
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


if __name__ == "__main__":
    # Instead of running single handlers in a non-blocking way, we can tell
    # the Application to run the whole call of Application.process_update concurrently:
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler("start", start)
    cat_handler = CommandHandler("cat", catificate)
    dog_handler = CommandHandler("dog", dogificate)

    task_handler = CommandHandler("task", task)

    # Stages

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("task", task)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(one, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
                CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
                CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
                CallbackQueryHandler(apply, pattern="^" + str(SIX) + "$"),
                CallbackQueryHandler(back, pattern="^" + str(FIVE) + "$"),
            ],

            END_ROUTES: [],
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
