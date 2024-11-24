from django.core.management.base import BaseCommand

import telebot
from telebot.util import smart_split, antiflood
from telebot.types import Message, ChatMemberUpdated, CallbackQuery, ChatInviteLink, ChatJoinRequest

from datetime import datetime
from threading import Thread
from time import sleep

import logging

from bot.bot.texts import *
from bot.bot.databaser import *
from linker.settings import BOT_TOKEN, ADMINS, CHANNEL_ID, TABLE_URL


logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    filemode='a',
    format="%(asctime)s %(funcName)s %(levelname)s %(message)s")


bot = telebot.TeleBot(BOT_TOKEN, num_threads=10, parse_mode='HTML', disable_web_page_preview=True)


allowed_updates = ['message', 'chat_member', 'callback_query', "chat_join_request",]



def is_admin(message: Message) -> bool:
    '''
    проверка админ или нет
    '''
    return message.from_user.id in ADMINS 


def is_target_channel(chat_member: ChatMemberUpdated|ChatJoinRequest) -> bool:
    '''
    возвращает тру если канал тот за которым следим
    '''
    return chat_member.chat.id == CHANNEL_ID


def rm_btns(chat_id: int, msg_id: int) -> None:
    '''
    '''
    try:
        bot.edit_message_reply_markup(chat_id, msg_id, reply_markup=None)
    except:
        pass


def wait_user_name(message: Message, msg_id: int) -> None:
    '''
    ждем ввода юзернеймов для подтверждения ВИП
    '''
    user_name = message.text
    
    rm_btns(message.chat.id, msg_id)

    if user_name is None:
        return
    if user_name.startswith("/start"):
        main_menu(message)
        return
    if user_name in all_btns:
        admin_btn(message)
        return
    
    t = Thread(
        target=update_users,
        args=(message, 2)
    )
    t.start()



def update_users(message: Message, task: int) -> None:
    '''
    '''
    users = set([user.strip() for user in message.text.split("\n") if user.strip()])
    counter = confirm(task, users)

    bot.reply_to(message, f"Добавлено юзеров: {counter}", reply_markup=admin_menu_keyboard)
    

@bot.chat_member_handler(func=is_target_channel)
def new_group_member(chat_member: ChatMemberUpdated) -> None:
    '''
    если юзер вступает в группу по ссылке
    '''
    from_user = chat_member.new_chat_member.user
    status = chat_member.new_chat_member.status
    if status == "member":
        logging.info(f"New member {from_user.id}")
        
        if chat_member.invite_link is not None:
            link = get_or_create_link(chat_member.invite_link)
            user = get_or_create(from_user)
            add_to_base_table(user, link)



@bot.message_handler(
        commands=['start'],
        chat_types=['private'],
        func=is_admin)
def main_menu(message: Message) -> None:
    '''
    отправляем ексель с подписчиками
    '''

    bot.send_message(
        message.chat.id,
        text=send_write_user_names_text,
        reply_markup=admin_menu_keyboard)


@bot.message_handler(
        chat_types=['private'],
        func=is_admin)
def admin_btn(message: Message) -> None:
    '''
    отправляем ексель с подписчиками
    '''

    if message.text in all_btns:
        bot.clear_step_handler_by_chat_id(message.chat.id)

        if message.text == excel_btn_text:
            text = TABLE_URL
            bot.send_message(
                message.chat.id,
                text=text,
                reply_markup=admin_menu_keyboard)
        
        elif message.text == vip_user_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=send_vip_user_names_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id
            )

    elif message.text:
        # 
        t = Thread(
            target=update_users,
            args=(message, 1)
        )
        t.start()


@bot.callback_query_handler(func=is_admin)
def query_handler(call: CallbackQuery):

    chat_id = call.message.chat.id
    msg_id = call.message.id

    if call.data == "cancel":
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.delete_message(chat_id, msg_id)
        main_menu(call.message)


