from telegram import InlineKeyboardButton
from exceptions import OutOfRangeError


GREETINGS = [
    (
        'Вы, стало быть, крѣпко рѣшили освоить Химію? Что же, %s - '
        'мое почтеніе, сударь! Я, разумѣется, совершенно уже не '
        'тотъ блестящій ученый, однако же всѣ-таки '
        'могу оказаться полезенъ...'
    )
]


def keyboard_constructor(buttons_amount: int) -> list:
    """Функция принимает на вход число, отвечающее желаемому количеству кнопок
    во встроенной клавиатуре: оно должно находиться в диапазоне от 2 до 8 и
    выбираться из расчета 2+n (2 кнопки выполняют служебные функции и должны
    всегда находиться в составе клавиатуры, n кнопок соответствуют вариантам
    ответов).
       Возвращает список списков экземпляров класса 
    telegram.InlineKeyboardButton, что соответствует интерфейсу класса
    InlineKeyboardMarkup.
    """

    if buttons_amount < 2 or buttons_amount > 8:
        raise OutOfRangeError('Аргумент buttons_amount за пределами диапазона')

    layout_set = ['⟵', '☑️', 'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII']
    callback_data_set = range(buttons_amount)

    keyboard = []

    for text, data in zip(layout_set[:buttons_amount], callback_data_set):
        keyboard.append(InlineKeyboardButton(text, callback_data=str(data)))

    # преобразуем список так, чтобы две служебные кнопки всегда были в конце:
    if len(keyboard) > 2:
        keyboard = keyboard[2:] + keyboard[:2]

    return [keyboard]


def text_adder(addition: str, query) -> str:
    text = query.message.text
    if not text.startswith('['):
        return addition
    else:
        return text + addition


def text_subber(query) -> str:
    text = query.message.text
    if not text.startswith('['):
        return text

    text = text[:-5]
    if not text:
        return 'Отвѣты внизу, одинъ изъ нихъ вѣренъ - дерзайте!'

    return text
