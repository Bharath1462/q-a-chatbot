FROM python:3.9-slim

RUN pip install --upgrade pip
COPY model /opt/program/model

WORKDIR /opt/program/model

RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED=TRUE

ENV SAGEMAKER_PROGRAM=inference.py

ENTRYPOINT ["python", "inference.py"]
