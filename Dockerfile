# Base image with PyTorch and CUDA
FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set working directory to match SageMaker inference convention
WORKDIR /opt/program

# Copy Python dependencies
COPY code/requirements.txt .

# Install dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Create required directories
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/code

# Copy source code to SageMaker code directory
COPY code/serve /opt/ml/code/
COPY code/serve.py /opt/ml/code/
COPY code/interface.py /opt/ml/code/
COPY code/chatbot.py /opt/ml/code/
COPY data/questions_answers.csv /opt/ml/code/

# Make sure serve is executable
RUN chmod +x /opt/ml/code/serve

# Create symbolic link from /opt/program to /opt/ml/code
RUN ln -s /opt/ml/code /opt/program/code

# Set environment variables required by SageMaker
ENV PYTHONUNBUFFERED=TRUE
ENV SAGEMAKER_PROGRAM=serve
ENV SAGEMAKER_SUBMIT_DIRECTORY=/opt/ml/code
ENV FLASK_APP=serve
ENV FLASK_ENV=production

# Set working directory and run the serve script
WORKDIR /opt/ml/code
ENTRYPOINT ["./serve"]

