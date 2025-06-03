import pandas as pd
from sentence_transformers import SentenceTransformer, util
import mlflow
import dagshub
dagshub.init(repo_owner='bhumireddyrajareddy01', repo_name='llm_sagemaker_tracking', mlflow=True)
mlflow.set_tracking_uri("https://dagshub.com/bhumireddyrajareddy01/llm_sagemaker_tracking.mlflow")

mlflow.set_experiment("aws_devops_chatbot")

df = pd.read_csv("data/questions_answers.csv")

embedder = SentenceTransformer('all-MiniLM-L6-v2')
question_embeddings = embedder.encode(df['question'].tolist(), convert_to_tensor=True)

def get_best_answer(user_question):
    user_embedding = embedder.encode(user_question, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)[0]
    best_idx = similarities.argmax().item()
    best_score = similarities[best_idx].item()
    best_answer = df.iloc[best_idx]['answer']

    with mlflow.start_run():
        mlflow.log_param("user_question", user_question)
        mlflow.log_metric("similarity", best_score)

    return best_answer
