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
    TaskCallbacks,
    SignUp,
    StateConstants,
)
from test_util import GREETINGS, keyboard_constructor
from commands import profile, start, catificate, dogificate, echo

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
)

logger = logging.getLogger(__name__)
load_dotenv()

TOKEN = getenv('BOT_TOKEN')
CAT = getenv('CAT_URL')
DOG = getenv('DOG_URL')


# async def _start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     # Get user that sent /start and log his name
#     # await context.bot.set_chat_menu_button(MenuButtonCommands)

#     user = update.message.from_user
#     logger.info('User %s started the conversation.', user.first_name)

#     chat = update.effective_chat
#     name = update.message.chat.first_name

#     buttons = ReplyKeyboardMarkup([['/task', '/cat', '/dog'],], resize_keyboard=True,)

#     menu_button_1 = MenuButton(str)

#     await context.bot.send_message(
#         chat_id=chat.id, text=GREETINGS[0] % name, reply_markup=buttons,
#     )


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
        'Отвѣты внизу, одинъ изъ нихъ вѣренъ - дерзайте!', reply_markup=reply_markup,
    ),

    # reply_markup
    # Tell ConversationHandler that we're in state `FIRST` now
    return StateConstants.START_ROUTES


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler('start', start)

    task_handler = CommandHandler('task', task)
    quiz_callbacks = []

    for raw_number in range(1, 9):
        quiz_callbacks.append(TaskCallbacks.callback_constructor(raw_number))

    start_routes = []

    for func, pattern in zip(quiz_callbacks, range(2, 8)):
        start_routes.append(
            CallbackQueryHandler(func, pattern='^' + str(pattern) + '$')
        )

    service_callbacks = [
        CallbackQueryHandler(TaskCallbacks.back, pattern='^' + str(0) + '$'),
        CallbackQueryHandler(TaskCallbacks.apply, pattern='^' + str(1) + '$'),
    ]

    routes = start_routes + service_callbacks

    task_handler = ConversationHandler(
        entry_points=[CommandHandler('task', task)],
        states={StateConstants.START_ROUTES: routes, StateConstants.END_ROUTES: [],},
        fallbacks=[CommandHandler('task', task)],
    )

    signup_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('profile', profile),
        ],
        states={
            StateConstants.SIGN_UP: [
                CallbackQueryHandler(
                    SignUp.gender_choose,
                    pattern='^' + str(StateConstants.ADD_USER) + '$',
                ),
                # CallbackQueryHandler(stop, pattern='^' + str(END) + '$'),
            ],
            StateConstants.GENDER_CHOICE: [
                CallbackQueryHandler(
                    SignUp.name_input,
                    pattern='^'
                    + str(StateConstants.M)
                    + '|'
                    + str(StateConstants.F)
                    + '$',
                ),
                CallbackQueryHandler(
                    SignUp.name_input,
                    pattern='^' + str(StateConstants.SKIP_GENDER) + '$',
                ),
            ],
            StateConstants.NAME_CHOICE: [
                CallbackQueryHandler(
                    SignUp.ask_name, pattern='^' + str(StateConstants.INPUT_NAME) + '$'
                ),
                CallbackQueryHandler(
                    SignUp.grade_input,
                    pattern='^' + str(StateConstants.SKIP_NAME) + '$',
                ),
            ],
            StateConstants.GRADE_CHOICE: [
                CallbackQueryHandler(
                    SignUp.ask_grade,
                    pattern='^' + str(StateConstants.INPUT_GRADE) + '$',
                ),
                CallbackQueryHandler(
                    SignUp.finish_sign_up, pattern='^' + str(StateConstants.END) + '$'
                ),
            ],
            StateConstants.TYPING: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, SignUp.save_input)
            ],
            StateConstants.STOPPING: [
                CommandHandler('start', start),
                # CallbackQueryHandler(stop, pattern='^' + str(END) + '$'),
            ],
        },
        fallbacks=[],
    )

    # echo of non-empty, non-command messages
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # may be "add_handlerS" instead?

    app.add_handler(start_handler)

    app.add_handler(signup_handler)
    app.add_handler(task_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)
