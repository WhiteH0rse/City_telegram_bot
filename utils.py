import shelve

import settings


def set_user_game(chat_id, RUSSIAN_CITY_LIST, bot_past_letter=""):
    """
    Записываем юзера в игроки и даем ему список городов.
    Создаем в базе значение последней буквы конкретному пользователю.
    param chat_id: id юзера
    param RUSSIAN_CITY_LIST: список городов для конкретного пользователя
    param bot_past_letter: последняя буква на которую пользователю называть город
    """
    with shelve.open("shelve_players") as storage:
        storage[str(chat_id)] = {
            "bot_past_letter": bot_past_letter,
            "city_dictionary": RUSSIAN_CITY_LIST,
        }


def finish_user_game(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем его из хранилища
    param chat_id: id юзера
    """
    with shelve.open("shelve_players") as storage:
        del storage[str(chat_id)]


def get_next_user_answer(chat_id, user_answer):
    """
    Получаем ответы от текущего юзера.
    param chat_id: id юзера
    param bot_past_letter(берем из базы): последняя буква бота
    param user_answer: город пользователя
    return: сообщение об ошибке
    """
    with shelve.open("shelve_players") as storage:
        bot_past_letter = storage[str(chat_id)]["bot_past_letter"]
        db_shelve = storage[str(chat_id)]
        if (user_answer in db_shelve["city_dictionary"]) and (
            user_answer[0] == bot_past_letter or bot_past_letter == ""
        ):
            db_shelve["city_dictionary"].remove(user_answer)
            storage[str(chat_id)] = db_shelve
            return True
        else:
            return False


def client_past_letter(user_answer):
    """
    Получаем последнюю букву города пользователя.
    param user_answer: город пользователя
    return user_past_letter: последняя буква в городе пользователя 
    """
    user_past_letter = user_answer[-1]
    if user_past_letter in ("Ы", "Й", "Ь"):
        user_past_letter = user_answer[-2]
        if user_past_letter in ("Ы", "Й", "Ь"):
            user_past_letter = user_answer[-3]
    return user_past_letter


def programm_past_letter(chat_id, bot_answer):
    """
    Получаем последнюю букву города бота.
    param chat_id: id юзера
    param bot_answer: город бота
    return bot_past_letter: последняя буква в городе бота 
    """
    bot_past_letter = bot_answer[-1]
    if bot_past_letter in ("Ы", "Й", "Ь"):
        bot_past_letter = bot_answer[-2]
        if bot_past_letter in ("Ы", "Й", "Ь"):
            bot_past_letter = bot_answer[-3]
    with shelve.open("shelve_players") as storage:
        db_shelve = storage[str(chat_id)]
        db_shelve.update({"bot_past_letter": bot_past_letter})
        storage[str(chat_id)] = db_shelve
    return bot_past_letter


def programm_answer(chat_id, user_past_letter):
    """
    Даем ответ бота.
    param chat_id: id юзера
    param user_past_letter: последняя буква города пользователя
    return: город программы
    """
    with shelve.open("shelve_players") as storage:
        db_shelve = storage[str(chat_id)]
        for bot_answer_for_cycle in db_shelve["city_dictionary"]:
            if bot_answer_for_cycle[0] == user_past_letter:
                db_shelve["city_dictionary"].remove(bot_answer_for_cycle)
                storage[str(chat_id)] = db_shelve
                bot_answer = bot_answer_for_cycle
                return bot_answer
