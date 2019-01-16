# -*- coding: utf8 -*-

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler

import settings
from handlers import new_game, city_game

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=settings.PROXY)

    dp = mybot.dispatcher
    dp.add_handler(RegexHandler("^(Начать новую игру)$", new_game))
    dp.add_handler(MessageHandler(Filters.text, city_game))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
