from telegram import ReplyKeyboardMarkup
from random import sample

import utils
import cities_base


def new_game(bot, update):
    """
    Запускаем новую игру для текущего пользователя,
    создаем базу городов и базу последней буквы.
    """
    chat_id = update.message.chat_id
    text = """Привет! Сыграем в города? Немного поясню правила: 
    города только России, в случае написания города в несколько слов, 
    пиши слитно, пожалуй все, удачи!"""
    RUSSIAN_CITY_LIST = sample(cities_base.RUSSIAN_CITY_LIST, 1097)
    start_keyboard = ReplyKeyboardMarkup([["Начать новую игру"]], resize_keyboard=True)
    update.message.reply_text(text, reply_markup=start_keyboard)
    try:
        utils.finish_user_game(chat_id)
    except KeyError:
        pass
    utils.set_user_game(chat_id, RUSSIAN_CITY_LIST)
    utils.set_bot_past_letter_for_game(chat_id)


def city_game(bot, update):
    """
    Играем в города.
    """
    chat_id = update.message.chat_id
    user_city = update.message.text.upper()
    update.message.reply_text(("Ты назвал город: {0}").format(user_city))
    user_answer = user_city
    implement_get_next_user_answer = utils.get_next_user_answer(chat_id, user_answer)
    if implement_get_next_user_answer == True:
        user_past_letter = utils.client_past_letter(user_answer)
        bot_answer = utils.programm_answer(chat_id, user_past_letter)
        if bot_answer != "":
            update.message.reply_text(("Мой ответ {0}.").format(bot_answer))
            bot_past_letter = utils.programm_past_letter(chat_id, bot_answer)
            update.message.reply_text(("Тебе на букву {0}").format(bot_past_letter))
        else:
            update.message.reply_text("Поздравляю с победой!")
    else:
        update.message.reply_text("Твой ответ не принимается, попробуй снова.")
