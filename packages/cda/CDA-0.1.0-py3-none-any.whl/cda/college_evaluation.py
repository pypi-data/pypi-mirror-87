from .college_scorecard import CollegeData

class CollegeEvaluation():

    def __init__(self):
        self._data = CollegeData().get_evaluation_metrics()

    def export_data(self, path='evaluation_data.csv'):
        self._data.to_csv(path, index=False)
