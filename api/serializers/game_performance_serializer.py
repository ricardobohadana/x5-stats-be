from api.models.game_performance import GamePerformance
from rest_framework import serializers

from api.models.game import Game
from api.models.player import Player

class GamePerformanceSerializer(serializers.ModelSerializer):
    game_id = serializers.UUIDField()
    player_id = serializers.UUIDField()

    class Meta:
        model = GamePerformance
        fields = [
            'id',  # Read-only
            'game_id',
            'player_id',
            'champion_id',
            'game_lane',
            'team',
            'kills',
            'deaths',
            'assists',
            'damage_dealt',
            'gold',
            'cs',
            'vision_score',
        ]
        read_only_fields = ['id']  # `id` is excluded from input but included in the response

    def get_game_id(self, obj: GamePerformance):
        return obj.game.id

    def get_player_id(self, obj: GamePerformance):
        return obj.player.id        

    def create(self, validated_data):
        # Extract `gameId` and `playerId`
        game_id = validated_data.pop('game_id')
        player_id = validated_data.pop('player_id')

        # Get the corresponding Game and Player objects
        game = Game.objects.get(id=game_id)
        player = Player.objects.get(id=player_id)

        # Create the GamePerformance instance
        game_performance = GamePerformance.objects.create(game=game, player=player, **validated_data)
        return game_performance
