import json
import numpy.random
import pandas as pd
from wc_predict import load_data, setup_tournament, TournamentRunner

if __name__ == '__main__':
    tourney = setup_tournament()

    class DummyModel:

        def predict(self, df):
            df.loc[:, 'home_goals'] = 1
            df.loc[:, 'away_goals'] = 0
            return df

    class RandomModel:

        def predict(self, df):
            df.loc[:, 'home_goals'] = numpy.random.randint(3, size=len(df))
            df.loc[:, 'away_goals'] = numpy.random.randint(3, size=len(df))
            return df

    class FloatRandomModel:

        def predict(self, df):
            df.loc[:, 'home_goals'] = numpy.random.random(size=len(df)) * 3
            df.loc[:, 'away_goals'] = numpy.random.random(size=len(df)) * 3
            return df

    runner = TournamentRunner(tourney)
    runner.predict(RandomModel(), FloatRandomModel())

    print(tourney)