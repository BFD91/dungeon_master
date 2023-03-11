from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import sota_llm


template = """{scene}

Add the Dungeon Master's response to the player's action (either narrating what happens or taking the role of an NPC in \
a dialogue depending on the situation). The context is that the scene above is being acted out during a DnD session. \
If at the very beginning of the DM and player back-and-forth, we are still at the very beginning of the scene, so respond accordingly! \
If a fight starts, print the text "~Fight~" verbatim and then stop. \
If the end of the scene is reached and it's time for the next scene to begin, print the text "~Next Scene~" verbatim and then stop. \
If the end of the entire adventure is reached, print the text "~End Adventure~" verbatim and then stop. \

Some information about characters and other entities in the scene: {entity_memory_key}

The game played up so far: {buffer_memory_key}

Player input: {player_input}
DM, either narrating the story or roleplaying some NPC:"""

exploration_prompt = PromptTemplate(
    input_variables=["scene", "entity_memory_key", "buffer_memory_key", "player_input"],
    template=template
)



