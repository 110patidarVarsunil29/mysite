# Generated by Django 3.0.2 on 2020-03-02 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tutorials',
            name='tutorial_published',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date published'),
        ),
    ]
