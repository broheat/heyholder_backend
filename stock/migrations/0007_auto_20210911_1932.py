# Generated by Django 3.1.13 on 2021-09-11 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0006_auto_20210911_1903'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='company',
            field=models.CharField(max_length=10),
        ),
    ]
