from telebot import types
from random import shuffle


def generate_markup(right_answer, wrong_answers):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    all_answers = '{},{}'.format(right_answer, wrong_answers)
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)

    shuffle(list_items)
    for item in list_items:
        markup.add(item)

    return markup
