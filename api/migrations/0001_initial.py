# Generated by Django 5.1.3 on 2024-11-23 18:59

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('winning_team', models.CharField(choices=[('blue', 'Blue'), ('red', 'Red')], max_length=10)),
                ('duration', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nickname', models.CharField(max_length=100)),
                ('gamer_tag', models.CharField(max_length=100)),
                ('lane', models.CharField(choices=[('top', 'Top'), ('jungle', 'Jungle'), ('mid', 'Mid'), ('marksman', 'Marksman'), ('support', 'Support')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='GamePerformance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('champion_id', models.PositiveIntegerField()),
                ('game_lane', models.CharField(choices=[('top', 'Top'), ('jungle', 'Jungle'), ('mid', 'Mid'), ('marksman', 'Marksman'), ('support', 'Support')], max_length=20)),
                ('team', models.CharField(choices=[('blue', 'Blue'), ('red', 'Red')], max_length=10)),
                ('kills', models.PositiveIntegerField()),
                ('deaths', models.PositiveIntegerField()),
                ('assists', models.PositiveIntegerField()),
                ('damage_dealt', models.PositiveIntegerField()),
                ('gold', models.PositiveIntegerField()),
                ('cs', models.PositiveIntegerField()),
                ('vision_score', models.PositiveIntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='api.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='performances', to='api.player')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(related_name='games', to='api.player'),
        ),
    ]
