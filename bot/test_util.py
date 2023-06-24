# man = input('input a name: ')
# statement = 'some mister %s in the house'
# print(statement % man)

GREETINGS = [
    (
        "Вы, стало быть, крѣпко рѣшили освоить Химію? Что же, %s - "
        "мое почтеніе, сударь! Я, разумѣется, совершенно уже не "
        "тотъ блестящій ученый, однако же всѣ-таки "
        "могу оказаться полезенъ..."
    )
]

print(GREETINGS)


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
    
    elif text:
        return text[:-5]