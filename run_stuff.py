import json
from wc_predict import load_data, Match, Group, Bracket, Tournament

if __name__ == '__main__':
    # df = load_data()
    # print(df)
    # print(sorted(set(df.loc[:, 'home_team'])))

    # grp = Group("A", ["NL", "Qatar", "Ecuador", "Senegal"])
    # grp.fill_score("A2", 1, 1)
    # grp.fill_score("A3", 2, 0)
    # grp.fill_score("A4", 0, 2)
    # grp.fill_score("A5", 1, 3)
    # for game in grp:
    #     print(game)
    
    # grp.calculate_standings()
    # print(grp.standings)
    # print(grp.group_order)

    groups = json.load(open('wc_predict/data/poules.json', 'r'))
    bracket_format = json.load(open('wc_predict/data/bracket_format.json', 'r'))

    tourney = Tournament(groups, bracket_format)

    for grp in tourney.groups.values():
        print(grp)

    print(tourney.get_games())

    tourney.fill_ro16()
    print(tourney.get_games())
    for match in tourney.ro16.values():
        print(match)
    
    tourney.fill_quarters()
    print(tourney.get_games())
    for match in tourney.quarters.values():
        print(match)

    tourney.fill_semis()
    print(tourney.get_games())
    for match in tourney.semis.values():
        print(match)

    tourney.fill_finals()
    print(tourney.get_games())
    for match in tourney.finals.values():
        print(match)