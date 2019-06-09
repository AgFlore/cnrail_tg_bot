# basics.py
# basic functions for greeting etc.
# By waymao in 2019

from telegram.ext import Updater, CommandHandler

# Welcome msg
def start(bot, update):
    text = 'Hi {}, I\'m a bot, and you can ask me about the chinese railway!'.\
        format(update.message.from_user['username'])
    bot.send_message(chat_id=update.message.chat_id, text=text)

start_handler = CommandHandler('start', start)
