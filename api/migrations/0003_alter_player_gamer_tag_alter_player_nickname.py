# Generated by Django 5.1.3 on 2024-11-24 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_game_gold_blue_game_gold_red_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='gamer_tag',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='nickname',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
