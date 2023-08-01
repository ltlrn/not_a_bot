from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from test_util import text_adder, text_subber, keyboard_constructor

START_ROUTES, END_ROUTES = range(2)
ONE, TWO, THREE, FOUR, FIVE, SIX = range(6)


def callback_constructor(raw_number: int):
    async def callback_func(
            update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> int:

        answer_vars = context.user_data["answer_vars"]

        buttons_amount = len(answer_vars) + 2
        callback_number = raw_number
        query = update.callback_query

        button_text=text_adder(f"[ {callback_number} ]", query)
       
        await query.answer()
        
        keyboard = keyboard_constructor(buttons_amount)
        reply_markup = InlineKeyboardMarkup(keyboard)
    
        await query.edit_message_text(
            text=button_text,
            reply_markup=reply_markup,
        )

        context.user_data["choices"].append(callback_number)

        return START_ROUTES
    
    return callback_func


async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
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

    answer_vars = context.user_data["answer_vars"]
    buttons_amount = len(answer_vars) + 2


    await query.answer()

    keyboard = keyboard_constructor(buttons_amount)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text_subber(query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].pop()

    return START_ROUTES


# class CallbackConstructor:
#     def __init__(self):
#         pass

#     async def callback_function(
#         update: Update, context: ContextTypes.DEFAULT_TYPE
#     ) -> int:
#         pass



async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    answer = context.user_data["answer"]  # answer thing

    await query.answer()

    keyboard = keyboard_constructor(6)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
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

        text=text_adder("[ 4 ]", query),
        reply_markup=reply_markup,
    )

    context.user_data["choices"].append(4)

    return START_ROUTES


