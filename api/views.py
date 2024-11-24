import pandas as pd
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models.game import Game
from api.models.player import Player
from api.models.game_performance import GamePerformance
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
        
        # concatenate the two dataframes
        full_df = pd.merge(games_df, perf_df, left_on='id', right_on='game_id')

        # Add calculated columns
        full_df['kda'] = (full_df['kills'] + full_df['assists']) / full_df['deaths'].replace(0, 1)  # Avoid division by zero
        full_df['gold_per_minute'] = full_df['gold'] / (full_df['duration'] / 60)
        full_df['damage_per_minute'] = full_df['damage_dealt'] / (full_df['duration'] / 60)
        full_df['cs_per_minute'] = full_df['cs'] / (full_df['duration'] / 60)
        full_df['win'] = full_df['winning_team'] == full_df['team']
        full_df['kill_participation'] = (full_df['kills'] + full_df['assists']) / full_df['team_kills']

        # Group by player_id and aggregate metrics
        aggregated_df = full_df.groupby('player_id').agg(
            avg_kda=('kda', 'mean'),
            avg_gold_per_minute=('gold_per_minute', 'mean'),
            avg_vision_score=('vision_score', 'mean'),
            avg_damage_per_minute=('damage_per_minute', 'mean'),
            avg_cs_per_minute=('cs_per_minute', 'mean'),
            avg_kills=('kills', 'mean'),
            avg_deaths=('deaths', 'mean'),
            avg_assists=('assists', 'mean'),
            avg_duration=('duration', 'mean'),
            win_rate=('win', 'mean'),
            avg_kill_participation=('kill_participation', 'mean'),
        ).reset_index()

        # Calculate blue and red win rates separately
        blue_win_rate = full_df[full_df['winning_team'] == 'blue'].groupby('player_id').size() / full_df.groupby('player_id').size()
        red_win_rate = full_df[full_df['winning_team'] == 'red'].groupby('player_id').size() / full_df.groupby('player_id').size()

        # Merge blue and red win rates into the aggregated DataFrame
        aggregated_df['blue_win_rate'] = aggregated_df['player_id'].map(blue_win_rate)
        aggregated_df['red_win_rate'] = aggregated_df['player_id'].map(red_win_rate)

        # Replace NaN values with 0 for cases where players have no wins on a side
        aggregated_df['blue_win_rate'] = aggregated_df['blue_win_rate'].fillna(0)
        aggregated_df['red_win_rate'] = aggregated_df['red_win_rate'].fillna(0)

        # Order aggregated_df by kda
        aggregated_df = aggregated_df.sort_values(by='avg_kda', ascending=False)

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
        
        # concatenate the two dataframes
        full_df = pd.merge(games_df, perf_df, left_on='id', right_on='game_id')

        # Calculate the average KDA
        full_df['kda'] = (full_df['kills'] + full_df['assists']) / full_df['deaths']
        avg_kda = full_df['kda'].mean()

        # Calculate the average gold per minute
        full_df['gold_per_minute'] = full_df['gold'] / (full_df['duration'] / 60)
        avg_gold_per_minute = full_df['gold_per_minute'].mean()

        # Calculate the average vision score
        avg_vision_score = full_df['vision_score'].mean()

        # Calculate the average damage dealt per minute
        full_df['damage_per_minute'] = full_df['damage_dealt'] / (full_df['duration'] / 60)
        avg_damage_per_minute = full_df['damage_per_minute'].mean()

        # Calculate the average CS per minute
        full_df['cs_per_minute'] = full_df['cs'] / (full_df['duration'] / 60)
        avg_cs_per_minute = full_df['cs_per_minute'].mean()

        # Calculate the average kills per game
        avg_kills = full_df['kills'].mean()
        # Calculate the average deaths per game
        avg_deaths = full_df['deaths'].mean()
        # Calculate the average assists per game
        avg_assists = full_df['assists'].mean()

        # Calculate average game duration
        avg_duration = full_df['duration'].mean()

        # Calculate the average win rate
        total_games = full_df.shape[0]
        total_wins = full_df[full_df['winning_team'] == full_df['team']].shape[0]
        win_rate = total_wins / total_games

        # Calculate average win rate in blue side
        blue_wins = full_df[full_df['winning_team'] == 'blue']
        blue_win_rate = blue_wins.shape[0] / full_df.shape[0]

        # Calculate average win rate in red side
        red_wins = full_df[full_df['winning_team'] == 'red']
        red_win_rate = red_wins.shape[0] / full_df.shape[0]

        # Calculate average kill participation
        full_df['kill_participation'] = (full_df['kills'] + full_df['assists']) / full_df['team_kills']
        avg_kill_participation = full_df['kill_participation'].mean()

        return Response({
            "player_id": player_id,
            "avg_kda": avg_kda,
            "avg_gold_per_minute": avg_gold_per_minute,
            "avg_vision_score": avg_vision_score,
            "avg_damage_per_minute": avg_damage_per_minute,
            "avg_cs_per_minute": avg_cs_per_minute,
            "avg_kills": avg_kills,
            "avg_deaths": avg_deaths,
            "avg_assists": avg_assists,
            "avg_duration": avg_duration,
            "win_rate": win_rate,
            "blue_win_rate": blue_win_rate,
            "red_win_rate": red_win_rate,
            "avg_kill_participation": avg_kill_participation
        })
