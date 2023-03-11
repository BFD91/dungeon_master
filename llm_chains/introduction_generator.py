from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import sota_llm



introduction_generation_template = """Consider the following DnD adventure:

{adventure}

The following is a highly detailed introduction to the setting where the adventure takes place. The introduction begins \
with a description of the area in which the adventure takes place, including geography, climate, history, political \
situation, and culture. The introduction then moves on to give a vague and spoiler-free hint of the adventure to come, for example by \
mentioning circulating rumors pertaining to the adventure. 

"""

introduction_generation_prompt = PromptTemplate(
    input_variables=["adventure"],
    template=introduction_generation_template
)

introduction_chain = LLMChain(llm=sota_llm, prompt=introduction_generation_prompt)

