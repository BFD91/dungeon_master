from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import sota_llm


def get_adventure_chain():
    adventure_generation_template = """Write a highly detailed walkthough of a novel levels {level_range} Dungeons and \
    Dragons adventure. Be highly descriptive of the background setting and locations. Be specific about what characters \
    and enemies are encountered! The adventure should have a complex and interesting plot with many colorful characters \
    of different roles and dispositions. There should be several different options for how the players can approach the \
    adventure. Your walkthrough should describe the adventure scene by scene, and clearly state under what conditions \
    the players progress to another of the scenes (an example might be that after they find the hidden chest in one \
    scene a treasure map directs them to the location of the next scene). Give the scenes the headlines Scene 1, Scene 2,\
     etc. It is important that the adventure has a coherent plot."""

    adventure_generation_prompt = PromptTemplate(
        input_variables=["level_range"],
        template=adventure_generation_template
    )

    adventure_chain = LLMChain(llm=sota_llm, prompt=adventure_generation_prompt)
    return adventure_chain
