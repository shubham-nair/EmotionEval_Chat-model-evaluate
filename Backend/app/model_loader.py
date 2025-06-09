# Backend/app/model_loader.py
from sentence_transformers import SentenceTransformer

# Global variable to hold the loaded model
sentence_model = None

async def preload_model():
    global sentence_model
    print("Preloading SentenceTransformer model ('all-MiniLM-L6-v2') from model_loader...")
    try:
        sentence_model = SentenceTransformer('all-MiniLM-L6-v2')
        print("SentenceTransformer model loaded successfully from model_loader.")
        print(f"ID of sentence_model in model_loader after load: {id(sentence_model)}")
    except Exception as e:
        print(f"Error loading SentenceTransformer model in model_loader: {e}")
