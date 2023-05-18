# #!/usr/bin/env python
# # coding=utf-8
# from langchain.llms.base import LLM
# from typing import Optional, List, Mapping, Any
# from transformers import LlamaTokenizer, AutoModelForCausalLM, GenerationConfig

# class LlamaModel(LLM):
    
#     model_name: str = ""
#     tokenizer: LlamaTokenizer = None
#     model: AutoModelForCausalLM = None

#     def __init__(self, huggingface_model_name: str) -> None:
#         super().__init__()
#         self.model_name = huggingface_model_name 
#         self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name) 

#         self.model = AutoModelForCausalLM.from_pretrained(self.model_name) 
#         if self.tokenizer.pad_token_id == None:
#             self.tokenizer.add_special_tokens({"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})
#         self.model.resize_token_embeddings(len(self.tokenizer)) 
        
#     @property 
#     def _llm_type(self) -> str: 
#         return self.model_name
    
#     def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:

#         inputs = self.tokenizer(
#             prompt,
#             padding=True,
#             max_length=self.tokenizer.model_max_length,
#             truncation=True,
#             return_tensors="pt"
#         )

#         inputs_len = inputs["input_ids"].shape[1]

#         generation_config = GenerationConfig(
#             max_new_tokens=30,
#             eos_token_id=self.tokenizer.eos_token_id,
#             bos_token_id=self.tokenizer.bos_token_id,
#             pad_token_id=self.tokenizer.pad_token_id,
#         )
#         generated_outputs = self.model.generate(
#             inputs["input_ids"], 
#             generation_config,
#         )
#         decoded_output = self.tokenizer.batch_decode(
#             generated_outputs[..., inputs_len:], skip_special_tokens=True)
#         output = decoded_output[0]
#         return output
    
#     @property
#     def _identifying_params(self) -> Mapping[str, Any]:
#         """Get the identifying parameters."""
#         return {"model_name": self.model_name} 
    
# if __name__ == "__main__":
#     # import ipdb; ipdb.set_trace()
#     # can accept all huggingface LlamaModel family
#     llm = LlamaModel("decapoda-research/llama-7b-hf")
#     print('check which one breaks')
#     print(llm("The capital of China is ?"))

# 上面是我修改的，下面是钱成的，都可以运行。

#!/usr/bin/env python
# coding=utf-8
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
from transformers import LlamaTokenizer, AutoModelForCausalLM

class LlamaModel(LLM):
    
    model_name: str = ""
    tokenizer: LlamaTokenizer = None
    model: AutoModelForCausalLM = None

    def __init__(self, huggingface_model_name: str) -> None:
        super().__init__()
        self.model_name = huggingface_model_name
        self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        if self.tokenizer.pad_token_id == None:
            self.tokenizer.add_special_tokens({"bos_token": "<s>", "eos_token": "</s>", "pad_token": "<pad>"})
        self.model.resize_token_embeddings(len(self.tokenizer))
        
    @property
    def _llm_type(self) -> str:
        return self.model_name
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        inputs = self.tokenizer(
            prompt,
            padding=True,
            max_length=self.tokenizer.model_max_length,
            truncation=True,
            return_tensors="pt"
        )
        inputs_len = inputs["input_ids"].shape[1]
        generated_outputs = self.model.generate(
            input_ids=inputs["input_ids"], #.cuda(),
            attention_mask=inputs["attention_mask"], #.cuda(),
            max_new_tokens=512,
            eos_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
            pad_token_id=self.tokenizer.pad_token_id,
        )
        decoded_output = self.tokenizer.batch_decode(
            generated_outputs[..., inputs_len:], skip_special_tokens=True)
        output = decoded_output[0]
        return output
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model_name": self.model_name}
    
if __name__ == "__main__":
    # can accept all huggingface LlamaModel family
    llm = LlamaModel("decapoda-research/llama-7b-hf")
    print(llm("You are an task creation AI that uses the result of an execution agent to create new tasks with the following objective: What's the weather in Shanghai today? Should I bring an umbrella?, The last completed task has the result: According to the weather report, it is sunny in Shanghai today and there is no precipitation, so you do not need to bring an umbrella.. This result was based on this task description: Make a todo list about this objective: What's the weather in Shanghai today? Should I bring an umbrella?. These are incomplete tasks: . Based on the result, create new tasks to be completed by the AI system that do not overlap with incomplete tasks. Do not generate repetitive tasks (e.g., tasks that have already been completed). If there is not futher task needed to complete the objective, only return NO TASK. Now return the tasks as an array."))