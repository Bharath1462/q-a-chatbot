from transformers import pipeline
import json

def model_fn(model_dir):
    return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

def predict_fn(data, model):
    question = data.get("question")
    context = data.get("context")
    if not question or not context:
        return {"error": "Invalid input"}
    answer = model(question=question, context=context)
    return {"answer": answer["answer"], "score": answer["score"]}
