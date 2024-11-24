from rest_framework import serializers
from api.models.game import Game
from api.models.game_performance import GamePerformance
from api.models.player import Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'
        read_only_fields = ['id']  # `id` is excluded from input but included in the response


class GameSerializer(serializers.ModelSerializer):
    players = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True  # Only used for input
    )
    # player_objects = serializers.SerializerMethodField()  # Return full player data

    class Meta:
        model = Game
        fields = ['id', 'date', 'players', 'winning_team', 'duration', 'gold_blue', 'gold_red', 'kills_blue', 'kills_red']
        read_only_fields = ['id']  # `id` is excluded from input but included in the response
    
    def get_player_objects(self, obj: Game):
        # Serialize full player data for the response
        return [player.id for player in obj.players.all()]

    def create(self, validated_data):
        # Extract players and remove from validated_data
        player_ids = validated_data.pop('players', [])
        players = Player.objects.filter(id__in=player_ids)

        # Ensure exactly 10 players
        if len(players) != 10:
            raise serializers.ValidationError("A game must have exactly 10 valid players.")

        # Create the Game instance
        game = Game.objects.create(**validated_data)

        # Set the Many-to-Many relationship
        game.players.set(players)

        return game


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
