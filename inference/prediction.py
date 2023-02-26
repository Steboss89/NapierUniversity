from apache_beam import DoFn
import logging 
import json 
from sklearn.linear_model import LogisticRegression
import numpy as np 


class Predict(DoFn):
    def __init__(self):
        super().__init__()
        self.json_file = "LR.json"

    def logistic_regression_from_json(jstring):
        data = json.loads(jstring)
        model = LogisticRegression(**data['init_params'])
        for name, p in data['model_params'].items():
            setattr(model, name, np.array(p))
        return model

    def process(self, element, *args, **kwargs):
        logger = logging.getLogger().setLevel(logging.INFO)
        # open the file 
        ifile = open(self.json_file, "r")
        model = json.load(ifile)
        prediction = model.predict(element)
        logger.log(f"Element {element} - Prediction {prediction}")
        yield prediction

