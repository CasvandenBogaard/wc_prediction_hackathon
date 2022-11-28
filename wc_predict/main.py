import os
import pandas as pd

def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'data', 'results.csv'))
    df = _preprocess(df)
    return df

def _preprocess(df):
    df.loc[:, 'home_score'] = df.loc[:, 'home_score'].astype(pd.Int8Dtype())
    df.loc[:, 'away_score'] = df.loc[:, 'away_score'].astype(pd.Int8Dtype())
    df = df[df.loc[:, 'date'] < '2022-11-20']
    return df


class Match:

    def __init__(self, home_team, away_team):
        self.home = home_team
        self.away = away_team

        self.score = None
    
    def fill_score(self, home_score, away_score):
        self.score = (home_score, away_score)


class Group:
    
    def __init__(self, teams):
        self.teams = teams
    
        self.games = None

    def _generate_games(self):
        pass

    @property
    def standings(self):
        return