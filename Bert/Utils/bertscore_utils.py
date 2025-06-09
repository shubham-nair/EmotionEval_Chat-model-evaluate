import sentence_transformers
from Backend.app.model_loader import sentence_model # Import the globally loaded model
import torch

def evaluate_bertscore(user_inputs, bot_replies):
    print(f"--- Inside evaluate_bertscore ---")
    print(f"ID of imported sentence_model (top-level import): {id(sentence_model)}, Value: {sentence_model}")
    
    # Try to access the module directly during the call
    try:
        import Backend.app.model_loader as runtime_model_loader
        print(f"ID of runtime_model_loader.sentence_model: {id(runtime_model_loader.sentence_model)}, Value: {runtime_model_loader.sentence_model}")
        # If the top-level import is None, but this one is not, let's try using this one
        current_model_to_use = runtime_model_loader.sentence_model if sentence_model is None else sentence_model
    except Exception as e_import:
        print(f"Error importing Backend.app.model_loader at runtime: {e_import}")
        current_model_to_use = sentence_model # Fallback to the top-level imported one

    print(f"Model to be used for encoding: {id(current_model_to_use)}, Value: {current_model_to_use}")
    if current_model_to_use is None:
        # This case should ideally not be hit if preloading works
        print(f"Error: SentenceTransformer model (current_model_to_use) is None.")
        # Return dummy scores to avoid crashing, but log error
        return [0.0], [0.0], [0.0]

    # Ensure inputs are lists of strings, even if single strings are passed
    c_user_inputs = [user_inputs] if isinstance(user_inputs, str) else list(user_inputs)
    c_bot_replies = [bot_replies] if isinstance(bot_replies, str) else list(bot_replies)

    if not c_user_inputs or not c_bot_replies:
        print("Warning: Empty inputs to evaluate_bertscore.")
        return [0.0], [0.0], [0.0]

    try:
        user_embeddings = current_model_to_use.encode(c_user_inputs, convert_to_tensor=True)
        bot_embeddings = current_model_to_use.encode(c_bot_replies, convert_to_tensor=True)

        # Calculate cosine similarity
        # Handles cases: single sentence vs single sentence, or list vs list (pairwise)
        cosine_similarity_matrix = sentence_transformers.util.cos_sim(user_embeddings, bot_embeddings)

        scores = []
        if len(c_user_inputs) == len(c_bot_replies):
            # Pairwise comparison for lists of the same length
            for i in range(len(c_user_inputs)):
                scores.append(round(cosine_similarity_matrix[i][i].item(), 4))
        elif len(c_user_inputs) == 1 and len(c_bot_replies) > 0:
            # One user input vs multiple bot replies (take max similarity to the single user input)
            # Or average, or similarity to first bot reply. For now, let's do first vs first for simplicity if lengths differ significantly.
            # This logic might need to be more sophisticated based on exact requirements.
             scores.append(round(cosine_scores_tensor[0][0].item(), 4)) # Simplified
        elif len(c_bot_replies) == 1 and len(c_user_inputs) > 0:
            # Multiple user inputs vs one bot reply
             scores.append(round(cosine_scores_tensor[0][0].item(), 4)) # Simplified
        elif cosine_scores_tensor.numel() > 0: # Fallback for other cases
            scores.append(round(cosine_scores_tensor[0][0].item(), 4))
        else:
            scores.append(0.0) # Should not happen if inputs are not empty
            
    except Exception as e:
        print(f"Error during sentence embedding or similarity calculation: {e}")
        return [0.0], [0.0], [0.0] # Dummy scores on error

    # Return the similarity scores as F1, and repeat for P and R to maintain structure
    return scores, scores, scores
