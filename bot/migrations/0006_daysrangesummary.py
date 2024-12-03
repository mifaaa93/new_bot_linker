# Generated by Django 5.1.3 on 2024-12-03 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_alter_link_buyer'),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysRangeSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.DateField(blank=True, default=None, null=True, verbose_name='Дата от')),
                ('date_to', models.DateField(blank=True, default=None, null=True, verbose_name='Дата до')),
            ],
            options={
                'verbose_name': 'Период',
                'verbose_name_plural': 'Период',
                'abstract': False,
                'unique_together': {('date_from', 'date_to')},
            },
        ),
    ]