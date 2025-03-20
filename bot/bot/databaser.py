from telebot import types
from bot.models import User, Link, BaseTable



def get_or_create(tg_user: types.User) -> User:
    '''
    создаем или получаем объект юзера
    если юзер заблокирован, то разблокируем его
    '''
    user_id = tg_user.id
    user_name = tg_user.username
    first_name = tg_user.first_name
    last_name = tg_user.last_name

    user, now_create = User.objects.get_or_create(
        user_id=user_id,
        defaults={
            "user_name": user_name,
            "first_name": first_name,
            "last_name": last_name,
        })
    
    if not now_create and (
        user.user_name != user_name or
        user.first_name != first_name):
        
        # если пользователь регестрировался ранее, то обновляем данные(если нужно)
        user.user_name = user_name
        user.first_name = first_name
        user.save(update_fields=["user_name", "first_name",])
    
    return user


def get_or_create_link(link: types.ChatInviteLink) -> Link:
    '''
    создает или возвращает уже созданную ссылку
    '''
    invite_link = link.invite_link
    name = link.name

    chat_link, now_create = Link.objects.get_or_create(
        invite_link=invite_link,
        name=name,
        )
    
    return chat_link


def add_to_base_table(user: User, link: Link) -> BaseTable:
    '''
    вносим в базу что юзер вступил в канал
    '''
    bt = BaseTable(user=user, link=link)
    bt.save()
    
    return bt


def get_user_by_username_or_id(user_name_or_id: str) -> User:
    '''
    возвращает юзера по его айди или юзернейму
    '''
    if not user_name_or_id:
        return None
    user = None
    try:
        if user_name_or_id.isnumeric():
            user_id = int(user_name_or_id)
            user = User.objects.get(user_id=user_id)
        else:
            user_name = user_name_or_id.replace("@", '')
            user = User.objects.get(user_name=user_name)
    except Exception as e:
        pass
    return user


def turn_on_write(user: User) -> None:
    '''
    отмечаем что юзер написал на последней строке
    '''
    if not BaseTable.objects.filter(user=user, write=True).exists():
        last_row = BaseTable.objects.filter(user=user).last()
        if last_row is not None:
            last_row.make_write(True)


def turn_off_write(user: User) -> None:
    '''
    '''
    rows = BaseTable.objects.filter(user=user)
    for row in rows:
        row.make_write(False)



def turn_on_join_VIP(user: User) -> None:
    '''
    проверка если вступил в вип еще нету то отмечаем на последней дате
    '''
    if not BaseTable.objects.filter(user=user, join_chat=True).exists():
        last_row = BaseTable.objects.filter(user=user).last()
        if last_row is not None:
            last_row.make_join_VIP(True)


def turn_off_join_VIP(user: User) -> None:
    '''
    '''
    rows = BaseTable.objects.filter(user=user)
    for row in rows:
        row.make_join_VIP(False)


def confirm(task: int, users: set[str]) -> int:
    '''
    если task == 1 обновляем возле последней записи с юзером, что он написал
    если task == 2 обновляем везде для юзера что он вступил в ВИП
    если task == 3 обновляем для юзера что он написал False
    если task == 4 обновляем везде для юзера что он вступил в ВИП False
    '''
    counter = 0
    for user_name_or_id in users:
        user = get_user_by_username_or_id(user_name_or_id)
        if user is not None:
            if task == 1:
                turn_on_write(user)
            elif task == 2:
                turn_on_join_VIP(user)
            elif task == 3:
                turn_off_write(user)
            elif task == 4:
                turn_off_join_VIP(user)
                
            counter += 1
    
    return counter


def count_users(users: set[str]) -> str:
    '''
    '''
    res = ''
    for user_name_or_id in users:
        user = get_user_by_username_or_id(user_name_or_id)
        if user is not None:
            counter = BaseTable.objects.filter(user=user).count()
            res += f"{user_name_or_id} - {counter}\n"
        else:
            res += f"{user_name_or_id} - ❌\n"
    return res


def status_users(users: set[str]) -> str:
    '''
    '''
    res = ''
    for user_name_or_id in users:
        user = get_user_by_username_or_id(user_name_or_id)
        if user is None:
            res += f"{user_name_or_id} - ❌\n"
        else:
            w, v = '💤', '💤'
            bases = BaseTable.objects.filter(user=user)
            for b in bases:
                if b.write:
                    w = "📝"
                if b.join_chat:
                    v = "✅"
            res += f"{user_name_or_id} - {w} {v}\n"
    return res
