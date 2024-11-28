import pandas as pd
from .helpers import calculate_aggregations_values

def get_champion_statistics(performances_df: pd.DataFrame, games_df: pd.DataFrame) -> pd.DataFrame:
    full_df = pd.merge(games_df, performances_df, left_on='id', right_on='game_id')
    aggregated_df = calculate_aggregations_values(full_df, ['champion_id'])
    return aggregated_df

def get_champion_lane_statistics(performances_df: pd.DataFrame, games_df: pd.DataFrame) -> pd.DataFrame:
    full_df = pd.merge(games_df, performances_df, left_on='id', right_on='game_id')
    aggregated_df = calculate_aggregations_values(full_df, ['champion_id', 'game_lane'])
    return aggregated_df