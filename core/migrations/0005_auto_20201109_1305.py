# Generated by Django 3.1.3 on 2020-11-09 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20201108_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='start_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
