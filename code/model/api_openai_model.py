from openai import OpenAI
import openai
from .model_init import Model
import time


class APIOpenAIModel(Model):
    def __init__(self, config):
        super().__init__(config)
        try:
            self.api_key = config["api_key_info"]["api_keys"]
            self.api_url = config["api_key_info"]["api_url"]
            print(self.api_key)
            print(self.api_url)
        except:
            print("ERROR: API key and base URL are not provided. Maybe you are using a local model.")
        self.set_API_key()
        self.max_output_tokens = int(config["params"]["max_output_tokens"])

    def set_API_key(self):
        self.client = OpenAI(api_key=self.api_key, base_url=self.api_url)
    
    def set_instruction(self, instruction):
        text_split = instruction.split('\nText: ') 
        if len(text_split) == 2:
            sys_instruction = text_split[0]
            user_instruction = text_split[1]
        else:
            sys_instruction = ""
            user_instruction = instruction
        return sys_instruction, user_instruction

    def query(self, msg, base64_images):
        sys_instruction, user_instruction = self.set_instruction(msg)
        for _ in range(10):
            tag=False 
            print("Start Query")
            response = ""
            try:
                user_content = [{"type": "text", "text": "\nText: " + user_instruction}]
                for img in base64_images:
                    user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img}"}})    

                    
                #user_content.extend([{"type": "image_url", "image_url": {"url": url}} for url in img_url]))
                start_time = time.time()
                completion = self.client.chat.completions.create(
                    model=self.name,
                    messages=[
                        {"role": "system", "content": sys_instruction},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=self.temperature,
                    max_tokens=self.max_output_tokens
                )
                end_time = time.time()
                total_time = end_time - start_time
                if completion and completion.choices:
                    print(completion.choices[0].message.content)
                    response = completion.choices[0].message.content
                else:
                    print("API response is empty or malformed. No choices returned.")
                    response = "API response is empty or malformed. No choices returned."

                #response = completion.choices[0].message.content
                tag=True
                # time.sleep(5)
                break
            except openai.APIConnectionError as e:
                print("The server could not be reached")
                print(e.__cause__)  # an underlying Exception, likely raised within httpx.
            except openai.RateLimitError as e:
                print("A 429 status code was received; we should back off a bit.")
            except openai.APIStatusError as e:
                print("Another non-200-range status code was received")
                print(e.status_code)
                print(e.response)
            time.sleep(2)

        return response,total_time if tag else "I can't assist your question"