from telebot.types import ReplyKeyboardMarkup
from telebot.util import quick_markup


excel_btn_text = "Открыть таблицу"
vip_user_btn_text = "VIP"
del_write_user_btn_text = "Отменить написал"
del_vip_user_btn_text = "Отменить VIP"
check_users_btn_text = "Проверить юзеров"
check_users_status_btn_text = "Проверить Статус"
write_user_btn_text = "Написал"

btn1_text = "Юзернейм"
btn2_text = "Имя"
btn3_text = "Закуп"

all_btns = (
    write_user_btn_text,
    excel_btn_text,
    vip_user_btn_text,
    del_write_user_btn_text,
    del_vip_user_btn_text,
    check_users_btn_text,
    check_users_status_btn_text,
    btn1_text,
    btn2_text,
    btn3_text,
)

admin_menu_text = 'Меню'
admin_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

btns_array = [
    [write_user_btn_text, vip_user_btn_text,],
    [check_users_btn_text, check_users_status_btn_text,],
    [btn1_text, btn2_text,],
    [excel_btn_text, btn3_text,],
    [del_write_user_btn_text, del_vip_user_btn_text,],
]
for row in btns_array:
    admin_menu_keyboard.add(
        *row,
        row_width=len(row)
    )

main_admin_menu = "Меню"

send_write_user_names_text = "Пришлите ID или юзернеймы тех кто написал"
send_vip_user_names_text = "Пришлите ID или юзернеймы тех кто вступил в vip"

send_del_write_user_names_text = "Пришлите ID или юзернеймы тех кто написал"
send_del_vip_user_names_text = "Пришлите ID или юзернеймы тех кто вступил в vip"

check_usersnames_text = "Пришлите ID или юзернеймы тех кого нужно проверить в базе"
check_usersnames_status_text = "Пришлите ID или юзернеймы тех чьи статусы нужно проверить"

check_1_text = "Пришлите ID для получения юзернеймов"
check_2_text = "Пришлите ID для получения Имя Фамилия"
check_3_text = "Пришлите ID для просмотра закупов"


cencel_btn = quick_markup(
    {"Отменить": {"callback_data": "cancel"}}
)

