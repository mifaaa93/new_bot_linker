# Generated by Django 5.1.3 on 2024-11-24 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('first_name', models.CharField(editable=False, max_length=64, verbose_name='Имя')),
                ('user_name', models.CharField(blank=True, default=None, editable=False, max_length=32, null=True, verbose_name='Юзернейм')),
                ('last_name', models.CharField(blank=True, default=None, editable=False, max_length=64, null=True, verbose_name='Фамилия')),
                ('registratin_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата Первого Вступления')),
            ],
            options={
                'verbose_name': 'Юзер телеграм',
                'verbose_name_plural': 'Юзер телеграм',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invite_link', models.CharField(editable=False, max_length=512, verbose_name='Ссылка')),
                ('name', models.CharField(blank=True, default=None, editable=False, max_length=256, null=True, verbose_name='Название')),
                ('ads_price', models.IntegerField(blank=True, default=None, null=True, verbose_name='Цена Рекламы')),
                ('date', models.DateField(blank=True, default=None, null=True, verbose_name='Дата')),
            ],
            options={
                'verbose_name': 'Ссылка',
                'verbose_name_plural': 'Ссылки',
                'abstract': False,
                'unique_together': {('invite_link', 'name')},
            },
        ),
        migrations.CreateModel(
            name='BaseTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='Дата Вступления')),
                ('write', models.BooleanField(default=False, verbose_name='Написал')),
                ('join_chat', models.BooleanField(default=False, verbose_name='Вступил в VIP')),
                ('link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.link', verbose_name='Ссылка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.user', verbose_name='Юзер')),
            ],
            options={
                'verbose_name': 'База',
                'verbose_name_plural': 'База',
                'abstract': False,
            },
        ),
    ]
