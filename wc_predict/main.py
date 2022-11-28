import os
import json
import pandas as pd
from .tournament import Tournament

def load_data():
    def _preprocess(df):
        df.loc[:, 'home_score'] = df.loc[:, 'home_score'].astype(pd.Int8Dtype())
        df.loc[:, 'away_score'] = df.loc[:, 'away_score'].astype(pd.Int8Dtype())
        df = df[df.loc[:, 'date'] < '2022-11-20']
        return df

    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'results.csv'))
    df = _preprocess(df)
    return df


def setup_tournament():
    groups = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'poules.json'), 'r'))
    bracket_format = json.load(open(os.path.join(os.path.dirname(__file__), 'data', 'bracket_format.json'), 'r'))

    return Tournament(groups, bracket_format)
