# Generated by Django 3.2.2 on 2021-05-20 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0037_remove_u_p_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='u_p',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
