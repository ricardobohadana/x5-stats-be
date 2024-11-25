import pandas as pd

def aggregate_by_summing(series: pd.Series, df: pd.DataFrame, col: str):
    return series.sum() / df.loc[series.index, col].sum()