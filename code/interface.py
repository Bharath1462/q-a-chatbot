from chatbot import get_best_answer
import json

def model_fn(model_dir):
    from sentence_transformers import SentenceTransformer
    import pandas as pd
    import os
    
    try:
        # Load the embeddings model
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load the QA dataset
        data_path = os.path.join(os.path.dirname(__file__), 'questions_answers.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            model.df = df
            model.question_embeddings = model.encode(df['question'].tolist(), convert_to_tensor=True)
            return model
        else:
            raise FileNotFoundError(f"Could not find questions_answers.csv at {data_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to load model: {str(e)}")

def predict_fn(input_data, model):
    question = input_data.get("question")
    answer = get_best_answer(question)
    return {"answer": answer}
