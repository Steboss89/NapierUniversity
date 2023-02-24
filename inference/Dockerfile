FROM gcr.io/dataflow-templates-base/python3-template-launcher-base

RUN mkdir /inference
ARG WORKDIR=/inference
WORKDIR ${WORKDIR}

ENV PYTHONPATH ${WORKDIR}
COPY requirements.txt ${WORKDIR}/requirements.txt
COPY inference_pipeline.py ${WORKDIR}
COPY prediction.py ${WORKDIR}
COPY text_preprocessing.py ${WORKDIR}
COPY KN.joblib ${WORKDIR}

RUN apt-get update \
    && apt-get install -y libffi-dev git \
    && rm -rf /var/lib/apt/lists/* \
    # Upgrade pip and install the requirements.
    && pip install --no-cache-dir --upgrade pip

RUN pip install --no-cache-dir -r ${WORKDIR}/requirements.txt \
    && pip download --no-cache-dir --use-deprecated=legacy-resolver --dest /tmp/dataflow-requirements-cache -r ${WORKDIR}/requirements.txt

RUN python -c "import nltk; nltk.download('punkt', download_dir='/usr/share/nltk_data')"
ENV NLTK_DATA="/usr/share/nltk_data"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/inference_pipeline.py"
#ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV PIP_NO_DEPS=True

ENTRYPOINT [ "/opt/apache/beam/boot" ]