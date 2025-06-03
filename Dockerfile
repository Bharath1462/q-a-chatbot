FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Create working directory for inference code
WORKDIR /opt/program

# Install Python packages
COPY code/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy source code (e.g., serve.py and interface.py)
COPY code/serve.py code/interface.py . 

# Install Flask (if not in requirements.txt)
RUN pip install flask

# Required env for SageMaker inference
ENV PYTHONUNBUFFERED=TRUE

# Required for SageMaker to run your container
ENTRYPOINT ["python"]
CMD ["serve.py"]

