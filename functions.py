import pandas as pd
import datetime
import math
players_arr = []
games_df = pd.read_csv('games_table.csv', sep=',', encoding='utf-8-sig')


def get_players():
    players = pd.read_csv('players_table.csv', sep=',', encoding='utf-8-sig')

    for i, row in players.iterrows():
        p = {
            "name": row['name'],
            "rank": row['rank'],
            "club": row['club'],
            "category": row['category'],
            "points": row['points'],
            "id": row['id'],
        }
        players_arr.append(p)
        if (i == 199):
            break
    return {"players_arr": players_arr}


def get_wins_history(vs_df, date, p1_id, p2_id):
    try:
        vs_df = vs_df[vs_df['date'] < date].copy()
        vs_df.drop_duplicates('match_id', inplace=True)
        p1 = {"id": int(p1_id)}
        p2 = {"id": int(p2_id)}
        p1_wins = 0
        p2_wins = 0
        p1['wins'] = len(vs_df[vs_df['winner_id'] == p1['id']])
        p2['wins'] = len(vs_df[vs_df['winner_id'] == p2['id']])
        return p1, p2

    except:
        p1 = {"wins": 0, "id": 0}
        p2 = {"wins": 0, "id": 0}
        return p1, p2


def get_vs_df(p1, p2):
    games_df.drop_duplicates('match_id', inplace=True)
    df = games_df[(games_df['p1_id'] == p1) | (games_df['p2_id'] == p1)]
    df = df[(df['p1_id'] == p2) | (df['p2_id'] == p2)]

    return df


def get_player_form(player_id, date, match_id):
    form = 0
    try:
        datetime_object = datetime.datetime.strptime(date, '%Y-%m-%d')
        start = datetime_object - datetime.timedelta(days=14)
        end = datetime_object
        date_time_start = start.strftime("%Y-%m-%d")
        date_time_end = end.strftime("%Y-%m-%d")
        temp_df = games_df[games_df['date'] <= date_time_end]
        temp_df.drop_duplicates('match_id', inplace=True)
        temp_df = temp_df[temp_df['date'] >= date_time_start]
        temp_df = temp_df[temp_df['match_id'] != match_id]
        temp_df = temp_df[(temp_df['p1_id'] == player_id) |
                          (temp_df['p2_id'] == player_id)]
        for j, row in temp_df.iterrows():
            form += row['p1_points_gained'] if row['p1_id'] == player_id else row['p2_points_gained']
    except:
        pass
    return form


def create_match(p1_id, p2_id):
    #x = datetime.datetime.now()
    #now_date = f'{x.year}-{x.month}-{x.day}'
    now_date = '2022-01-05'
    players = pd.read_csv('players_table.csv', sep=',', encoding='utf-8-sig')

    to_df = {"diff": [], "p1_prevwins": [],
             "p2_prevwins": [], "p1_form": [], "p2_form": []}
    diff = players[players['id'] == int(
        p1_id)]['points'].values[0] - players[players['id'] == int(p2_id)]['points'].values[0]
    vs_df = get_vs_df(int(p1_id), int(p2_id))
    pwin1, pwin2 = get_wins_history(
        vs_df, now_date, p1_id, p2_id)
    p1_prevwins = pwin1['wins'] if pwin1['id'] == int(p1_id) else pwin2['wins']
    p2_prevwins = pwin2['wins'] if pwin2['id'] == int(p2_id) else pwin1['wins']
    p1_form = get_player_form(int(p1_id), now_date, 0)
    p2_form = get_player_form(int(p2_id), now_date, 0)
    to_df['diff'].append(math.floor(diff))
    to_df['p1_prevwins'].append(p1_prevwins)
    to_df['p2_prevwins'].append(p2_prevwins)
    to_df['p1_form'].append(p1_form)
    to_df['p2_form'].append(p2_form)
    return pd.DataFrame.from_dict(to_df)


def get_player_row(player_id):
    players = pd.read_csv('players_table.csv', sep=',', encoding='utf-8-sig')
    player = players[players['id'] == int(player_id)]
    return player.to_dict()
