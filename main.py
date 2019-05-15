# -*- coding: utf-8 -*-

import time
import json
from telegram import *
from telegram.ext import *
import sys
import datetime
import os
import logging
import threading

secret = -1
choose = 0

Version_Code = 'v1.1.0'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )

PATH = os.path.dirname(os.path.realpath(__file__)) + '/'

CONFIG = json.loads(open(PATH + 'config.json', 'r').read())

LANG = json.loads(open(PATH + 'lang/' + CONFIG['Lang'] + '.json'
                       ).read())

MESSAGE_LOCK = False

message_list = json.loads(open(PATH + 'data.json', 'r').read())

PREFERENCE_LOCK = False

preference_list = json.loads(open(PATH + 'preference.json', 'r').read())


def save_data():
    global MESSAGE_LOCK
    while MESSAGE_LOCK:
        time.sleep(0.05)
    MESSAGE_LOCK = True
    f = open(PATH + 'data.json', 'w')
    f.write(json.dumps(message_list))
    f.close()
    MESSAGE_LOCK = False


def save_preference():
    global PREFERENCE_LOCK
    while PREFERENCE_LOCK:
        time.sleep(0.05)
    PREFERENCE_LOCK = True
    f = open(PATH + 'preference.json', 'w')
    f.write(json.dumps(preference_list))
    f.close()
    PREFERENCE_LOCK = False


def save_config():
    f = open(PATH + 'config.json', 'w')
    f.write(json.dumps(CONFIG, indent=4))
    f.close()


def init_user(user):
    global preference_list
    if not str(user.id) in preference_list:
        preference_list[str(user.id)] = {}
        preference_list[str(user.id)]['notification'] = True
        preference_list[str(user.id)]['blocked'] = False
        preference_list[str(user.id)]['name'] = user.full_name
        threading.Thread(target=save_preference).start()
        return
    if not 'blocked' in preference_list[str(user.id)]:
        preference_list[str(user.id)]['blocked'] = False
    if preference_list[str(user.id)]['name'] != user.full_name:
        preference_list[str(user.id)]['name'] = user.full_name
        threading.Thread(target=save_preference).start()


updater = Updater(token=CONFIG['Token'])
dispatcher = updater.dispatcher

me = updater.bot.get_me()
CONFIG['ID'] = me.id
CONFIG['Username'] = '@' + me.username

print('Starting... (ID: ' + str(CONFIG['ID']) + ', Username: ' \
      + CONFIG['Username'] + ')')


def process_msg(bot, update):
    global message_list
    global secret
    global choose
    init_user(update.message.from_user)
    if CONFIG['Admin'] == 0:
        bot.send_message(chat_id=update.message.from_user.id,
                         text=LANG['please_setup_first'])
        return
    if update.message.from_user.id == CONFIG['Admin']:
        if update.message.reply_to_message:

            sender_id = update.message.reply_to_message.forward_from.id
            #if str(update.message.reply_to_message.message_id) in message_list:
            if sender_id:
                msg = update.message
                #sender_id = message_list[str(update.message.reply_to_message.message_id)]['sender_id']

                try:
                    #bot.send_message(chat_id=sender_id,text='ادمین انجمن به پیام شما پاسخ زیر را داد.')
                    if msg.audio:
                        bot.send_audio(chat_id=sender_id,
                                       audio=msg.audio, caption=msg.caption)
                    elif msg.document:
                        bot.send_document(chat_id=sender_id,
                                          document=msg.document,
                                          caption=msg.caption)
                    elif msg.voice:
                        bot.send_voice(chat_id=sender_id,
                                       voice=msg.voice, caption=msg.caption)
                    elif msg.video:
                        bot.send_video(chat_id=sender_id,
                                       video=msg.video, caption=msg.caption)
                    elif msg.sticker:
                        bot.send_sticker(chat_id=sender_id,
                                         sticker=update.message.sticker)
                    elif msg.photo:
                        bot.send_photo(chat_id=sender_id,
                                       photo=msg.photo[0], caption=msg.caption)
                    elif msg.text_markdown:
                        prefix ='ادمین انجمن به پیام شما پاسخ زیر را داد.'
                        prefix += '⬇️⬇️⬇️'
                        prefix +='\n'
                        bot.send_message(chat_id=sender_id,
                                         text=prefix + msg.text_markdown,
                                         parse_mode=ParseMode.MARKDOWN)
                    else:
                        bot.send_message(chat_id=CONFIG['Admin'],
                                         text=LANG['reply_type_not_supported'])
                        return
                except Exception as e:
                    if e.message \
                            == 'Forbidden: bot was blocked by the user':
                        bot.send_message(chat_id=CONFIG['Admin'],
                                         text=LANG['blocked_alert'])
                    else:
                        bot.send_message(chat_id=CONFIG['Admin'],
                                         text=LANG['reply_message_failed'])
                    return
                if preference_list[str(update.message.from_user.id)]['notification']:
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=LANG['reply_message_sent']
                                          % (preference_list[str(sender_id)]['name'],
                                             str(sender_id)),
                                     parse_mode=ParseMode.MARKDOWN)
            else:
                bot.send_message(chat_id=CONFIG['Admin'],
                                 text=LANG['reply_to_message_no_data'])
        else:
            bot.send_message(chat_id=CONFIG['Admin'],
                             text=LANG['reply_to_no_message'])
    else:
        if preference_list[str(update.message.from_user.id)]['blocked']:
            bot.send_message(chat_id=update.message.from_user.id, text=LANG['be_blocked_alert'])
            return
        if not choose:
            msg = 'لطفا ابتدا رویداد مورد نظر را انتخاب کنید.'
            bot.send_message(chat_id=update.message.chat_id,text=msg)
        else:
            if secret == -1:
                msg = 'لطفا روش ارسال را انتخاب کنید.'
                bot.send_message(chat_id=update.message.chat_id,text=msg)
            else:
                if secret == 0:
                    msg = 'شناس فرستاده!!!' + '\n' + 'برای ' + choose
                    bot.send_message(chat_id=CONFIG['Admin'], text=msg)
                    bot.forward_message(chat_id=CONFIG['Admin'],
                                              from_chat_id=update.message.chat_id,
                                              message_id=update.message.message_id)
                if secret == 1:
                    msg = 'ضایع نکن،ناشناس فرستاده:))' + '\n' + 'برای ' + choose
                    bot.send_message(chat_id=CONFIG['Admin'], text=msg)
                    bot.forward_message(chat_id=CONFIG['Admin'],
                                              from_chat_id=update.message.chat_id,
                                              message_id=update.message.message_id)

                if preference_list[str(update.message.from_user.id)]['notification']:
                    if secret:
                        bot.send_message(chat_id=update.message.from_user.id, text=LANG['message_received_notification_secret'])
                    else:
                        bot.send_message(chat_id=update.message.from_user.id, text=LANG['message_received_notification'])
        message_list[str(update.message.message_id)] = {}
        message_list[str(update.message.message_id)]['sender_id'] = update.message.from_user.id
        threading.Thread(target=save_data).start()
    pass


def button(bot, update):
    query = update.callback_query
    chat_id = query.message.chat_id
    print(query)
    if 'رویداد' in query['message']['text']:
        bot.edit_message_text(text="انتخاب شما: {}".format(query.data),
                              chat_id=chat_id, message_id=query.message.message_id)
        if query.data == 'خروج':
            exit_message = "شما خارج شدید. برای شروع مجدد "
            exit_message += " "+"start/"+" " + "را بزنید."
            bot.send_message(text=exit_message,chat_id=chat_id)
        else:
            global choose
            choose = query.data
            keyboard = [[InlineKeyboardButton("ناشناس", callback_data='ناشناس'),
                         InlineKeyboardButton("شناس", callback_data='شناس')]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            msg = 'ارسال پیام به صورت:'
            bot.send_message(text=msg, chat_id=chat_id, reply_markup=reply_markup)
    elif 'صورت' in query['message']['text']:

        bot.edit_message_text(text="انتخاب شما: {}".format(query.data),
                              chat_id=chat_id, message_id=query.message.message_id)
        msg = 'لطفا پیامتان را ارسال کنید.'
        bot.send_message(text=msg, chat_id=chat_id)
        global secret
        if query.data == 'ناشناس':
            secret = 1
        if query.data == 'شناس':
            secret = 0

    else:
        bot.edit_message_text(text="انتخاب شما: {}".format(query.data),
                              chat_id=chat_id, message_id=query.message.message_id)


def process_command(bot, update):
    init_user(update.message.from_user)
    id = update.message.from_user.id
    global CONFIG
    global preference_list
    global secret
    global choose
    command = update.message.text[1:].replace(CONFIG['Username'], ''
                                              ).lower().split()
    if command[0] == 'cancel':
        global user_id
        choose = 0
        secret = -1
        chat_id = update.message.chat_id
        exit_message = "شما خارج شدید. برای شروع مجدد "
        exit_message += " "+"start/"+" " + "را بزنید."
        bot.send_message(text=exit_message,chat_id=chat_id)

    if command[0] == 'start':
        global user_id
        choose = 0
        secret = -1
        user_id = update.message.chat_id
        bot.send_message(chat_id=update.message.chat_id,
                         text=LANG['start'])
        keyboard = [[InlineKeyboardButton("کارگاه مدیریت پروژه", callback_data='کارگاه مدیریت پروژه'),
                     InlineKeyboardButton("کارگاه پایگاه داده", callback_data='کارگاه پایگاه داده'),
                     InlineKeyboardButton("کارگاه فلاتر", callback_data='کارگاه فلاتر'),
                     InlineKeyboardButton("خروج", callback_data='خروج')]]

        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = 'لظفا رویداد مورد نظر خود را انتخاب کنید.'
        bot.send_message(text=msg, chat_id=update.message.chat_id, reply_markup=reply_markup)
    elif command[0] == 'version':
        bot.send_message(chat_id=update.message.chat_id,
                         text='Telegram Private Message Chat Bot\n'
                              + Version_Code
                              + '\nhttps://github.com/Netrvin/telegram-pm-chat-bot'
                         )
        return
    elif command[0] == 'setadmin':
        if CONFIG['Admin'] == 0:
            CONFIG['Admin'] = int(update.message.from_user.id)
            save_config()
            bot.send_message(chat_id=update.message.chat_id,
                             text=LANG['set_admin_successful'])
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=LANG['set_admin_failed'])
        return
    elif command[0] == 'togglenotification':
        preference_list[str(id)]['notification'] = \
            preference_list[str(id)]['notification'] == False
        threading.Thread(target=save_preference).start()
        if preference_list[str(id)]['notification']:
            bot.send_message(chat_id=update.message.chat_id,
                             text=LANG['togglenotification_on'])
        else:
            bot.send_message(chat_id=update.message.chat_id,
                             text=LANG['togglenotification_off'])
    elif command[0] == 'info':
        if update.message.from_user.id == CONFIG['Admin'] \
                and update.message.chat_id == CONFIG['Admin']:
            if update.message.reply_to_message:
                if str(update.message.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(update.message.reply_to_message.message_id)]['sender_id']
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=LANG['info_data']
                                          % (preference_list[str(sender_id)]['name'],
                                             str(sender_id)),
                                     parse_mode=ParseMode.MARKDOWN,
                                     reply_to_message_id=update.message.reply_to_message.message_id)
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_to_message_no_data'])
            else:
                bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_to_no_message'])
        else:
            bot.send_message(chat_id=update.message.chat_id, text=LANG['not_an_admin'])
    elif command[0] == 'ping':  # Ping~Pong!
        bot.send_message(chat_id=update.message.chat_id, text='Pong!')
    elif command[0] == 'ban':
        if update.message.from_user.id == CONFIG['Admin'] \
                and update.message.chat_id == CONFIG['Admin']:
            if update.message.reply_to_message:
                if str(update.message.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(update.message.reply_to_message.message_id)]['sender_id']
                    preference_list[str(sender_id)]['blocked'] = True
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=LANG['ban_user']
                                          % (preference_list[str(sender_id)]['name'],
                                             str(sender_id)),
                                     parse_mode=ParseMode.MARKDOWN)
                    bot.send_message(chat_id=sender_id, text=LANG['be_blocked_alert'])
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_to_message_no_data'])
            else:
                bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_to_no_message'])
        else:
            bot.send_message(chat_id=update.message.chat_id, text=LANG['not_an_admin'])
    elif command[0] == 'unban':
        if update.message.from_user.id == CONFIG['Admin'] \
                and update.message.chat_id == CONFIG['Admin']:
            if update.message.reply_to_message:
                if str(update.message.reply_to_message.message_id) in message_list:
                    sender_id = message_list[str(update.message.reply_to_message.message_id)]['sender_id']
                    preference_list[str(sender_id)]['blocked'] = False
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=LANG['unban_user']
                                          % (preference_list[str(sender_id)]['name'],
                                             str(sender_id)),
                                     parse_mode=ParseMode.MARKDOWN)
                    bot.send_message(chat_id=sender_id, text=LANG['be_unbanned'])
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_to_message_no_data'])
            elif len(command) == 2:
                if command[1] in preference_list:
                    preference_list[command[1]]['blocked'] = False
                    bot.send_message(chat_id=update.message.chat_id,
                                     text=LANG['unban_user']
                                          % (preference_list[command[1]]['name'],
                                             command[1]),
                                     parse_mode=ParseMode.MARKDOWN)
                    bot.send_message(chat_id=int(command[1]), text=LANG['be_unbanned'])
                else:
                    bot.send_message(chat_id=update.message.chat_id, text=LANG['user_not_found'])
            else:
                bot.send_message(chat_id=update.message.chat_id, text=LANG['reply_or_enter_id'])
        else:
            bot.send_message(chat_id=update.message.chat_id, text=LANG['not_an_admin'])
    else:
        bot.send_message(chat_id=update.message.chat_id, text=LANG['nonexistent_command'])


dispatcher.add_handler(MessageHandler(Filters.all
                                      & Filters.private
                                      & ~Filters.command
                                      & ~Filters.status_update,
                                      process_msg))

dispatcher.add_handler(MessageHandler(Filters.command
                                      & Filters.private, process_command))
dispatcher.add_handler(CallbackQueryHandler(button))

updater.start_polling()
print('Started')
updater.idle()
print('Stopping...')
save_data()
save_preference()
print('Data saved.')
print('Stopped.')
