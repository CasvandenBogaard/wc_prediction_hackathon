import sys
import pytest

sys.path.append('../wc_predict/')
from wc_predict.tournament import Tournament, Group, Match


class TestMatch:

    def test_setting_score(self):
        match = Match(1, 'A', 'B')
        match.fill_score(3, 0)

        assert match.score[0] == 3
        assert match.score[1] == 0
    
    def test_played_is_set(self):
        match = Match(1, 'A', 'B')
        match.fill_score(3, 0)

        assert match.score is not None
        assert match.played == True

    def test_played_match_has_winner(self):
        match = Match(1, 'A', 'B')
        match.fill_score(3, 0)

        match2 = Match(1, 'A', 'B')
        match2.fill_score(0, 2)

        assert match.winner == 'A'
        assert match2.winner == 'B'
    
    def test_tied_match_has_tiebreak_winner(self):
        match = Match(1, 'A', 'B')
        match.fill_score(1, 1)
        assert match.winner == 'A'
    
    def test_not_played_raises_error_for_winner(self):
        match = Match(1, 'A', 'B')
        assert match.score is None
        with pytest.raises(ValueError):
            match.winner


@pytest.fixture
def group_a():
    grp = Group("A", ["NL", "QA", "EC", "SE"])
    return grp

class TestGroup:

    def test_group_has_standings(self, group_a):
        assert hasattr(group_a, 'standings')

    def test_number_of_games(self, group_a):
        assert len(group_a.games) == (len(group_a.teams) * (len(group_a.teams) - 1)) / 2
    
    def test_game_uniqueness(self, group_a):
        no_games = len(group_a.games)
        unique_games = len(set(group_a.games.values()))
        assert no_games == unique_games
    
    def test_group_order_correctness(self, group_a):
        group_a.fill_score('A1', 2, 0)
        group_a.fill_score('A6', 1, 0)
        group_a.calculate_standings()
        assert group_a.group_order == ['NL', 'EC', 'SE', 'QA']

    def test_iterates_correctly(self, group_a):
        games = list(iter(group_a))
        assert games == list(group_a.games.values())