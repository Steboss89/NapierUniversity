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


RUN apt update -y && sudo apt upgrade -y && \
    apt-get install -y wget build-essential checkinstall  libreadline-gplv2-dev  libncursesw5-dev  libssl-dev  libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev && \
    cd /usr/src && \
    sudo wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz && \
    sudo tar xzf Python-3.9.2.tgz && \
    cd Python-3.9.2 && \
    sudo ./configure --enable-optimizations && \
    sudo make altinstall

RUN pip3 install --no-cache-dir -r ${WORKDIR}/requirements.txt \
    && pip3 download --no-cache-dir --use-deprecated=legacy-resolver --dest /tmp/dataflow-requirements-cache -r ${WORKDIR}/requirements.txt

RUN python3 -c "import nltk; nltk.download('punkt', download_dir='/usr/share/nltk_data')"
ENV NLTK_DATA="/usr/share/nltk_data"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/inference_pipeline.py"
#ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV PIP_NO_DEPS=True

ENTRYPOINT [ "/opt/apache/beam/boot" ]