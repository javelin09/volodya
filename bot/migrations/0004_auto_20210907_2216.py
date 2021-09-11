# Generated by Django 3.2.7 on 2021-09-07 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0003_auto_20210907_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sticker',
            name='sticker',
            field=models.FileField(upload_to='stickers', verbose_name='Стикеры'),
        ),
        migrations.AlterField(
            model_name='voicemessage',
            name='voice',
            field=models.FileField(upload_to='voices', verbose_name='Голосовое сообщение'),
        ),
    ]