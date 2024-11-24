from django.contrib import admin
from api.models.game import Game
from api.models.player import Player
from api.models.game_performance import GamePerformance



# Register your models here.

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'gamer_tag', 'lane')

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('date', 'winning_team', 'duration')

@admin.register(GamePerformance)
class GamePerformanceAdmin(admin.ModelAdmin):
    list_display = ('game', 'player', 'champion_id', 'game_lane', 'team', 'kills', 'deaths', 'assists')
