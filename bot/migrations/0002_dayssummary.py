# Generated by Django 5.1.3 on 2024-11-25 08:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysSummary',
            fields=[
            ],
            options={
                'verbose_name': 'Дни',
                'verbose_name_plural': 'Дни',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bot.basetable',),
        ),
    ]
