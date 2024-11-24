from django.db import models
import uuid

class Lane(models.TextChoices):
    TOP = "top", "Top"
    JG = "jungle", "Jungle"
    MID = "mid", "Mid"
    ADC = "marksman", "Marksman"
    SUP = "support", "Support"

class Player(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nickname = models.CharField(max_length=100, unique=True)
    gamer_tag = models.CharField(max_length=100, unique=True)
    lane = models.CharField(max_length=20, choices=Lane.choices)

    def __str__(self):
        return self.nickname
