# to run the job python3 inference_pipeline.py  --runner DataflowRunner --project napieruniversity --region europe-west1 --temp_location gs://tempbucket5/tmp --staging_location gs://stagingbucket3/staging
import apache_beam as beam 
from apache_beam import DoFn, ParDo, io, Map, Pipeline
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
from inference.text_preprocessing import TextProcessing
from inference.prediction import Predict
import argparse
import logging

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