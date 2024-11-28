import pandas as pd

def aggregate_by_summing(series: pd.Series, df: pd.DataFrame, col: str):
    return series.sum() / df.loc[series.index, col].sum()

def calculate_aggregations_values(full_df: pd.DataFrame, cols: list):
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
    full_df['duration_in_mins'] = full_df['duration'] / 60
    full_df['team_damage'] = full_df.groupby(['game_id', 'team'])['damage_dealt'].transform('sum')

    # Calculate blue and red win rates separately
    blue_win_rate = full_df[full_df['team'] == 'blue'].groupby(cols)['win'].mean()
    red_win_rate = full_df[full_df['team'] == 'red'].groupby(cols)['win'].mean()


    # Group by player_id and aggregate metrics
    aggregated_df = full_df.groupby(cols).agg(
        avg_damage_share=('damage_dealt', lambda x: x.sum()/full_df.loc[x.index,'team_damage'].sum()),
        avg_gold_per_minute=('gold', lambda x: aggregate_by_summing(x, full_df, 'duration_in_mins')),
        avg_vision_score_per_minute=('vision_score', lambda x: aggregate_by_summing(x, full_df, 'duration_in_mins')),
        avg_damage_per_minute=('damage_dealt', lambda x: aggregate_by_summing(x, full_df, 'duration_in_mins')),
        avg_cs_per_minute=('cs', lambda x: aggregate_by_summing(x, full_df, 'duration_in_mins')),
        avg_kill_participation=('kill_participation', lambda x: aggregate_by_summing(x, full_df, 'team_kills')),
        avg_gold_share=('gold', lambda x: aggregate_by_summing(x, full_df, 'team_gold')),
        avg_damage_per_gold=('damage_dealt', lambda x: aggregate_by_summing(x, full_df, 'gold')),
        
        avg_vision_score=('vision_score', 'mean'),
        avg_kills=('kills', 'mean'),
        avg_deaths=('deaths', 'mean'),
        avg_assists=('assists', 'mean'),
        avg_duration=('duration', 'mean'),
        win_rate=('win', 'mean'),
        
        # drop later
        total_kills=('kills', 'sum'),
        total_deaths=('deaths', 'sum'),
        total_assists=('assists', 'sum'),
        appearances=('game_id', 'count')
    ).reset_index()

    
    # Calculate KDA
    aggregated_df['avg_kda'] = (aggregated_df['total_kills'] + aggregated_df['total_assists']) / aggregated_df['total_deaths'].replace(0, 1)
    aggregated_df = aggregated_df.drop(columns=['total_kills', 'total_deaths', 'total_assists'])

    col = cols
    if type(cols) == list:
        col = cols[0]

    # Merge blue and red win rates into the aggregated DataFrame
    aggregated_df['blue_win_rate'] = aggregated_df[col].map(blue_win_rate)
    aggregated_df['red_win_rate'] = aggregated_df[col].map(red_win_rate)

    # Replace NaN values with 0 for cases where players have no wins on a side
    aggregated_df['blue_win_rate'] = aggregated_df['blue_win_rate'].fillna(0)
    aggregated_df['red_win_rate'] = aggregated_df['red_win_rate'].fillna(0)

    # Order aggregated_df by kda
    aggregated_df = aggregated_df.sort_values(by='avg_kda', ascending=False)

    # Replace NaN values with None for cases where there was a division by 0
    aggregated_df = aggregated_df.where(pd.notnull(aggregated_df), 0)

    return aggregated_df
    