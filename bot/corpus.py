import logging
import requests

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler
from dotenv import load_dotenv
from os import getenv


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

TOKEN = getenv('BOT_TOKEN')
URL = getenv('CAT_URL')


def get_a_cat() -> str:
    response = requests.get(URL).json()[0]
    url = response.get('url')

    return url


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='I am not a bot, this is a mistake!'
    )


async def echo(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'id: {update.effective_chat.id}, text: {update.message.text}'
    )

async def catificate(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):  
    "Функция - котификатор"
    url = get_a_cat()

    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=url
    )


if __name__ == '__main__':

    # Instead of running single handlers in a non-blocking way, we can tell 
    # the Application to run the whole call of Application.process_update concurrently:
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()
    
    start_handler = CommandHandler('start', start)
    cat_handler = CommandHandler('cat', catificate)

    # echo of non-empty, non-command messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)


    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(cat_handler)
    app.run_polling()