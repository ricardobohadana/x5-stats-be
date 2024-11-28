from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlayerViewSet, GameViewSet, GamePerformanceViewSet, PlayerStatisticView, StatisticView, StatisticsPerLane, ChampionStatistics, ChampionLaneStatistics

router = DefaultRouter()
router.register(r'players', PlayerViewSet)
router.register(r'games', GameViewSet)
router.register(r'performances', GamePerformanceViewSet)



urlpatterns = [
    path('', include(router.urls)),  # Include routes for ViewSets
    path('player-stats/<str:player_id>/', PlayerStatisticView.as_view(), name='player-stats'),  # Use path for APIView
    path('stats/', StatisticView.as_view(), name='stats'),
    path('lane-stats/', StatisticsPerLane.as_view(), name='lane-stats'),
    path('champions-stats/', ChampionStatistics.as_view(), name='champion-stats'),
    path('champions-lane-stats/', ChampionLaneStatistics.as_view(), name='champion-lane-stats'),
]