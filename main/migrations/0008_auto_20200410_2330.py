# Generated by Django 3.0.2 on 2020-04-10 18:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20200410_2309'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usersession',
            name='is_session_active',
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='tutorial_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 10, 23, 30, 52, 382433), verbose_name='date published'),
        ),
    ]
