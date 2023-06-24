from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler

START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


async def start_over(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompt same text & keyboard as `start` does but not as new message"""
    # Get CallbackQuery from Update

    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("7", callback_data=str(ONE)),
            InlineKeyboardButton("8", callback_data=str(TWO)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    # Instead of sending a new message, edit the message that
    # originated the CallbackQuery. This gives the feeling of an
    # interactive menu.

    await query.edit_message_text(
        text="Отвѣты внизу, одинъ изъ нихъ вѣренъ - дерзайте! ",
        reply_markup=reply_markup,
    )

    return START_ROUTES


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()

    keyboard = [
        [
            InlineKeyboardButton("I", callback_data=str(ONE)),
            InlineKeyboardButton("II", callback_data=str(TWO)),
            InlineKeyboardButton("III", callback_data=str(THREE)),
            InlineKeyboardButton("IV", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Вы скрываете свой талантъ ото всѣхъ также хорошо, какъ и отъ меня?",
        reply_markup=reply_markup,
    )
    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()

    await query.edit_message_text(text="Браво! Академики рукоплещутъ!")
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Это дѣйствительно правильный отвѣтъ!"
    )

    return ConversationHandler.END


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("I", callback_data=str(ONE)),
            InlineKeyboardButton("II", callback_data=str(TWO)),
            InlineKeyboardButton("III", callback_data=str(THREE)),
            InlineKeyboardButton("IV", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Костыль мнѣ въ ротъ!", reply_markup=reply_markup
    )

    return START_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("I", callback_data=str(ONE)),
            InlineKeyboardButton("II", callback_data=str(TWO)),
            InlineKeyboardButton("III", callback_data=str(THREE)),
            InlineKeyboardButton("IV", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text="Феноменальный бредъ...", reply_markup=reply_markup
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
