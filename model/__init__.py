from .api_openai_model import APIOpenAIModel
from .local_model import LocalModel
from .api_google_model import APIGoogleModel
from .api_zhipuai_model import APIZHIPUModel


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
        elif provider == "google":
            model = APIGoogleModel(config) #TODO: google model is not implemented yet
        elif provider == "zhipuai":
            model = APIZHIPUModel(config) 
        else:
            raise ValueError(f"ERROR: Unknown provider {provider} for API model.")
    else:
            model = LocalModel(config)

    return model