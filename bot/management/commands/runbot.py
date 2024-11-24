from django.core.management.base import BaseCommand


from bot.bot.bot import bot, allowed_updates




class Command(BaseCommand):
    # Используется как описание команды обычно
    help = 'Just a command for launching a Telegram bot.'

    def handle(self, *args, **kwargs):

        print(f"Bot Started {bot.get_me().username}")
        bot.infinity_polling(allowed_updates=allowed_updates)
