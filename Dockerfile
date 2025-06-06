# Base image with PyTorch and CUDA
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set working directory to match SageMaker inference convention
WORKDIR /opt/program

# Copy Python dependencies
COPY code/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# If Flask is not in requirements.txt, install it here (optional)
# RUN pip install flask

# Create required directories
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/code

# Copy source code to both locations for redundancy
COPY code/serve.py /opt/program/
COPY code/interface.py /opt/program/
COPY code/chatbot.py /opt/program/
COPY data/questions_answers.csv /opt/program/

# Also copy to /opt/ml/code as required by SageMaker
COPY code/serve.py /opt/ml/code/
COPY code/interface.py /opt/ml/code/
COPY code/chatbot.py /opt/ml/code/
COPY data/questions_answers.csv /opt/ml/code/

# Ensure serve.py is executable in both locations
RUN chmod +x /opt/program/serve.py
RUN chmod +x /opt/ml/code/serve.py

# Environment variables required by SageMaker
ENV PYTHONUNBUFFERED=TRUE
ENV SAGEMAKER_PROGRAM=serve.py
ENV SAGEMAKER_SUBMIT_DIRECTORY=/opt/ml/code
ENV FLASK_APP=serve.py
ENV FLASK_ENV=production

# Set working directory and entry point
WORKDIR /opt/program
ENTRYPOINT ["python"]
CMD ["/opt/program/serve.py"]

