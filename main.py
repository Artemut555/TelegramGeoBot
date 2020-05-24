import telebot
import config
import random
import qmanager
from telebot import types
import ScoreBoard

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['game'])
def game(message):
    qmanager.fill_shelve(message.chat.id, message.chat.username)  # fills info about user
    qmanager.send_question(bot, message.chat.id)  # sends question


@bot.message_handler(commands=['board'])  # custom command not for user
def show_board(message):
    text = ScoreBoard.get_score_board()
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    if not qmanager.is_shown(message.chat.id):  # check if question is shown or not exists
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        question = qmanager.get_question(message.chat.id)  # gets question
        right_answer = question[2]
        wrong_answers = question[3]

        keyboard_hider = types.ReplyKeyboardRemove()

        answered = False  # check if variant was chosen

        if message.text == right_answer:
            qmanager.update_answer(message.chat.id, True, question)
            bot.send_message(message.chat.id, 'Верно!', reply_markup=keyboard_hider)
            answered = True
        elif message.text not in wrong_answers:
            bot.send_message(message.chat.id, 'Такого варианта нет, попробуйте ещё раз', reply_markup=keyboard_hider)
        else:
            qmanager.update_answer(message.chat.id, False, question)
            bot.send_message(message.chat.id, f'Правильный ответ {right_answer}', reply_markup=keyboard_hider)
            answered = True

        if answered:
            score = ScoreBoard.get_score(message.chat.id)
            bot.send_message(message.chat.id, f'Ваш счёт:{score}')
            text = ScoreBoard.get_score_board()
            bot.send_message(message.chat.id, text)

        qmanager.send_question(bot, message.chat.id)


if __name__ == '__main__':
    random.seed()
    bot.infinity_polling()
