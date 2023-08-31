import logging
from os import getenv

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    Update,
    MenuButton,
    MenuButtonCommands,
)

from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from urllib3.util.retry import Retry

from callbacks import (
    END_ROUTES,
    FOUR,
    FIVE,
    SIX,
    ONE,
    START_ROUTES,
    THREE,
    TWO,
    four,
    one,
    back,
    apply,
    three,
    two,
    callback_constructor,
)
from test_util import GREETINGS, keyboard_constructor

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
load_dotenv()

TOKEN = getenv('TEST_BOT_TOKEN')
CAT = getenv('CAT_URL')
DOG = getenv('DOG_URL')


def get_a_pet(api: str) -> str:
    response = requests.get(api).json()[0]
    url = response.get('url')

    return url


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get user that sent /start and log his name
    # await context.bot.set_chat_menu_button(MenuButtonCommands)

    user = update.message.from_user
    logger.info('User %s started the conversation.', user.first_name)

    chat = update.effective_chat
    name = update.message.chat.first_name

    buttons = ReplyKeyboardMarkup(
        [['/task', '/cat', '/dog'],], resize_keyboard=True,
    )

    menu_button_1 = MenuButton(str)

    await context.bot.send_message(
        chat_id=chat.id, text=GREETINGS[0] % name, reply_markup=buttons,
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'id: {update.effective_chat.id}, text: {update.message.text}',
    )


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить задачу из api."""

    url = 'http://195.2.93.26/api/tasks/2/'

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    response = session.get(url).json()
    question = response.get('image')
    answer = response.get('answer')
    photo = requests.get(question).content

    context.user_data['answer'] = answer
    context.user_data['answer_vars'] = list(range(5))
    context.user_data['choices'] = []

    logger.info('Task has loaded from the server')
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=photo)

    keyboard = keyboard_constructor(len(context.user_data['answer_vars']) + 2)
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send message with text and appended InlineKeyboard
    await update.message.reply_text(
        'Отвѣты внизу, одинъ изъ нихъ вѣренъ - дерзайте!',
        reply_markup=reply_markup,
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


if __name__ == '__main__':
    # Instead of running single handlers in a non-blocking way, we can tell
    # the Application to run the whole call of Application.process_update concurrently:
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler('start', start)
    cat_handler = CommandHandler('cat', catificate)
    dog_handler = CommandHandler('dog', dogificate)

    task_handler = CommandHandler('task', task)

    # quiz callback routes: ########################################

    quiz_callbacks = []

    for raw_number in range(1, 9):
        quiz_callbacks.append(callback_constructor(raw_number))

    start_routes = []

    for func, pattern in zip(quiz_callbacks, range(2, 8)):
        start_routes.append(
            CallbackQueryHandler(func, pattern='^' + str(pattern) + '$')
        )

    service_callbacks = [
        CallbackQueryHandler(back, pattern='^' + str(0) + '$'),
        CallbackQueryHandler(apply, pattern='^' + str(1) + '$'),
    ]

    routes = start_routes + service_callbacks

    # ##############################################################

    task_handler = ConversationHandler(
        entry_points=[CommandHandler('task', task)],
        states={
            START_ROUTES: routes,
            # [
            #     CallbackQueryHandler(one, pattern="^" + str(2) + "$"),
            #     CallbackQueryHandler(two, pattern="^" + str(3) + "$"),
            #     CallbackQueryHandler(three, pattern="^" + str(4) + "$"),
            #     CallbackQueryHandler(four, pattern="^" + str(5) + "$"),
            #     # CallbackQueryHandler(five, pattern="^" + str(6) + "$"),
            #     # CallbackQueryHandler(six, pattern="^" + str(7) + "$"),
            #     # CallbackQueryHandler(seven, pattern="^" + str(8) + "$"),
            #     # CallbackQueryHandler(eight, pattern="^" + str(9) + "$"),
            #     CallbackQueryHandler(back, pattern="^" + str(0) + "$"),
            #     CallbackQueryHandler(apply, pattern="^" + str(1) + "$"),
            # ],
            END_ROUTES: [],
        },
        fallbacks=[CommandHandler('task', task)],
    )

    # echo of non-empty, non-command messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # may be "add_handlerS" instead?

    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(cat_handler)
    app.add_handler(dog_handler)

    app.add_handler(task_handler)

    app.run_polling()
