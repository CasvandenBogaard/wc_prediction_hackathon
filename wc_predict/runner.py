import warnings
import pandas as pd

class TournamentRunner:

    def __init__(self, tournament):
        self.tournament = tournament
    
    def predict(self, group_phase_model, ko_phase_model=None):
        self.group_phase_model = group_phase_model
        if ko_phase_model is None:
            self.ko_phase_model = group_phase_model
        else:
            self.ko_phase_model = ko_phase_model
        self._run_tournament()
    
    def _run_tournament(self):
        is_next_round = True
        while is_next_round:
            self._predict_stage()
            is_next_round = self.tournament.fill_next_stage()

    def _predict_stage(self):
        if self.tournament.stage == self.tournament.STAGE.GROUPS:
            model = self.group_phase_model
        else:
            model = self.ko_phase_model
        games_to_predict = self.tournament.get_games()
        predictions = model.predict(games_to_predict)
        predictions = self._check_and_transform(predictions)
        self.tournament.score_games(predictions)
    
    @staticmethod
    def _check_and_transform(preds):
        
        try:
            preds = preds.loc[:, ['home_goals', 'away_goals']]
        except:
            raise ValueError("Predict method must return a dataframe with columns ('home_goals', 'away_goals'), got {}".format(list(preds)))
        
        for col in list(preds):
            if not pd.api.types.is_integer_dtype(preds.loc[:, col]):
                warnings.warn("Predicted number of goals is not integer, trying to convert...")
                try:
                    preds.loc[:, col] = preds.loc[:, col].astype(int)
                except:
                    raise ValueError("Can't convert prediction to integer.")
        
        return preds