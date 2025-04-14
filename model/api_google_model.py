import google.generativeai as palm
import google.ai.generativelanguage as gen_lang

from .model_init import Model


class APIGoogleModel(Model):
    def __init__(self, config):
        super().__init__(config)
        try:
            self.api_key = config["api_key_info"]["api_keys"]
        except:
            print("API key and base URL are not provided. Maybe you are using a local model.")        
        self.set_API_key()
        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        
    def set_API_key(self):
        palm.configure(api_key=self.api_key)
        
    def query(self, msg):
        try:
            if 'text' in self.name:
                completion = palm.generate_text(
                    model=self.name,
                    prompt=msg,
                    temperature=self.temperature,
                    max_output_tokens=self.max_output_tokens,
                    safety_settings=[
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_DEROGATORY,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_TOXICITY,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_VIOLENCE,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_SEXUAL,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_MEDICAL,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                        {
                            "category": gen_lang.HarmCategory.HARM_CATEGORY_DANGEROUS,
                            "threshold": gen_lang.SafetySetting.HarmBlockThreshold.BLOCK_NONE,
                        },
                    ]
                )
                response = completion.result

            elif 'chat' in self.name:
                response = palm.chat(messages=msg, candidate_count=1).last
        except:
            response = ""

        return response