import pandas as pd

def get_games():
    game_df = pd.read_csv('..\data\game_list.csv', header=0, names=['game_symbol', 'game_name'])
    game_dict = {}
    # game_df = [{'game_symbol'
    for i, game in game_df.iterrows():
        game_dict[game['game_name'].strip()] = game['game_symbol'].strip()
    return game_dict


