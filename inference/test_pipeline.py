# to run the job python3 test_pipeline.py  --runner DataflowRunner --project napieruniversity --region europe-west1 --temp_location gs://tempbucket5/tmp --staging_location gs://stagingbucket3/staging
import apache_beam as beam 
from apache_beam import DoFn, ParDo, io, Map, Pipeline
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
import argparse
import logging

import joblib
import numpy as np 
from sklearn.feature_extraction.text import TfidfVectorizer

class Predict(DoFn):     

    def process(self, element, *args, **kwargs):
        self.model = joblib.load("KN.joblib", "r")
        logger = logging.getLogger().setLevel(logging.INFO)
        prediction = self.model.predict(element)
        logger.log(f"Element {element} - Prediction {prediction}")
        yield prediction


class TextProcessing(DoFn):

    def process(self, element, *args, **kwargs):
        r""" Given an element perform the text cleaning
        """
         # theoretically this is wrong, we should have a saved TfIdF 
        vectorizer = TfidfVectorizer() 
        vectors = vectorizer.fit_transform([str(element)])

        yield vectors
        

def run(argv=None):
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)
    pipeline_options =PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session=True 
    pipeline_options.view_as(StandardOptions).streaming=True 

    p = Pipeline(options=pipeline_options)
    spam_pipeline = (p 
                    | "Read input text from PubSub" >> io.ReadFromPubSub(subscription="projects/napieruniversity/subscriptions/scamspaminputs-sub", with_attributes=True )
                    | "Preprocessing" >> ParDo(TextProcessing())
                    | "Predict" >> ParDo(Predict())
                    )
    p.run()

if __name__=="__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()