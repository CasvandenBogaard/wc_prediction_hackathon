from enum import Enum
import pandas as pd


class Match:

    def __init__(self, match_id, home_team, away_team):
        self.id = match_id
        self.home = home_team
        self.away = away_team

        self.score = None
        self.played = False
    
    @property
    def teams(self):
        return (self.home, self.away)

    @property
    def winner(self):
        if not self.played:
            # Only for debugging purposes, otherwise throw error
            # return None
            return self.home

        if self.score[0] == self.score[1]:
            # Default to home team win in case of tie in knock-out phase
            return self.home
        elif self.score[0] > self.score[1]:
            return self.home
        else:
            return self.away

    def fill_score(self, home_score, away_score):
        self.score = (home_score, away_score)
        self.played = True

    def __str__(self):
        if not self.played:
            return "{}| {} vs {}: not played yet".format(self.id, self.home, self.away)
        else:
            return "{}| {} vs {}: {}-{}".format(self.id, self.home, self.away, *self.score)


class Group:
    
    def __init__(self, group_id, teams):
        self.group_id = str(group_id)
        self.teams = teams
        self._generate_games()
        self._create_empty_standings()

    def _generate_games(self):
        self.games = {}

        n = 1
        for i, t1 in enumerate(self.teams):
            for t2 in self.teams[i+1:]:
                match_id = self.group_id + str(n)
                self.games[match_id] = Match(match_id, t1, t2)
                n += 1

    def _create_empty_standings(self):
        self.standings = {team: {'points': 0, "goal_diff": 0, "goals": 0} for team in self.teams}

    def calculate_standings(self):
        self._create_empty_standings()

        for game in self:
            if game.played:
                self._add_game_to_standings(game)

    def _add_game_to_standings(self, game):
        st = self.standings

        (t1, t2) = game.teams
        score = game.score
        st[t1]['goals'] += score[0]
        st[t1]['goal_diff'] += score[0] - score[1]
        st[t2]['goals'] += score[1]
        st[t2]['goal_diff'] += score[1] - score[0]

        if score[0] == score[1]:
            st[t1]['points'] += 1
            st[t2]['points'] += 1
        elif score[0] > score[1]:
            st[t1]['points'] += 3
        else:
            st[t2]['points'] += 3

    def fill_score(self, match_id, home_score, away_score):
        self.games[match_id].fill_score(home_score, away_score)

    @property
    def group_order(self):
        return sorted(self.teams, key=lambda x: (self.standings[x]['points'], self.standings[x]['goal_diff'], self.standings[x]['goals']), reverse=True)

    def __iter__(self):
        return iter(self.games.values())

    def __str__(self):
        return_string = "Standings in Group {}\n".format(self.group_id)
        return_string += "-"*20 + '\n'
        return_string += ' '*16 + '|Points\t|GD\t|Goals\n'
        return_string += '\n'.join(['{:15s}\t|{}\t|{}\t|{}'.format(x, self.standings[x]['points'], self.standings[x]['goal_diff'], self.standings[x]['goals']) for x in self.group_order])
        return_string += '\n'
        return return_string


class Tournament:
    STAGE = Enum("STAGE", ['GROUPS', 'RO16', 'Q', 'S', 'F'])

    def __init__(self, groups, bracket_format):
        self.groups = {group_id: Group(group_id, teams) for group_id, teams in groups.items()}
        self.bracket_format = bracket_format

        self.stage = self.STAGE.GROUPS

        self.ro16 = {}
        self.quarters = {}
        self.semis = {}
        self.finals = {}

    @property
    def winner(self):
        final = self.finals.get('F1', None)
        if final is None or not final.played:
            return None
        else:
            return final.winner

    def fill_next_stage(self):
        if self.stage == self.STAGE.F:
            return False
        elif self.stage == self.STAGE.GROUPS:
            self._fill_ro16()
        elif self.stage == self.STAGE.RO16:
            self._fill_quarters()
        elif self.stage == self.STAGE.Q:
            self._fill_semis()
        elif self.stage == self.STAGE.S:
            self._fill_finals()
        return True
        
    def _fill_ro16(self):
        for game_id, (a, b) in self.bracket_format['RO16'].items():
            t1 = self.groups[a[0]].group_order[int(a[1])-1]
            t2 = self.groups[b[0]].group_order[int(b[1])-1]
            self.ro16[game_id] = Match(game_id, t1, t2)
        self.stage = self.STAGE.RO16
        
    def _fill_quarters(self):
        for game_id, (a, b) in self.bracket_format['Q'].items():
            t1 = self.ro16[a].winner
            t2 = self.ro16[b].winner
            self.quarters[game_id] = Match(game_id, t1, t2)
        self.stage = self.STAGE.Q
        
    def _fill_semis(self):
        for game_id, (a, b) in self.bracket_format['S'].items():
            t1 = self.quarters[a].winner
            t2 = self.quarters[b].winner
            self.semis[game_id] = Match(game_id, t1, t2)
        self.stage = self.STAGE.S
        
    def _fill_finals(self):
        for game_id, (a, b) in self.bracket_format['F'].items():
            t1 = self.semis[a].winner
            t2 = self.semis[b].winner
            self.finals[game_id] = Match(game_id, t1, t2)
        self.stage = self.STAGE.F

    def get_games(self):
        if self.stage == self.STAGE.GROUPS:
            games = []
            for group in self.groups.values():
                games += [game for game in group]
        elif self.stage == self.STAGE.RO16:
            games = list(self.ro16.values())
        elif self.stage == self.STAGE.Q:
            games = list(self.quarters.values())
        elif self.stage == self.STAGE.S:
            games = list(self.semis.values())
        elif self.stage == self.STAGE.F:
            games = list(self.finals.values())
        return self._games_to_df(games)

    def score_games(self, df):
        records = df[['home_goals', 'away_goals']].to_records()
        if self.stage == self.STAGE.GROUPS:
            for game in records:
                self.groups[game[0][0]].fill_score(*game)

            for group in self.groups.values():
                group.calculate_standings()
        elif self.stage == self.STAGE.RO16:
            for game in records:
                self.ro16[game[0]].fill_score(game[1], game[2])
        elif self.stage == self.STAGE.Q:
            for game in records:
                self.quarters[game[0]].fill_score(game[1], game[2])
        elif self.stage == self.STAGE.S:
            for game in records:
                self.semis[game[0]].fill_score(game[1], game[2])
        elif self.stage == self.STAGE.F:
            for game in records:
                self.finals[game[0]].fill_score(game[1], game[2])

    def _games_to_df(self, games):
        records = [(game.id, *game.teams) for game in games]
        df = pd.DataFrame.from_records(records)
        df.columns = ['match_id', 'home_team', 'away_team']
        df = df.set_index('match_id')
        return df
