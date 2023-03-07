from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import sota_llm


def get_introduction_chain():
    introduction_generation_template = """Consider the following DnD adventure:
    
    {adventure}
    
    The following is a highly detailed introduction to the adventure. The introduction begins with a description of the area
    in which the adventure takes place, including geography, climate, history, political situation, and culture. The introduction
    then moves on to describe how it came to be that the party is in the area, and what they are doing there.
    
    
    """

    introduction_generation_prompt = PromptTemplate(
        input_variables=["adventure"],
        template=introduction_generation_template
    )

    introduction_chain = LLMChain(llm=sota_llm, prompt=introduction_generation_prompt)

    return introduction_chain