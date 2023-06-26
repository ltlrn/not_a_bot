from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from test_util import text_adder, text_subber, keyboard_constructor

START_ROUTES, END_ROUTES = range(2)
# Callback data
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    print("CALLBACK DATA", context.user_data)
    answer = context.user_data["answer"]  # answer thing
    await query.answer()

    keyboard = keyboard_constructor(6)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        # text="Вы скрываете свой талантъ ото всѣхъ также хорошо, какъ и отъ меня?",
        text=text_adder("[ 1 ]", query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].append(1)

    return START_ROUTES


async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query

    await query.answer()

    keyboard = keyboard_constructor(6)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        # text="Браво! Академики рукоплещутъ!"
        text=text_adder("[ 2 ]", query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].append(2)

    return START_ROUTES


async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons. This is the end point of the conversation."""

    query = update.callback_query
    await query.answer()

    keyboard = keyboard_constructor(6)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        # text="Костыль мнѣ въ ротъ!",
        text=text_adder("[ 3 ]", query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].append(3)

    return START_ROUTES


async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""

    query = update.callback_query
    await query.answer()

    keyboard = keyboard_constructor(6)
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        # text="Феноменальный бредъ...",
        text=text_adder("[ 4 ]", query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].append(4)

    return START_ROUTES


async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """

    query = update.callback_query

    await query.answer()
    await query.edit_message_text(text="Итакъ...")

    if context.user_data["choices"] == [context.user_data["answer"]]:
        await query.edit_message_text(text="Браво! Академики рукоплещутъ!")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Это дѣйствительно правильный отвѣтъ!",
        )
    else:
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text="Феноменальный бредъ..."
        )

    return ConversationHandler.END


async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query

    await query.answer()

    keyboard = keyboard_constructor(6)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text_subber(query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].pop()

    return START_ROUTES
