from chatbot import get_best_answer
import json

def model_fn(model_dir):
    return None  # not using a model object, just logic

def predict_fn(input_data, model):
    question = input_data.get("question")
    answer = get_best_answer(question)
    return {"answer": answer}
