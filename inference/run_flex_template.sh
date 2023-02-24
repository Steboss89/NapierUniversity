#!/bin/bash
set -e


PROJECT="napieruniversity"
PIPELINE_NAME="napierpipeline"
DATAFLOW_GCS_LOCATION="gs://napierpipeline/templates/template.json"

echo "Project ${PROJECT}"
echo "Job Name/Pipeline Name ${PIPELINE_NAME}"
echo "Dataflow GCS location ${DATAFLOW_GCS_LOCATION}"

GCP_PROJECT_ID="napieruniversity"
gcloud config set project napieruniversity

gcloud dataflow flex-template run ${PIPELINE_NAME} \
--project=${PROJECT} \
--template-file-gcs-location=${DATAFLOW_GCS_LOCATION} \
--region=europe-west1 \
--worker-zone=europe-west1-b \
--worker-machine-type=n1-standard-2 \
--max-workers=2  \
--num-workers=1  \
--temp-location=gs://dataflow-temp/tmp \
--staging-location=gs://dataflow-stag/staging