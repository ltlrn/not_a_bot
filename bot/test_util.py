from telegram import InlineKeyboardButton


GREETINGS = [
    (
        "Вы, стало быть, крѣпко рѣшили освоить Химію? Что же, %s - "
        "мое почтеніе, сударь! Я, разумѣется, совершенно уже не "
        "тотъ блестящій ученый, однако же всѣ-таки "
        "могу оказаться полезенъ..."
    )
]


def keyboard_constructor(buttons_amount: int) -> list:
    """The parameter `inline_keyboard should be a sequence
    of sequences of InlineKeyboardButtons.
    """

    layout_set = ["⟵", "☑️", "I", "II", "III", "IV", "V", "VI", "VII", "VIII"]
    callback_data_set = range(buttons_amount)

    keyboard = []

    for text, data in zip(layout_set[:buttons_amount], callback_data_set):
        keyboard.append(InlineKeyboardButton(text, callback_data=str(data)))

    # преобразуем список так, чтобы две служебные кнопки всегда были в конце:
    if len(keyboard) > 2:
        keyboard = keyboard[2:] + keyboard[:2]

    return [keyboard]


print(GREETINGS)


def text_adder(addition: str, query) -> str:
    text = query.message.text
    if not text.startswith("["):
        return addition
    else:
        return text + addition


def text_subber(query) -> str:
    text = query.message.text
    if not text.startswith("["):
        return text

    elif text:
        return text[:-5]
