from chatbot import get_best_answer
import json

def model_fn(model_dir):
    from sentence_transformers import SentenceTransformer
    import pandas as pd
    import os
    import logging
    
    logger = logging.getLogger(__name__)
    
    try:
        # Load the embeddings model
        logger.info("Loading SentenceTransformer model...")
        model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Try multiple possible locations for the CSV file
        possible_paths = [
            os.path.join(os.path.dirname(__file__), 'questions_answers.csv'),
            '/opt/program/code/questions_answers.csv',
            '/opt/program/questions_answers.csv',
            '/opt/ml/code/questions_answers.csv'
        ]
        
        df = None
        for data_path in possible_paths:
            logger.info(f"Trying to load CSV from: {data_path}")
            if os.path.exists(data_path):
                logger.info(f"Found CSV file at: {data_path}")
                df = pd.read_csv(data_path)
                break
                
        if df is None:
            raise FileNotFoundError(f"Could not find questions_answers.csv in any of: {possible_paths}")
            
        logger.info("Creating embeddings...")
        model.df = df
        model.question_embeddings = model.encode(df['question'].tolist(), convert_to_tensor=True)
        logger.info("Model initialization complete")
        return model
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        raise RuntimeError(f"Failed to load model: {str(e)}")

def predict_fn(input_data, model):
    question = input_data.get("question")
    answer = get_best_answer(question)
    return {"answer": answer}
