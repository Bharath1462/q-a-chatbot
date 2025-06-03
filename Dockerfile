FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Create working directory for inference code
WORKDIR /opt/program

# Install Python packages
COPY code/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Install Flask (if not in requirements.txt)
RUN pip install flask

# Copy source code
COPY code/serve.py /opt/program/serve.py
COPY code/interface.py /opt/program/interface.py
COPY data/questions_answers.csv /opt/program/questions_answers.csv
# Make serve.py executable
RUN chmod +x /opt/program/serve.py

# Create model directory
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/code
# Required env for SageMaker inference
ENV PYTHONUNBUFFERED=TRUE
ENV SAGEMAKER_PROGRAM=serve.py
ENV SAGEMAKER_SUBMIT_DIRECTORY=/opt/ml/code

# Required for SageMaker to run your container
ENTRYPOINT ["python"]
CMD ["serve.py"]
