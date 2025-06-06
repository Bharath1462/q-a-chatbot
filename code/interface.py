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
    try:
        if not isinstance(input_data, dict) or "question" not in input_data:
            raise ValueError("Input must be a dictionary with a 'question' key")
        
        question = input_data["question"]
        if not isinstance(question, str):
            raise ValueError("Question must be a string")
            
        # Encode the input question
        question_embedding = model.encode(question, convert_to_tensor=True)
        
        # Find the most similar question in our dataset
        from torch import nn
        cos = nn.CosineSimilarity(dim=1)
        similarities = cos(question_embedding.unsqueeze(0), model.question_embeddings)
        
        # Get the most similar question's index
        most_similar_idx = similarities.argmax().item()
        
        # Get the corresponding answer
        answer = model.df.iloc[most_similar_idx]['answer']
        
        return {"answer": answer, "confidence": similarities[most_similar_idx].item()}
    except Exception as e:
        import logging
        logging.getLogger(__name__).error(f"Prediction failed: {str(e)}")
        raise
