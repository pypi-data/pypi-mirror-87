from .college_scorecard.api import MetaData

class DatasetInfo():

    def __init__(self):
        self._data = MetaData()

    def show_attributes(self):
        print('Attributes:\n', self._data.get_attribute_names())
