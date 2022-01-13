from flask import Flask, request
from functions import get_players, create_match, get_player_row, get_vs_df
import numpy as np
import joblib
import pandas as pd
import json


app = Flask(__name__)
rf_model = joblib.load('rf_model.pkl')


players = get_players()


def np_encoder(object):
    if isinstance(object, np.generic):
        return object.item()


@app.route('/')
@app.route('/get_players')
def get_players():
    return players


@app.route('/predict', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def predict():
    if request.method == 'POST':
        p1_id = request.get_json()['p1_id']
        p2_id = request.get_json()['p2_id']
        game = create_match(p1_id, p2_id)
    score = rf_model. predict(game)
    result = game.to_dict()
    print(result)
    if (list(result['diff'].values())[0] >= 80) & (score[0] == 0):
        result['is_p1_win'] = {0: 1}
    else:
        result['is_p1_win'] = {0: score[0]}

    return json.dumps(result, default=np_encoder)


@app.route('/get_player', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def get_player():
    player_id = request.form.get('player_id')
    print(request.form)
    return get_player_row(player_id)


@app.route('/get_vs_df', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def get_vs():
    p1_id = request.get_json()['p1_id']
    p2_id = request.get_json()['p2_id']

    df = get_vs_df(int(p1_id), int(p2_id))
    return df.to_json()
