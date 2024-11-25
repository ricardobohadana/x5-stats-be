import pandas as pd
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.game import Game
from api.models.player import Player
from api.models.game_performance import GamePerformance
from api.statistics.general import get_statistics_from_game_and_performance
from api.statistics.per_lane import get_statistics_from_game_and_performance_per_game_lane
from .serializers import PlayerSerializer, GameSerializer, GamePerformanceSerializer

class PlayerViewSet(ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class GameViewSet(ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GamePerformanceViewSet(ModelViewSet):
    queryset = GamePerformance.objects.all()
    serializer_class = GamePerformanceSerializer


class StatisticView(APIView):
    include_root_view = True

    def get(self, request, *agrs, **kwargs):
        games = Game.objects.all()
        games_data = GameSerializer(games, many=True).data
        games_df = pd.DataFrame(games_data)

        performances = GamePerformance.objects.all()
        performances_data = GamePerformanceSerializer(performances, many=True).data
        perf_df = pd.DataFrame(performances_data)

        if games_df.empty or perf_df.empty:
            return Response([], status=200)
        
        aggregated_df = get_statistics_from_game_and_performance(perf_df, games_df)

        return Response(aggregated_df.to_dict(orient='records'))


class PlayerStatisticView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract query parameters for filtering if provided
        player_id = kwargs.get('player_id')
        
        if not player_id:
            return Response({"error": "Player ID is required"}, status=400)
        
        try:
            player = Player.objects.get(id=player_id)
        except Player.DoesNotExist:
            return Response({"error": "Player not found"}, status=404)
        
        games = Game.objects.filter(players=player)
        games_data = GameSerializer(games, many=True).data
        games_df = pd.DataFrame(games_data)

        performances = GamePerformance.objects.filter(player=player)
        performances_data = GamePerformanceSerializer(performances, many=True).data
        perf_df = pd.DataFrame(performances_data)

        if games_df.empty or perf_df.empty:
            return Response([], status=200)
        
        # Perform data aggregation
        aggregated_df = get_statistics_from_game_and_performance_per_game_lane(perf_df, games_df)

        return Response(aggregated_df.to_dict(orient='records'))


class StatisticsPerLane(APIView):
    def get(self, request, *args, **kwargs):
        
        games = Game.objects.all()
        games_data = GameSerializer(games, many=True).data
        games_df = pd.DataFrame(games_data)

        performances = GamePerformance.objects.all()
        performances_data = GamePerformanceSerializer(performances, many=True).data
        perf_df = pd.DataFrame(performances_data)

        aggregated_df = get_statistics_from_game_and_performance_per_game_lane(perf_df, games_df)

        if games_df.empty or perf_df.empty:
            return Response([], status=200)
        
        lanes = aggregated_df['game_lane'].unique()

        result = {}
        for lane in lanes:
            lane_df = aggregated_df[aggregated_df['game_lane'] == lane]
            result[lane] = lane_df.to_dict(orient='records')

        return Response(result, status=200)