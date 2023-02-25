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
    && rm -rf /var/lib/apt/lists/* ;

RUN sudo apt-get -y install libbz2-dev 
RUN apt update; \
apt install -y build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev; \
wget https://www.python.org/ftp/python/3.9.2/Python-3.9.2.tgz; \
tar -zxvf Python-3.9.2.tgz; \
cd Python-3.9.2; \
sudo ./configure --prefix=/usr/local/python3; \
sudo make; \
sudo make install; \
ln -sf /usr/local/python3/bin/python3.9 /usr/local/bin/python3; \
ln -sf /usr/local/python3/bin/pip3.9 /usr/local/bin/pip3

RUN pip3 install bz2file
RUN pip3 install --no-cache-dir -r ${WORKDIR}/requirements.txt 
RUN pip3 install pysqlite3
#RUN python3 -c "import nltk; nltk.download('stopwords', download_dir='/usr/share/nltk_data')"
#ENV NLTK_DATA="/usr/share/nltk_data"
ENV FLEX_TEMPLATE_PYTHON_REQUIREMENTS_FILE="${WORKDIR}/requirements.txt"
ENV FLEX_TEMPLATE_PYTHON_PY_FILE="${WORKDIR}/inference_pipeline.py"
#ENV FLEX_TEMPLATE_PYTHON_SETUP_FILE="${WORKDIR}/setup.py"
ENV PIP_NO_DEPS=True

ENTRYPOINT [ "/opt/apache/beam/boot" ]