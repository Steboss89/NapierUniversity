import apache_beam as beam 
from apache_beam import DoFn, ParDo, io, Map, Pipeline
from apache_beam.options.pipeline_options import PipelineOptions, SetupOptions, StandardOptions
import text_preprocessing
import prediction
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
                    | "Preprocessing" >> ParDo(text_preprocessing.TextProcessing())
                    | "Predict" >> ParDo(prediction.Predict())
                    )
    p.run()

if __name__=="__main__":
    logging.getLogger().setLevel(logging.INFO)
    run()