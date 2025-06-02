import telebot
from telebot.util import smart_split, antiflood
from telebot.types import Message, ChatMemberUpdated, CallbackQuery, ChatJoinRequest

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


bot = telebot.TeleBot(BOT_TOKEN, num_threads=3, parse_mode='HTML', disable_web_page_preview=True)


allowed_updates = ['message', 'chat_member', 'callback_query',]



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


def wait_user_name(message: Message, msg_id: int, tasks: int=2) -> None:
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
        args=(message, tasks)
    )
    t.start()



def update_users(message: Message, task: int) -> None:
    '''
    tasks 7 тг id - юзернейм
    tasks 8 тг id - имя фамилия 
    tasks 9 тг id - название ссылки с которой он подписался на канал - и дату подписки. 
    '''
    list_users = []
    for u in message.text.split("\n"):
        u_str = u.strip()
        if u_str and u_str not in list_users:
            list_users.append(u_str)
    users = set([user.strip() for user in message.text.split("\n") if user.strip()])
    if task <= 4:
        counter = confirm(task, users)
        bot.reply_to(message, f"Изменено юзеров: {counter}", reply_markup=admin_menu_keyboard)
    elif task == 5:
        # проверка юзеров по базе
        resp = count_users(users)
        for text in smart_split(resp):
            antiflood(
                function=bot.reply_to,
                message=message,
                text=text)
    
    elif task == 6:
        # проверка юзеров по статсусам
        resp = status_users(users)
        for text in smart_split(resp):
            antiflood(
                function=bot.reply_to,
                message=message,
                text=text)
    
    elif task == 7:
        # тг id - юзернейм
        resp = username_users(list_users)
        for text in smart_split(resp):
            antiflood(
                function=bot.reply_to,
                message=message,
                text=text)
    
    elif task == 8:
        # тг id - имя фамилия
        resp = names_users(list_users)
        for text in smart_split(resp):
            antiflood(
                function=bot.reply_to,
                message=message,
                text=text)
    
    elif task == 9:
        # тг id - название ссылки с которой он подписался на канал - и дату подписки.
        resp = links_users(list_users)
        for text in smart_split(resp):
            antiflood(
                function=bot.reply_to,
                message=message,
                text=text)
            

    

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
        text=main_admin_menu,
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
                msg_id=msg.id,
                tasks=2
            )
        elif message.text == del_write_user_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=send_del_vip_user_names_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=3
            )
        elif message.text == del_vip_user_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=send_del_vip_user_names_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=4
            )
        elif message.text == check_users_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=check_usersnames_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=5
            )
        elif message.text == check_users_status_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=check_usersnames_status_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=6
            )
        
        elif message.text == btn1_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=check_1_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=7
            )
        elif message.text == btn2_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=check_2_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=8
            )
        elif message.text == btn3_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=check_3_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=9
            )
        elif message.text == write_user_btn_text:
            # вводим юзернейм или юзерайди
            msg = bot.send_message(
                message.chat.id,
                text=send_write_user_names_text,
                reply_markup=cencel_btn
            )
            bot.register_next_step_handler_by_chat_id(
                chat_id=message.chat.id,
                callback=wait_user_name,
                msg_id=msg.id,
                tasks=1
            )

    elif message.text:
        # 
        main_menu(message)


@bot.callback_query_handler(func=is_admin)
def query_handler(call: CallbackQuery):

    chat_id = call.message.chat.id
    msg_id = call.message.id

    if call.data == "cancel":
        bot.clear_step_handler_by_chat_id(chat_id)
        bot.delete_message(chat_id, msg_id)
        main_menu(call.message)


