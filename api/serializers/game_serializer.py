from django.db import transaction
from rest_framework import serializers
from api.models.game import Game
from api.serializers.game_performance_serializer import GamePerformanceSerializer
from api.models.player import Player
from api.models.game_performance import GamePerformance

class GameSerializer(serializers.ModelSerializer):
    players = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True
    )
    game_performances = GamePerformanceSerializer(many=True, write_only=True)

    class Meta:
        model = Game
        fields = ['id', 'date', 'players', 'winning_team', 'duration', 'gold_blue', 'gold_red', 'kills_blue', 'kills_red']
        read_only_fields = ['id']  # `id` is excluded from input but included in the response
    
    def create(self, validated_data):
        # Extract players and remove from validated_data
        player_ids = validated_data.pop('players', [])
        players = Player.objects.filter(id__in=player_ids)
        
        # Ensure exactly 10 players
        if len(players) != 10:
            raise serializers.ValidationError("A game must have exactly 10 valid players.")

        # Extract game performances and remove from validated_data
        performances_data = validated_data.pop('game_performances', [])

        if (len(performances_data) != 10):
            raise serializers.ValidationError("A game must have exactly 10 performances.")
        
        # Validate that every player_id is inside performance_data only once
        performance_player_ids = [performance['player_id'] for performance in performances_data]
        if len(set(performance_player_ids)) != 10 or set(performance_player_ids) != set(player_ids):
            raise serializers.ValidationError("Each player must have exactly one performance.")
        
        with transaction.atomic():
            # Create the Game instance
            game = Game.objects.create(**validated_data)

            # Set the Many-to-Many relationship
            game.players.set(players)
            
            for performance in performances_data:
                player = players.get(id=performance['player_id'])
                GamePerformance.objects.create(game=game, player=player, **validated_data)

        return game