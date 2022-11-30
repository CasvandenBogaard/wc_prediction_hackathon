import sys
import pytest
import numpy as np
import pandas as pd

sys.path.append('../wc_predict/')
from wc_predict.runner import TournamentRunner
from wc_predict.tournament import Tournament


@pytest.fixture
def dummy_model():

    class DummyModel:

        def predict(self, df):
            df.loc[:, 'home_goals'] = 1
            df.loc[:, 'away_goals'] = 0
            return df

    return DummyModel()

@pytest.fixture
def float_model():

    class FloatModel:

        def predict(self, df):
            df.loc[:, 'home_goals'] = np.random.random(size=len(df)) * 3
            df.loc[:, 'away_goals'] = np.random.random(size=len(df)) * 3
            return df

    return FloatModel()

@pytest.fixture
def game_df():
    records = [
        ('G1', 'A', 'B'),
        ('G2', 'C', 'D'),
        ('G3', 'A', 'C'),
        ('G4', 'B', 'D'),
    ]
    df = pd.DataFrame.from_records(records)
    df.columns = ['match_id', 'home_team', 'away_team']
    df = df.set_index('match_id')
    return df


def test_check_transform_warns_on_wrong_dtype(float_model, game_df):
    preds = float_model.predict(game_df)
    with pytest.warns():
        TournamentRunner._check_and_transform(preds)

def test_check_transform_errors_on_missing_column(float_model, game_df):
    preds1 = float_model.predict(game_df)
    preds2 = float_model.predict(game_df)

    with pytest.raises(ValueError):
        preds1.drop(['home_goals'], axis=1, inplace=True)
        TournamentRunner._check_and_transform(preds1)

    with pytest.raises(ValueError):
        preds2.drop(['away_goals'], axis=1, inplace=True)
        TournamentRunner._check_and_transform(preds2)

def test_check_transform_warns_and_raises_on_none(float_model, game_df):
    preds = float_model.predict(game_df)
    preds.loc['home_goals', 'G1'] = None
    with pytest.warns():
        with pytest.raises(ValueError):
            TournamentRunner._check_and_transform(preds)