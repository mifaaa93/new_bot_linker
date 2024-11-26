from telebot.types import ReplyKeyboardMarkup
from telebot.util import quick_markup


excel_btn_text = "Открыть таблицу"
vip_user_btn_text = "VIP"
del_write_user_btn_text = "Отменить написал"
del_vip_user_btn_text = "Отменить VIP"

all_btns = (
    excel_btn_text,
    vip_user_btn_text,
    del_write_user_btn_text,
    del_vip_user_btn_text,
)

admin_menu_text = 'Меню'
admin_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
admin_menu_keyboard.add(
    excel_btn_text,
    vip_user_btn_text,
    row_width=2)
admin_menu_keyboard.add(
    del_write_user_btn_text,
    del_vip_user_btn_text,
    row_width=2)

send_write_user_names_text = "Пришлите ID или юзернеймы тех кто написал"
send_vip_user_names_text = "Пришлите ID или юзернеймы тех кто вступил в vip"

send_del_write_user_names_text = "Пришлите ID или юзернеймы тех кто написал"
send_del_vip_user_names_text = "Пришлите ID или юзернеймы тех кто вступил в vip"




cencel_btn = quick_markup(
    {"Отменить": {"callback_data": "cancel"}}
)

