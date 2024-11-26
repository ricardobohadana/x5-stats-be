import pandas as pd
from api.statistics.helpers import calculate_aggregations_values


def get_statistics_from_game_and_performance(game_performances_df, game_df):
    # concatenate the two dataframes
    full_df = pd.merge(game_df, game_performances_df, left_on='id', right_on='game_id')
    # concatenate the two dataframes
    full_df = pd.merge(game_df, game_performances_df, left_on='id', right_on='game_id')
    agg_cols = 'player_id'

    return calculate_aggregations_values(full_df, agg_cols)

