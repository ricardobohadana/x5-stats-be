import pandas as pd
from api.statistics.helpers import aggregate_by_summing


def get_statistics_from_game_and_performance_per_game_lane(game_performances_df, game_df):
    # concatenate the two dataframes
    full_df = pd.merge(game_df, game_performances_df, left_on='id', right_on='game_id')

    # Add calculated columns
    full_df['kda'] = (full_df['kills'] + full_df['assists']) / full_df['deaths'].replace(0, 1)  # Avoid division by zero
    full_df['gold_per_minute'] = full_df['gold'] / (full_df['duration'] / 60)
    full_df['damage_per_minute'] = full_df['damage_dealt'] / (full_df['duration'] / 60)
    full_df['cs_per_minute'] = full_df['cs'] / (full_df['duration'] / 60)
    full_df['win'] = full_df['winning_team'] == full_df['team']
    full_df['team_kills'] = full_df.apply(lambda row: row['kills_blue'] if row['team'] == 'blue' else row['kills_red'], axis=1)
    full_df['kill_participation'] = (full_df['kills'] + full_df['assists'])
    full_df['team_gold'] = full_df.apply(lambda row: row['gold_blue'] if row['team'] == 'blue' else row['gold_red'], axis=1)
    full_df['gold_share'] = full_df['gold'] / full_df['team_gold']

    # Group by player_id and aggregate metrics
    aggregated_df = full_df.groupby(['player_id', 'game_lane']).agg(

        avg_gold_per_minute=('gold_per_minute', lambda x: aggregate_by_summing(x, full_df, 'duration')),
        avg_vision_score=('vision_score', lambda x: aggregate_by_summing(x, full_df, 'duration')),
        avg_damage_per_minute=('damage_per_minute', lambda x: aggregate_by_summing(x, full_df, 'duration')),
        avg_cs_per_minute=('cs_per_minute', lambda x: aggregate_by_summing(x, full_df, 'duration')),
        avg_kill_participation=('kill_participation', lambda x: aggregate_by_summing(x, full_df, 'team_kills')),
        avg_gold_share=('gold', lambda x: aggregate_by_summing(x, full_df, 'team_gold')),

        avg_kills=('kills', 'mean'),
        avg_deaths=('deaths', 'mean'),
        avg_assists=('assists', 'mean'),
        avg_duration=('duration', 'mean'),
        win_rate=('win', 'mean'),
        
        # drop later
        total_kills=('kills', 'sum'),
        total_deaths=('deaths', 'sum'),
        total_assists=('assists', 'sum'),
    ).reset_index()

    
    # Calculate KDA
    aggregated_df['avg_kda'] = (aggregated_df['total_kills'] + aggregated_df['total_assists']) / aggregated_df['total_deaths'].replace(0, 1)
    aggregated_df = aggregated_df.drop(columns=['total_kills', 'total_deaths', 'total_assists'])

    # Calculate blue and red win rates separately
    blue_win_rate = full_df[full_df['team'] == 'blue'].groupby('player_id')['win'].mean()
    red_win_rate = full_df[full_df['team'] == 'red'].groupby('player_id')['win'].mean()

    # Merge blue and red win rates into the aggregated DataFrame
    aggregated_df['blue_win_rate'] = aggregated_df['player_id'].map(blue_win_rate)
    aggregated_df['red_win_rate'] = aggregated_df['player_id'].map(red_win_rate)

    # Replace NaN values with 0 for cases where players have no wins on a side
    aggregated_df['blue_win_rate'] = aggregated_df['blue_win_rate'].fillna(0)
    aggregated_df['red_win_rate'] = aggregated_df['red_win_rate'].fillna(0)

    # Order aggregated_df by kda
    aggregated_df = aggregated_df.sort_values(by='avg_kda', ascending=False)

    # Replace NaN values with None for cases where there was a division by 0
    aggregated_df = aggregated_df.where(pd.notnull(aggregated_df), None)

    return aggregated_df