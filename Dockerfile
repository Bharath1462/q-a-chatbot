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

# Copy source code
COPY code/serve.py .
COPY code/interface.py .
COPY data/questions_answers.csv .

# Ensure serve.py is executable
RUN chmod +x serve.py

# Optional: Create model and code directories (if your code uses them)
RUN mkdir -p /opt/ml/model
RUN mkdir -p /opt/ml/code

# Environment variables required by SageMaker
ENV PYTHONUNBUFFERED=TRUE
ENV SAGEMAKER_PROGRAM=serve.py
ENV SAGEMAKER_SUBMIT_DIRECTORY=/opt/ml/code

# Set entry point and default command
ENTRYPOINT ["python"]
CMD ["./serve.py"]

