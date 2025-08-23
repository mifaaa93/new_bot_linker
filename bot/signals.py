# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from bot.models import Admin
from bot.bot.bot import fetch_user_profile

@receiver(pre_save, sender=Admin)
def refresh_username_on_save(sender, instance: Admin, **kwargs):
    """
    Перед сохранением пробуем обновить ФИО/username из Telegram.
    Работает, только если пользователь ранее писал боту (иначе get_chat вернёт ошибку).
    """
    if not instance.user_id:
        return

    profile = fetch_user_profile(instance.user_id)
    if not profile:
        return

    # Аккуратно обновляем поля, не затирая НЕ-пустые значениями None
    if profile.get("first_name"):
        instance.first_name = profile["first_name"]
    if "last_name" in profile:  # может быть None — это ок
        instance.last_name = profile["last_name"]
    if "username" in profile:   # может быть None — это ок
        instance.user_name = profile["username"]
