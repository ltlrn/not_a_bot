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

from callbacks import StateConstants


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = 'Уточним данные...'

    context.user_data['name_input'] = 'Напечатайте ваше имя'
    context.user_data['grade_input'] = 'Ваш класс, пожалуйста'

    buttons = [
        [
            InlineKeyboardButton(text='Уточним?', callback_data=str(StateConstants.ADD_USER)),
            InlineKeyboardButton(
                text='Нее, и так нормально', callback_data=str(StateConstants.END)
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    text = 'изменялово'
    await update.message.reply_text(text=text, reply_markup=keyboard)

    return StateConstants.SIGN_UP


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    """Select an action: Adding parent/child or show data."""
    text = (
        'Здесь будет предложение выбрать регистрацию '
        'или продолжать инкогнито'
    )

    context.user_data['name_input'] = 'Напечатайте ваше имя'
    context.user_data['grade_input'] = 'Ваш класс, пожалуйста'

    buttons = [
        [
            InlineKeyboardButton(
                text='Знакомство', callback_data=str(StateConstants.ADD_USER)
            ),
            InlineKeyboardButton(
                text='Заниматься инкогнито', callback_data=str(StateConstants.END)
            ),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    # If we're starting over we don't need to send a new message
    if context.user_data.get(StateConstants.START_AGAIN):
        await update.callback_query.answer()
        await update.callback_query.edit_message_text(
            text=text, reply_markup=keyboard
        )
    else:
        text = 'Здесь пространное приветственное сообщение'
        await update.message.reply_text(text=text, reply_markup=keyboard)

    context.user_data[StateConstants.START_AGAIN] = False

    return StateConstants.SIGN_UP