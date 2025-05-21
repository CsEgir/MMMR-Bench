from .api_openai_model import APIOpenAIModel
from .api_thinking_model import APIThinkingModel

def create_model(config):
    """
    Factory method to create a LLM instance
    """
    provider = config["model_info"]["provider"].lower()
    '''Choose the model deployment method, default is API'''
    model_method = config["model_info"]["model_method"].lower() if "model_method" in config["model_info"] else 'api'
    if model_method == 'api':
        if provider == "openai":
            model = APIOpenAIModel(config)
        elif provider == "thinking":
            model = APIThinkingModel(config)    
        else:   
            raise ValueError(f"ERROR: Unknown provider {provider} for API model.")

    return model