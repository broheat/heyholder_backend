# Generated by Django 3.1.13 on 2021-09-11 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0005_auto_20210911_1722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='research',
            name='company',
            field=models.CharField(max_length=10),
        ),
    ]
