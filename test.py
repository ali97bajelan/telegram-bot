from InstagramAPI import InstagramAPI

# from telegram import (Bot, Update, ChatAction, TelegramError, User, InlineKeyboardMarkup,
#                       InlineKeyboardButton, InlineQueryResultArticle, InputTextMessageContent,
#                       ShippingOption, LabeledPrice)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def competition():
    return 'hi'



def start(bot, update):
    user_id = update.message.chat_id

    bot.send_message(user_id,'enter a number between 1-100')
    x = update.message
    print(x)

    if user_id == 117392973:
        txt = competition()
        bot.send_message(117392973, txt)
    else:
        firstName=update.message.chat.first_name
        lastName=update.message.chat.last_name
        print(firstName,lastName)
        if not lastName is None and not firstName is None :
            spy = firstName + " " + lastName + " \nchatID = " + str(user_id)
        if lastName is None :
            spy = firstName + " \nchatID = " + str(user_id)
        if firstName is None :
            spy = lastName + " \nchatID = " + str(user_id)


        bot.send_message(117392973, spy)
        warning = spy+"\nyou are not allowed to use this bot. your name has been sent for bot's creator"
        bot.send_message(user_id, warning)


def cancel(bot, update):
    pass


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("580725053:AAGPq9ErFzBKoXTfDhirpNHYLc_IqilTIc4")
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # conversation_handle = ConversationHandler(entry_points=[CommandHandler('start', start)],fallbacks=[CommandHandler('cancel', cancel)])

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('cancel', cancel))

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
