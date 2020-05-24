import shelve
from SQLighter import SQLighter
from config import database_name, shelve_name
import keyboard


def fill_shelve(chat_id, username):
    with shelve.open(shelve_name) as storage:
        if not str(chat_id) in storage:
            storage[str(chat_id)] = dict({'score': 0, 'current_q': 1, 'shown_question': False, 'username': username})


def send_question(bot, chat_id):
    row = get_question(chat_id)
    if not row:  # check for None
        bot.send_message(chat_id, 'Поздравляю, вы сыграли все вопросы!')
    else:
        markup = keyboard.generate_markup(row[2], row[3])
        bot.send_message(chat_id, row[1], reply_markup=markup)
        show_question(chat_id)


def get_question(chat_id):
    try:
        db_worker = SQLighter(database_name)
        row_num = get_row_num(chat_id)

        if row_num > db_worker.count_rows():  # check if there is no questions
            return None

        question = db_worker.select_single(row_num)
        db_worker.close()
        return question
        # Если человек не играет, ничего не возвращаем
    except KeyError:
        return None


def update_answer(chat_id, solved, question):
    with shelve.open(shelve_name) as storage:
        temp_store = storage[str(chat_id)]
        if solved:
            temp_store['score'] += 1
        temp_store['current_q'] += 1
        temp_store['shown_question'] = False
        storage[str(chat_id)] = temp_store


def get_row_num(chat_id):
    with shelve.open(shelve_name) as storage:
        return storage[str(chat_id)]['current_q']


def show_question(chat_id):
    with shelve.open(shelve_name) as storage:
        temp_store = storage[str(chat_id)]
        temp_store['shown_question'] = True
        storage[str(chat_id)] = temp_store


def hide_question(chat_id):
    with shelve.open(shelve_name) as storage:
        temp_store = storage[str(chat_id)]
        temp_store['shown_question'] = False
        storage[str(chat_id)] = temp_store


def is_shown(chat_id):
    with shelve.open(shelve_name) as storage:
        if not str(chat_id) in storage:
            return False
        return storage[str(chat_id)]['shown_question']


