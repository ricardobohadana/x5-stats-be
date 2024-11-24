from django.db import models
from api.models.player import Player, Lane
from api.models.game import Game, Team
import uuid

class GamePerformance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name="performances")
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="performances")
    champion_id = models.PositiveIntegerField()
    game_lane = models.CharField(max_length=20, choices=Lane.choices)
    team = models.CharField(max_length=10, choices=Team.choices)
    kills = models.PositiveIntegerField()
    deaths = models.PositiveIntegerField()
    assists = models.PositiveIntegerField()
    damage_dealt = models.PositiveIntegerField(null=True, blank=True)
    gold = models.PositiveIntegerField(null=True, blank=True)
    cs = models.PositiveIntegerField(null=True, blank=True)
    vision_score = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"Performance: {self.player.nickname} in Game {self.game.id}"
