import sys
import pytest

sys.path.append('../wc_predict/')
from wc_predict.runner import TournamentRunner
from wc_predict.tournament import Tournament


@pytest.fixture
def get_dummy_model():

    class DummyModel:

        def __init__():
            pass

        def predict(self, df):
            df.loc[:, 'home_goals'] = 1
            df.loc[:, 'away_goals'] = 0
            return df

    return DummyModel()
