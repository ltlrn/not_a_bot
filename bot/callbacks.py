from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, ConversationHandler
from test_util import text_adder, text_subber, keyboard_constructor


class TaskCallbacks:
    """Коробочка с функциями обратного вызова для команды /task."""

    @staticmethod
    def callback_constructor(raw_number: int):
        async def callback_func(
            update: Update, context: ContextTypes.DEFAULT_TYPE
        ) -> int:

            answer_vars = context.user_data['answer_vars']

            buttons_amount = len(answer_vars) + 2
            callback_number = raw_number
            query = update.callback_query

            button_text = text_adder(f'[ {callback_number} ]', query)

            await query.answer()

            keyboard = keyboard_constructor(buttons_amount)
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                text=button_text, reply_markup=reply_markup,
            )

            context.user_data['choices'].append(callback_number)

            return StateConstants.START_ROUTES

        return callback_func

    @staticmethod
    async def apply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query

        await query.answer()
        await query.edit_message_text(text='Итакъ...')

        if context.user_data['choices'] == [context.user_data['answer']]:
            await query.edit_message_text(text='Браво! Академики рукоплещутъ!')
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Это дѣйствительно правильный отвѣтъ!',
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id, text='Феноменальный бредъ...'
            )

        return ConversationHandler.END

    @staticmethod
    async def back(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query

        answer_vars = context.user_data['answer_vars']
        buttons_amount = len(answer_vars) + 2

        await query.answer()

        keyboard = keyboard_constructor(buttons_amount)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text_subber(query), reply_markup=reply_markup,
        )

        context.user_data['choices'].pop()

        return StateConstants.START_ROUTES

    @staticmethod
    async def one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        query = update.callback_query
        answer = context.user_data['answer']  # answer thing

        await query.answer()

        keyboard = keyboard_constructor(6)

        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text_adder('[ 1 ]', query), reply_markup=reply_markup,
        )

        context.user_data['choices'].append(1)

        return StateConstants.START_ROUTES

    @staticmethod
    async def two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""

        query = update.callback_query

        await query.answer()

        keyboard = keyboard_constructor(6)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text_adder('[ 2 ]', query), reply_markup=reply_markup,
        )

        context.user_data['choices'].append(2)

        return StateConstants.START_ROUTES

    @staticmethod
    async def three(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons. This is the end point of the conversation."""

        query = update.callback_query
        await query.answer()

        keyboard = keyboard_constructor(6)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text_adder('[ 3 ]', query), reply_markup=reply_markup,
        )

        context.user_data['choices'].append(3)

        return StateConstants.START_ROUTES

    @staticmethod
    async def four(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Show new choice of buttons"""

        query = update.callback_query
        await query.answer()

        keyboard = keyboard_constructor(6)
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text(
            text=text_adder('[ 4 ]', query), reply_markup=reply_markup,
        )

        context.user_data['choices'].append(4)

        return StateConstants.START_ROUTES


class StateConstants:
    """Класс содержит набор констант, необходимых для переключения между состояниями
    обработчиков ConversationHandlers, а также выступающими в качестве callback data,
    ассоциированными с кнопками встроенной клавиатуры.
    """

    (
        SIGN_UP,
        GENDER_CHOICE,
        NAME_CHOICE,
        GRADE_CHOICE,
        SKIP_NAME,
        SKIP_GENDER,
        SKIP_GRADE,
        ADD_USER,
        START_AGAIN,
        SHOWING,
        STOPPING,
        NAMELESS,
        TYPING,
        END,
    ) = range(14)

    START_ROUTES, END_ROUTES = range(14, 16)
    ONE, TWO, THREE, FOUR, FIVE, SIX = range(16, 22)

    M = 'male'
    F = 'female'
    INPUT_NAME = 'name_input'
    INPUT_GRADE = 'grade_input'

    FEATURES = []
    CURRENT_FEATURE = 'current feature in user data'
    START_OVER = 'start over in user data'


class SignUp:
    """Содержит набор методов обратного вызова для обеспечения работоспособности 
    регистрации в боте."""

    @staticmethod
    async def gender_choose(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Функция обратного вызова, отвечающая за выбор пола при регистрации в боте.
        Возвращает целое число, которое впоследствии позволяет переключить состояние
        обработчика ConversationHandler на GENDER_CHOICE."""

        query = update.callback_query
        await query.answer(text=query.data)

        buttons = [
            [
                InlineKeyboardButton(
                    text='сударь', callback_data=str(StateConstants.M)
                ),
                InlineKeyboardButton(
                    text='сударыня', callback_data=str(StateConstants.F)
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Оставим это', callback_data=str(StateConstants.SKIP_GENDER),
                ),
            ],
        ]

        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text('Выберем пол', reply_markup=keyboard)

        return StateConstants.GENDER_CHOICE

    @staticmethod
    async def name_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Функция обратного вызова, предлогающая ввести имя или пропустить этот шаг.
        Возвращает константу для переключения состояния обработчика на NAME_CHOICE."""

        query = update.callback_query
        await query.answer(query.data)
        user_data = context.user_data
        user_data['sex'] = query.data

        buttons = [
            [
                InlineKeyboardButton(
                    text='Представьтесь', callback_data=str(StateConstants.INPUT_NAME),
                )
            ],
            [
                InlineKeyboardButton(
                    text='Что за допрос?', callback_data=str(StateConstants.SKIP_NAME),
                )
            ],
        ]
        keyboard = InlineKeyboardMarkup(buttons)

        await query.edit_message_text('введение имени', reply_markup=keyboard)
        user_data['current_message'] = update.message

        return StateConstants.NAME_CHOICE

    @staticmethod
    async def grade_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Функция обратного вызова, отвечающая за выбор вводить ли класс или пропустить этот шаг.
        Возвращает константу для перевода состояния обработчика на GRADE_CHOICE."""

        buttons = [
            [
                InlineKeyboardButton(
                    text='Ваш класс?', callback_data=str(StateConstants.INPUT_GRADE),
                ),
            ],
            [
                InlineKeyboardButton(
                    text='Высший класс!', callback_data=str(StateConstants.END)
                ),
            ],
        ]

        keyboard = InlineKeyboardMarkup(buttons)
        user_data = context.user_data

        if not user_data.get('ask_name'):
            query = update.callback_query
            await query.answer()
            await query.edit_message_text('введение класса', reply_markup=keyboard)
        else:
            await update.message.reply_text(text='класс сюда', reply_markup=keyboard)

        user_data['current_message'] = update.message

        return StateConstants.GRADE_CHOICE

    @staticmethod
    async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Приглашение для ввода имени, переводит ConversationHandler в состояние TYPING."""

        query = update.callback_query
        prompt_text = context.user_data.get(query.data)
        text = 'ИМЯ ВВЕДИ'

        await query.answer(text=query.data)
        await query.edit_message_text(text=text)

        user_data = context.user_data

        user_data['ask_grade'] = False
        user_data['ask_name'] = True
        user_data.get('current_message')

        return StateConstants.TYPING

    @staticmethod
    async def ask_grade(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Приглашение для ввода имени, переводит ConversationHandler в состояние TYPING."""

        query = update.callback_query
        prompt_text = context.user_data.get(query.data)
        text = 'ВВЕДИ КЛАСС'

        user_data = context.user_data
        user_data['ask_grade'] = True
        user_data['ask_name'] = False

        await query.answer(text=query.data)
        await query.edit_message_text(text=text)
        user_data.get('current_message')

        return StateConstants.TYPING

    @staticmethod
    async def save_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
        """Сотраняет ввод, в зависимости от состояния диалога возвращает 
        соответствующую функцию обратного вызова.
        """

        user_data = context.user_data

        if user_data['ask_grade'] and not user_data['ask_name']:
            user_data['grade'] = update.message.text
            return await SignUp.finish_sign_up(update, context)

        elif user_data['ask_name'] and not user_data['ask_grade']:
            user_data['first_name'] = update.message.text
            print('I AM HERE!!')
            return await SignUp.grade_input(update, context)

    @staticmethod
    async def finish_sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Завершает диалог, выводит собранную информацию."""

        user_data = context.user_data
        name = user_data.get('first_name')
        grade = user_data.get('grade')
        sex = user_data.get('sex')

        msg = user_data.get('current_message')
        if msg:
            await msg.reply_text(
                text=f'Name is {name}, grade is {grade}, gender is {sex}'
            )
        # else:
        #     query = update.callback_query
        #     query.answer()
        #     await query.edit_message_text(text=f'Name is {name}, grade is {grade}, gender is {sex}')

        print(f'Name is {name}, grade is {grade}, gender is {sex}')

        user_data['ask_grade'] = False
        user_data['ask_name'] = False
        # chat = update.effective_chat

        # buttons = ReplyKeyboardMarkup([['/task', '/profile'],], resize_keyboard=True,)
        # await context.bot.send_message(
        #     chat_id=chat.id, text='Начинаем учиться!', reply_markup=buttons,
        # )

        return ConversationHandler.END
