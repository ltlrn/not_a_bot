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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO,
)
logging.getLogger('httpx').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


TOKEN = getenv('TEST_BOT_TOKEN')

SIGN_UP = 2
GENDER_CHOICE = 0
NAME_CHOICE = 1
GRADE_CHOICE = 3


SKIP_NAME = 13
SKIP_GENDER = 14
SKIP_GRADE = 15
INPUT_NAME = 'name_input'
INPUT_GRADE = 'grade_input'
ADD_USER = 4
START_AGAIN = 5
SHOWING = 6
STOPPING = 7

NAMELESS = 18

TYPING = 11
# INPUT_PROMPT = 12

M = 'male'
F = 'female'

END = 8

FEATURES = []
CURRENT_FEATURE = 'current feature in user data'
START_OVER = 'start over in user data'


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = 'Уточним данные...'

    context.user_data['name_input'] = 'Напечатайте ваше имя'
    context.user_data['grade_input'] = 'Ваш класс, пожалуйста'
    context.user_data[NAMELESS] = False

    buttons = [
        [
            InlineKeyboardButton(text='Уточним?', callback_data=str(ADD_USER)),
            InlineKeyboardButton(text='Нее, и так нормально', callback_data=str(END)),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text = 'изменялово'
    await update.message.reply_text(text=text, reply_markup=keyboard)

    return SIGN_UP


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = 'Здесь будет предложение выбрать регистрацию ' 'или продолжать инкогнито'

    context.user_data['name_input'] = 'Напечатайте ваше имя'
    context.user_data['grade_input'] = 'Ваш класс, пожалуйста'
    context.user_data[NAMELESS] = False

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

    return SIGN_UP


async def gender_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer(text=query.data)

    buttons = [
        [
            InlineKeyboardButton(text='сударь', callback_data=str(M)),
            InlineKeyboardButton(text='сударыня', callback_data=str(F)),
        ],
        [InlineKeyboardButton(text='Оставим это', callback_data=str(SKIP_GENDER)),],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('Выберем пол', reply_markup=keyboard)

    return GENDER_CHOICE


async def name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer(query.data)
    user_data = context.user_data
    user_data['sex'] = query.data

    buttons = [
        [InlineKeyboardButton(text='Представьтесь', callback_data=str(INPUT_NAME))],
        [InlineKeyboardButton(text='Что за допрос?', callback_data=str(SKIP_NAME))],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    await query.edit_message_text('введение имени', reply_markup=keyboard)

    user_data['current_message'] = update.message

    return NAME_CHOICE


async def grade_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data

    buttons = [
        [InlineKeyboardButton(text='Ваш класс?', callback_data=str(INPUT_GRADE)),],
        [InlineKeyboardButton(text='Высший класс!', callback_data=str(END)),],
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # if not user_data.get(START_OVER):
    #     query = update.callback_query
    #     await query.answer(text='refuse to say a name')
    #     print(query.data, 'NNNNNNNNNN')
    #     if query.data == SKIP_NAME:
    #         user_data[NAMELESS] = True
    #     else:
    #         await query.edit_message_text('введение класса', reply_markup=keyboard)

    # else:
    if not user_data.get('ask_name'):
        query = update.callback_query
        await query.answer()
        await query.edit_message_text('введение класса', reply_markup=keyboard)
    else:
        await update.message.reply_text(text='класс сюда', reply_markup=keyboard)

    user_data['current_message'] = update.message

    return GRADE_CHOICE


async def finish_sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    name = user_data.get('first_name')
    grade = user_data.get('grade')
    sex = user_data.get('sex')

    msg = user_data.get('current_message')
    if msg:
        await msg.reply_text(text=f'Name is {name}, grade is {grade}, gender is {sex}')
    # else:
    #     query = update.callback_query
    #     query.answer()
    #     await query.edit_message_text(text=f'Name is {name}, grade is {grade}, gender is {sex}')

    print(f'Name is {name}, grade is {grade}, gender is {sex}')

    user_data['ask_grade'] = False
    user_data['ask_name'] = False

    return ConversationHandler.END


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """End Conversation by command."""

    query = update.callback_query
    await query.answer()

    user_data = context.user_data
    await query.edit_message_text(text=f"Итакъ...{user_data.get('first_name')}")

    return ConversationHandler.END


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    query = update.callback_query
    prompt_text = context.user_data.get(query.data)
    text = 'ИМЯ ВВЕДИ'

    await query.answer(text=query.data)
    await query.edit_message_text(text=text)

    user_data = context.user_data

    user_data['ask_grade'] = False
    user_data['ask_name'] = True
    user_data.get('current_message')

    return TYPING


async def ask_grade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Prompt user to input data for selected feature."""
    query = update.callback_query
    prompt_text = context.user_data.get(query.data)
    text = 'ВВЕДИ КЛАСС'

    user_data = context.user_data
    user_data['ask_grade'] = True
    user_data['ask_name'] = False

    await query.answer(text=query.data)
    await query.edit_message_text(text=text)
    user_data.get('current_message')

    return TYPING


async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Save input for feature and return to feature selection."""
    user_data = context.user_data

    if user_data['ask_grade'] and not user_data['ask_name']:
        user_data['grade'] = update.message.text
        return await finish_sign_up(update, context)

    elif user_data['ask_name'] and not user_data['ask_grade']:
        user_data['first_name'] = update.message.text
        print('I AM HERE!!')
        return await grade_input(update, context)


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            CommandHandler('profile', profile),
        ],
        states={
            SIGN_UP: [
                CallbackQueryHandler(gender_choose, pattern='^' + str(ADD_USER) + '$'),
                CallbackQueryHandler(stop, pattern='^' + str(END) + '$'),
            ],
            GENDER_CHOICE: [
                CallbackQueryHandler(
                    name_input, pattern='^' + str(M) + '|' + str(F) + '$'
                ),
                CallbackQueryHandler(name_input, pattern='^' + str(SKIP_GENDER) + '$'),
            ],
            NAME_CHOICE: [
                CallbackQueryHandler(ask_name, pattern='^' + str(INPUT_NAME) + '$'),
                CallbackQueryHandler(grade_input, pattern='^' + str(SKIP_NAME) + '$'),
            ],
            GRADE_CHOICE: [
                CallbackQueryHandler(ask_grade, pattern='^' + str(INPUT_GRADE) + '$'),
                CallbackQueryHandler(finish_sign_up, pattern='^' + str(END) + '$'),
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
