# Generated by Django 3.2.2 on 2021-05-19 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0027_auto_20210519_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='u_p',
            name='status',
        ),
    ]