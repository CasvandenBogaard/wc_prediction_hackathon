import json
import numpy.random
import pandas as pd
from wc_predict import load_data, setup_tournament, TournamentRunner

if __name__ == '__main__':
    tourney = setup_tournament()

    # df = pd.DataFrame([('A2', 0, 1), ('A3', 0, 0), ('A4', 0, 2), ('A5', 1, 3)], columns=['match_id', 'home_goals', 'away_goals']).set_index('match_id')
    # tourney.score_games(df)
    # print(tourney.groups['A'])
    # print(tourney.groups['B'])

    # df_games_groups = tourney.get_games()
    # groups_preds = df_games_groups.copy()
    # groups_preds.loc[:, 'home_goals'] = numpy.random.randint(3, size=len(groups_preds))
    # groups_preds.loc[: ,'away_goals'] = numpy.random.randint(3, size=len(groups_preds))
    
    # tourney.score_games(groups_preds)    
    # print(groups_preds)
    # print(tourney.groups['A'])
    # print(tourney.groups['B'])
    # print(tourney.groups['C'])


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

    runner = TournamentRunner(tourney)
    runner.predict(RandomModel())

    print(tourney.groups['A'])
    for match in tourney.ro16.values():
        print(match)
    for match in tourney.quarters.values():
        print(match)
    for match in tourney.semis.values():
        print(match)
    for match in tourney.finals.values():
        print(match)