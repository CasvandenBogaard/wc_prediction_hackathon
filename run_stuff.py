import json
import pandas as pd
from wc_predict import load_data, setup_tournament

if __name__ == '__main__':
    tourney = setup_tournament()

    df = pd.DataFrame([('A2', 0, 1), ('A3', 0, 0), ('A4', 0, 2), ('A5', 1, 3)], columns=['match_id', 'home_goals', 'away_goals']).set_index('match_id')
    tourney.score_games(df)

    print(tourney.groups['A'])
    print(tourney.groups['B'])

    tourney.fill_ro16()
    print(tourney.get_games())
    for match in tourney.ro16.values():
        print(match)
    
    # tourney.fill_quarters()
    # print(tourney.get_games())
    # for match in tourney.quarters.values():
    #     print(match)

    # tourney.fill_semis()
    # print(tourney.get_games())
    # for match in tourney.semis.values():
    #     print(match)

    # tourney.fill_finals()
    # print(tourney.get_games())
    # for match in tourney.finals.values():
    #     print(match)