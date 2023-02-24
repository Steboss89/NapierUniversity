#!/bin/bash 

function create_flex_template() {
  TEMPLATE_IMAGE="eu.gcr.io/napieruniversity/napierpipeline:latest"
  TEMPLATE_PATH="gs://napierpipeline/templates/template.json"

  echo "${TEMPLATE_IMAGE}"
  echo "${TEMPLATE_PATH}"

  gcloud dataflow flex-template build "${TEMPLATE_PATH}" \
  --image "${TEMPLATE_IMAGE}" \
  --sdk-language "${SDK_LANGUAGE}" \
  --enable-streaming-engine
}

function push_docker_image_to_gcr(){
  echo "Creating Docker image"
  TEMPLATE_IMAGE="eu.gcr.io/napieruniversity/napierpipeline:latest"
  docker build -t "${TEMPLATE_IMAGE}" -f Dockerfile .
  gcloud config set project 424791427488
  gcloud auth configure-docker eu.gcr.io --quiet
  gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://eu.gcr.io
  docker push "${TEMPLATE_IMAGE}"
}

# staging
push_docker_image_to_gcr
create_flex_template 