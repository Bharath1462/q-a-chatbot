
from flask import Flask, request, Response, jsonify
import logging
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from interface import model_fn, predict_fn

# Configure logging for CloudWatch
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
model = None

# Load model at startup
try:
    logger.info("Loading model from /opt/ml/model")
    model = model_fn("/opt/ml/model")
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {str(e)}")

@app.route("/ping", methods=["GET"])
def ping():
    """Health check endpoint required by SageMaker."""
    logger.info("Ping endpoint called")
    
    # Check if model is loaded
    if model is None:
        error_msg = "Health check failed: Model not loaded"
        logger.error(error_msg)
        return Response(error_msg, status=500)
    
    try:
        # Log model information
        logger.info(f"Model type: {type(model)}")
        logger.info(f"Model attributes: {dir(model)}")
        
        # Verify model has required attributes
        if not hasattr(model, 'df') or not hasattr(model, 'question_embeddings'):
            error_msg = "Health check failed: Model missing required attributes"
            logger.error(error_msg)
            return Response(error_msg, status=500)
        
        # Perform a basic model check
        test_input = {"question": "test"}
        result = predict_fn(test_input, model)
        logger.info(f"Test prediction successful: {result}")
        
        logger.info("Health check passed")
        return Response("OK", status=200)
    except Exception as e:
        import traceback
        error_msg = f"Health check failed: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        return Response(error_msg, status=500)

@app.route("/invocations", methods=["POST"])
def invoke():
    logger.info("Invocations endpoint called")
    if model is None:
        logger.error("Model not loaded")
        return Response("Model not loaded", status=500)
    try:
        data = request.get_json()
        if not data:
            logger.error("No input data provided")
            return Response("No input data provided", status=400)
        prediction = predict_fn(data, model)
        logger.info("Inference completed successfully")
        return jsonify(prediction)
    except Exception as e:
        logger.error(f"Inference error: {str(e)}")
        return Response(f"Inference error: {str(e)}", status=500)

if __name__ == "__main__":
    # Log startup information
    logger.info("Starting server with gunicorn")
    
    # Change to the code directory
    os.chdir('/opt/program/code')
    logger.info(f"Working directory: {os.getcwd()}")
    logger.info(f"Directory contents: {os.listdir('.')}")
    logger.info(f"Python path: {sys.path}")
    
    # Use gunicorn for production
    import multiprocessing
    from gunicorn.app.base import BaseApplication

    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            for key, value in self.options.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '%s:%s' % ('0.0.0.0', '8080'),
        'workers': multiprocessing.cpu_count(),
        'timeout': 120,
        'worker_class': 'sync'
    }
    
    StandaloneApplication(app, options).run()
