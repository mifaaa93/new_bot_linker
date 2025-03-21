# Generated by Django 5.1.3 on 2025-01-21 16:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_alter_daysrangesummary_unique_together_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='LinkFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ads_price', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Цена Рекламы')),
                ('date', models.DateField(blank=True, default=None, null=True, verbose_name='Дата')),
                ('subs', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Подписалось')),
                ('write', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Написало')),
                ('join_vip', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Вступило в VIP')),
                ('subs_price', models.FloatField(blank=True, default=None, editable=False, null=True, verbose_name='Цена ПДП')),
                ('write_price', models.FloatField(blank=True, default=None, editable=False, null=True, verbose_name='Цена Написало')),
                ('join_vip_price', models.FloatField(blank=True, default=None, editable=False, null=True, verbose_name='Цена Вступило в VIP')),
                ('buyer', models.ForeignKey(blank=True, default=None, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bot.buyer', verbose_name='Закупщик')),
                ('invite_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.link', unique=True, verbose_name='Ссылка')),
            ],
            options={
                'verbose_name': 'Ссылка (сорт)',
                'verbose_name_plural': 'Ссылки (сорт)',
                'abstract': False,
            },
        ),
    ]
