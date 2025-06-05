
from flask import Flask, request, Response, jsonify
from interface import model_fn, predict_fn
import logging
import sys

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
    logger.info("Ping endpoint called")
    if model is None:
        logger.error("Health check failed: Model not loaded")
        return Response("Model not loaded", status=500)
    try:
        # Perform a basic model check
        test_input = {"question": "test"}
        predict_fn(test_input, model)
        logger.info("Health check passed")
        return Response("OK", status=200)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return Response(str(e), status=500)

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
    logger.info("Starting Flask server on port 8080")
    app.run(host="0.0.0.0", port=8080)
