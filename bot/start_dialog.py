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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


TOKEN = getenv('TEST_BOT_TOKEN')

SIGN_UP = 2
GENDER_CHOICE = 0
NAME_CHOICE = 1
GRADE_CHOICE = 3

ADD_USER = 4
START_AGAIN = 5
SHOWING = 6
STOPPING = 7

TYPING = 11
INPUT_PROMPT = 12

M = 9
F = 10

END = 8

FEATURES = []
CURRENT_FEATURE = 'current feature in user data'
START_OVER = 'start over in user data'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = 'Здесь будет предложение выбрать регистрацию ' 'или продолжать инкогнито'

    buttons = [
        [
            InlineKeyboardButton(text='Знакомство', callback_data=str(ADD_USER)),
            InlineKeyboardButton(text='Заниматься инкогнито', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(START_AGAIN):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        text = 'Здесь пространное приветственное сообщение'
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[START_AGAIN] = False

    return GENDER_CHOICE


async def gender_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    buttons = [
        [
            InlineKeyboardButton(text='сударь', callback_data=str(M)),
            InlineKeyboardButton(text='сударыня', callback_data=str(F)),
        ],
        [InlineKeyboardButton(text='Оставим это', callback_data=str(NAME_CHOICE)),],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('Выберем пол', reply_markup=keyboard)

    return NAME_CHOICE


async def name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton(text='Представьтесь', callback_data=str(TYPING))],
        [InlineKeyboardButton(text='Что за допрос?', callback_data=str(GRADE_CHOICE))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('введение имени', reply_markup=keyboard)

    return INPUT_PROMPT


async def grade_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()

    buttons = [
        [InlineKeyboardButton(text='Ваш класс?', callback_data=str(TYPING)),],
        [InlineKeyboardButton(text='Высший класс!', callback_data=str(END)),],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('введение имени', reply_markup=keyboard)

    return INPUT_PROMPT


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""

    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    await query.edit_message_text(text=f"Итакъ...{user_data.get('first_name')}")

    # await update.message.reply_text(text=f"Итакъ...{user_data.get('first_name')}")

    return ConversationHandler.END


async def ask_for_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    context.user_data[CURRENT_FEATURE] = update.callback_query.data
    text = 'Напечатайте Ваше имя'

    await update.callback_query.answer()
    await update.callback_query.edit_message_text(text=text)

    return TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data
    user_data['first_name'] = update.message.text

    user_data[START_OVER] = True
    print('WE ARE HERE NOW')

    return GRADE_CHOICE  # await stop(update, context)


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    registration_handlers = []

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            GENDER_CHOICE: [
                CallbackQueryHandler(gender_choose, pattern='^' + str(ADD_USER) + '$'),
                CallbackQueryHandler(stop, pattern='^' + str(END) + '$'),
            ],
            NAME_CHOICE: [
                CallbackQueryHandler(name_input, pattern='^' + str(M) + '|' + str(F) + '$'),
                CallbackQueryHandler(grade_input, pattern='^' + str(GRADE_CHOICE) + '$'),
                ],
            GRADE_CHOICE: [CallbackQueryHandler(
                grade_input, pattern='^' + str(GRADE_CHOICE) + '$'
            )],
            INPUT_PROMPT: [
                CallbackQueryHandler(ask_for_input, pattern='^(?!' + str(END) + ').*$')
            ],
            TYPING: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_input)],
            STOPPING: [
                CommandHandler('start', start),
                CallbackQueryHandler(stop, pattern='^' + str(END) + '$'),
            ],
        },
        fallbacks=[CommandHandler('stop', stop),],
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
