# Generated by Django 3.2.2 on 2021-05-15 11:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0015_alter_test_stime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='stime',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='startTime'),
        ),
    ]