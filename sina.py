#!/usr/bin/env python3
import time
import json
from telegram import *
from telegram.ext import *
import logging
import os




# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    user_id = update.message.chat_id
    if user_id == 117392973:
        print(1)
        # txt = download()
        # print(1111)
        # bot.send_message(117392973, txt)
    else:
        print(update)
        firstName = update.message.chat.first_name
        lastName = update.message.chat.last_name
        print("***\t", firstName, lastName, "\t***")
        if not lastName is None and not firstName is None:
            spy = firstName + " " + lastName + " \nchatID = " + str(user_id)
        if lastName is None:
            spy = firstName + " \nchatID = " + str(user_id)
        if firstName is None:
            spy = lastName + " \nchatID = " + str(user_id)

        bot.send_message(117392973, spy)
        warning = spy + "\nJust Fuck Sina"
        bot.send_message(user_id, warning)
        # bot.sendPhoto(user_id,'https://scontent-frx5-1.cdninstagram.com/vp/802cda62eb0ce260bfc5cac57bb39695/5D424F1D/t51.12442-15/e35/67878406_1100893550298599_195124236546211249_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&ig_cache_key=MjA5ODc5MTE1NTM2OTE2NTY2MA%3D%3D.2',caption="farshadpour-201907301140")



def cancel(bot, update):
    pass


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def process_msg(bot, update):
    print(4)
    #msg = update.message.text
    message = update.message
    if 'voice' in message:
        print(7)
    for i in message:
        if i == 'voice':
            print(8)
    print(message)
    #bot.send_message(user_id, msg, reply_markup=reply_markup)
    # print(username)
    # print(update.message)


def process_command(bot, update):
    id = update.message.from_user.id
    command = update.message.text[1:]
    if command[0] == 'cancel':
        bot.send_message(id, 'bye')
    if command[0] == 'story':
        bot.send_message(id, 'enter username')
    if command[0] == 'picture':
        bot.send_message(id, 'enter username')




def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("822996651:AAFLw1zgcmLZ9NfUdMVSpFd_Yzr-YY1Jv4U")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('cancel', cancel))

    # dp.add_handler(MessageHandler(Filters.all
    #                               & Filters.private
    #                               & ~Filters.command
    #                               & ~Filters.status_update,
    #                               process_msg))

    # dp.add_handler(MessageHandler(Filters.command
    #                               & Filters.private, process_command))
    dp.add_handler(MessageHandler(Filters.group, process_msg))



    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
