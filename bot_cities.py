# -*- coding: utf8 -*-

import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings
import utils

logging.basicConfig(
    format="%(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="bot.log",
)


def new_game(bot, update):
    """
    Запускаем новую игру для текущего пользователя,
    создаем базу городов и базу последней буквы.
    """
    chat_id = update.message.chat_id
    text = """Привет! Сыграем в города? Немного поясню правила: 
    города только России, в случае написания города в несколько слов, 
    пиши слитно, пожалуй все, удачи! Запрос отправляй в формате 
    /city твойгород. Для перезапуска игры /restart."""
    update.message.reply_text(text)
    utils.set_user_game(chat_id)
    utils.set_bot_past_letter_for_game(chat_id)


def restart_game(bot, update):
    """
    Перезапускаем игру.
    """
    chat_id = update.message.chat_id
    text = "Игра будет перезапущена!"
    update.message.reply_text(text)
    utils.finish_user_game(chat_id)


def city_game(bot, update):
    """
    Играем в города.
    """
    chat_id = update.message.chat_id
    user_city_low = update.message.text.split()[1]
    user_city = user_city_low.upper()
    update.message.reply_text(("Ты назвал город: {0}").format(user_city))
    user_answer = user_city
    implement_get_next_user_answer = utils.get_next_user_answer(chat_id, user_answer)
    if implement_get_next_user_answer == True:
        user_past_letter = utils.client_past_letter(user_answer)
        update.message.reply_text(("Мне на букву {0}.").format(user_past_letter))
        bot_answer = utils.programm_answer(chat_id, user_past_letter)
        if bot_answer != False:
            update.message.reply_text(("Мой ответ {0}.").format(bot_answer))
            bot_past_letter = utils.programm_past_letter(chat_id, bot_answer)
            update.message.reply_text(("Тебе на букву {1}").format(bot_past_letter))
        else:
            update.message.reply_text("Поздравляю с победой!")
    else:
        update.message.reply_text("Твой ответ не принимается, попробуй снова.")


def main():
    mybot = Updater(
        "539198846:AAH1LYODa8PGq-OEoRVJNpiPk4IxPxxvdik", request_kwargs=settings.PROXY
    )

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", new_game))
    dp.add_handler(CommandHandler("city", city_game))
    dp.add_handler(CommandHandler("restart", restart_game))

    mybot.start_polling()
    mybot.idle()


main()
