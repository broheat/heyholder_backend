# Generated by Django 3.1.13 on 2021-09-11 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0003_research'),
    ]

    operations = [
        migrations.RenameField(
            model_name='research',
            old_name='created_at',
            new_name='day',
        ),
    ]
