# Generated by Django 3.1.3 on 2020-11-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_game_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameprogress',
            name='category1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameprogress',
            name='category2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameprogress',
            name='category3',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameprogress',
            name='category4',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameprogress',
            name='category5',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gameprogress',
            name='category6',
            field=models.IntegerField(default=0),
        ),
    ]
