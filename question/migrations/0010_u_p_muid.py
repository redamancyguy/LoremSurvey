# Generated by Django 3.2.2 on 2021-05-15 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0009_auto_20210515_0531'),
    ]

    operations = [
        migrations.AddField(
            model_name='u_p',
            name='muid',
            field=models.BigIntegerField(default=None),
        ),
    ]
