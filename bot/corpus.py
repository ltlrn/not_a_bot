import logging
from os import getenv

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from telegram import Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)
from urllib3.util.retry import Retry

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
CAT = getenv("CAT_URL")
DOG = getenv("DOG_URL")


def get_a_pet(api: str) -> str:
    response = requests.get(api).json()[0]
    url = response.get("url")

    return url


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="I am not a bot, this is a mistake!"
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"id: {update.effective_chat.id}, text: {update.message.text}",
    )


async def task(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Получить задачу из api."""
    url = "http://195.2.93.26/api/tasks/1/"

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    response = session.get(url).json()
    question = response.get("question")

    await context.bot.send_message(chat_id=update.effective_chat.id, text=question)


async def catificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Функция - котификатор."""
    url = get_a_pet(CAT)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


async def dogificate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Собакирование."""
    url = get_a_pet(DOG)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)


if __name__ == "__main__":
    # Instead of running single handlers in a non-blocking way, we can tell
    # the Application to run the whole call of Application.process_update concurrently:
    app = ApplicationBuilder().token(TOKEN).concurrent_updates(True).build()

    start_handler = CommandHandler("start", start)
    cat_handler = CommandHandler("cat", catificate)
    dog_handler = CommandHandler("dog", dogificate)

    task_handler = CommandHandler("task", task)

    # echo of non-empty, non-command messages
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    # may be "add_handlerS" instead?

    app.add_handler(start_handler)
    app.add_handler(echo_handler)
    app.add_handler(cat_handler)
    app.add_handler(dog_handler)

    app.add_handler(task_handler)

    app.run_polling()
