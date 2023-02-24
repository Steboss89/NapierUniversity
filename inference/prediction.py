from apache_beam import DoFn
from sklearn.externals import joblib
import logging 


class Predict(DoFn):
    def __init__(self):
        super().__init__()
        self.model = joblib.load("KN.joblib", "r")

    def process(self, element, *args, **kwargs):
        logger = logging.getLogger().setLevel(logging.INFO)
        prediction = self.model.predict(element)
        logger.log(f"Element {element} - Prediction {prediction}")
        yield prediction

