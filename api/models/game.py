from django.db import models
from django.forms import ValidationError
from api.models.player import Player
import uuid


class Team(models.TextChoices):
    BLUE = "blue", "Blue"
    RED = "red", "Red"

class Game(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateField()
    players = models.ManyToManyField(Player, related_name="games")  # 10 players
    winning_team = models.CharField(max_length=10, choices=Team.choices)
    duration = models.PositiveIntegerField()  # in seconds
    gold_blue = models.PositiveIntegerField(null=True, blank=True)
    gold_red = models.PositiveIntegerField(null=True, blank=True)
    kills_blue = models.PositiveIntegerField(null=True, blank=True)
    kills_red = models.PositiveIntegerField(null=True, blank=True)
    # season = models.PositiveIntegerField(null=False, blank=True, default=1)

    def __str__(self):
        return f"Game on {self.date} - {self.winning_team}"

    def save(self, *args, **kwargs):
        # Call clean method before saving
        self.full_clean()
        super().save(*args, **kwargs)
