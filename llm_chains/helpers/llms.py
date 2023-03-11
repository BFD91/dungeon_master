from langchain import OpenAI
from langchain.llms import OpenAIChat

openai_api_key = "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"

#SOTA_OPENAI_LLM = "text-davinci-003"

sota_llm = OpenAIChat(temperature=0.7, api_key="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")

#sota_llm = OpenAI(model_name=SOTA_OPENAI_LLM, openai_api_key=openai_api_key)