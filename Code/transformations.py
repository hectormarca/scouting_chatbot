import pandas as pd

def union_events(df_list):

    result = pd.DataFrame()

    for df in df_list:

        result = pd.concat(result, df, ignore_index=True)

    return result

def filter_by_player(df, players, player_column='player'):

    df_filtered = df[df[player_column].isin(players)]
    return df_filtered

