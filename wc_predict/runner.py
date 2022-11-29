

class TournamentRunner:

    def __init__(self, tournament):
        self.tournament = tournament
    
    def predict(self, model):
        self.model = model
        self._run_tournament()
    
    def _run_tournament(self):
        is_next_round = True
        while is_next_round:
            self._predict_stage()
            is_next_round = self.tournament.fill_next_stage()

    def _predict_stage(self):
        games_to_predict = self.tournament.get_games()
        predictions = self.model.predict(games_to_predict)
        self.tournament.score_games(predictions)