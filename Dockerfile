FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

ARG WORKDIR=/dataflow/template
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

ENV PYTHONPATH ${WORKDIR}

COPY inference inference
COPY setup.py setup.py
RUN pip install --no-cache-dir -r inference/requirements.txt
RUN pip download --no-cache-dir --dest /tmp/dataflow-requirements-cache -r inference/requirements.txt
RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/share/nltk_data')"
# Do not include `apache-beam` in requirements.txt
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/inference/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/inference/inference_pipeline.py"
ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV PIP_NO_DEPS=True
ENV NLTK_DATA="/usr/share/nltk_data"