import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import mlflow
import dagshub

# ✅ Set DagsHub token in environment (for security)
os.environ["DAGSHUB_TOKEN"] = "ef58c854e85e26856052fdd89e499ed1904e2e49"

# ✅ Initialize DagsHub & MLflow
dagshub.init(repo_owner='Bharath1462', repo_name='llm-sagemaker-repo', mlflow=True)
mlflow.set_experiment("aws_devops_chatbot")

# ✅ Load data and model
df = pd.read_csv("data/questions_answers.csv")
embedder = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = embedder.encode(df['question'].tolist(), convert_to_tensor=True)

# ✅ Inference logic
def get_best_answer(user_question):
    user_embedding = embedder.encode(user_question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)[0]
    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()
    best_answer = df.iloc[best_idx]['answer']

    # ✅ Log to MLflow
    with mlflow.start_run():
        mlflow.log_param("user_question", user_question)
        mlflow.log_metric("similarity", best_score)

    return best_answer

# ✅ Optional: attach these to model object in interface.py's model_fn if needed
# model.df = df
# model.question_embeddings = question_embeddings

