import torch
from transformers import AutoTokenizer,AutoModelForCausalLM

from .model_init import Model


class LocalModel(Model):
    def __init__(self, config):
        super().__init__(config)
        self.max_output_tokens = int(config["params"]["max_output_tokens"])
        self.device = config["params"]["device"]
        self.max_output_tokens = config["params"]["max_output_tokens"]

        self.tokenizer = AutoTokenizer.from_pretrained(self.name, device_map="auto")
        self.model = AutoModelForCausalLM.from_pretrained(self.name, device_map="auto", torch_dtype=torch.float16)

    def query(self, msg):
        input_ids = self.tokenizer(msg, return_tensors="pt").input_ids.to("cuda")
        outputs = self.model.generate(input_ids,
            temperature=0.9,
            max_new_tokens=self.max_output_tokens,
            early_stopping=True)
        out = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        result = out[len(msg):]
        return result