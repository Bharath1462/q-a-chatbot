FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Create working directory for inference code
WORKDIR /opt/program

# Install Python packages
COPY code/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install Flask (if not in requirements.txt)
RUN pip install flask

# Create directories
RUN mkdir -p /opt/ml/model && mkdir -p /opt/ml/code

# Copy source code
COPY code/serve.py /opt/program/
COPY code/interface.py /opt/program/
COPY code/chatbot.py /opt/program/
COPY data/questions_answers.csv /opt/program/

# Copy files to code directory for SageMaker
RUN cp /opt/program/serve.py /opt/ml/code/
RUN cp /opt/program/interface.py /opt/ml/code/
RUN cp /opt/program/chatbot.py /opt/ml/code/
RUN cp /opt/program/questions_answers.csv /opt/ml/code/

# Make files executable
RUN chmod +x /opt/program/*.py
RUN chmod +x /opt/ml/code/*.py

# Required env for SageMaker inference
ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONPATH=/opt/program:/opt/ml/code
ENV SAGEMAKER_PROGRAM=serve.py
ENV SAGEMAKER_SUBMIT_DIRECTORY=/opt/ml/code
ENV LOG_LEVEL=DEBUG

# Required for SageMaker to run your container
WORKDIR /opt/program
ENTRYPOINT ["python"]
CMD ["/opt/program/serve.py"]
