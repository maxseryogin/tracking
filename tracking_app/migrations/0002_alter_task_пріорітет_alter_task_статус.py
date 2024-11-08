# Generated by Django 5.1.2 on 2024-10-22 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracking_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='Пріорітет',
            field=models.CharField(choices=[('low', 'Низький'), ('medium', 'Середній'), ('high', 'Високий')], default='medium', max_length=10),
        ),
        migrations.AlterField(
            model_name='task',
            name='Статус',
            field=models.CharField(choices=[('not_started', 'Не розпочато'), ('in_progress', 'В процесі'), ('completed', 'Зроблено')], default='not_started', max_length=20),
        ),
    ]
