import pandas as pd
from transformers import pipeline
import mlflow
import dagshub

# Initialize DagsHub MLflow tracking
dagshub.init(repo_owner='bhumireddyrajareddy01', repo_name='llm_sagemaker_tracking', mlflow=True)
mlflow.set_tracking_uri("https://dagshub.com/bhumireddyrajareddy01/llm_sagemaker_tracking.mlflow")

# Set experiment name
mlflow.set_experiment("aws_devops_chatbot")

# Load dataset of Q&A
df = pd.read_csv("data/questions_answers.csv")

# Initialize HuggingFace QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-cased-distilled-squad")

# Chatbot function
def get_best_answer(user_question):
    best_score = 0
    best_answer = "Sorry, I do not know the answer."

    with mlflow.start_run():
        for _, row in df.iterrows():
            context = row["answer"]
            result = qa_pipeline(question=user_question, context=context)

            if result["score"] > best_score:
                best_score = result["score"]
                best_answer = row["answer"]  # return full answer context

        # Log MLflow metadata
        mlflow.log_param("user_question", user_question)
        mlflow.log_metric("confidence", best_score)

    return best_answer
