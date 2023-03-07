from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import sota_llm


def get_exploration_chain():
    template = """{scene}
    
    Add the Dungeon Master's response to the player's action (either narrating what happens or taking the role of an NPC in \
    a dialogue depending on the situation). The context is that the scene above is being acted out during a DnD session. \
    If at the very beginning of the DM and player back-and-forth, we are still at the very beginning of the scene, so respond accordingly! \
    If a fight starts, print the text "Roll for initiative!" verbatim and then stop.
    
    Some information about characters and other entities in the scene: {entity_memory_key}
    
    The game played up so far: {buffer_memory_key}
    
    Player input: {player_input}
    DM, either narrating the story or roleplaying some NPC:"""

    prompt = PromptTemplate(
        input_variables=["scene", "entity_memory_key", "buffer_memory_key", "player_input"],
        template=template
    )

    conv_memory = ConversationBufferWindowMemory(
        llm = sota_llm,
        memory_key="buffer_memory_key",
        input_key="player_input"
    )

    entity_memory = ConversationEntityMemory(llm=sota_llm, memory_key="entity_memory_key", input_key="player_input")

    memory = CombinedMemory(memories=[entity_memory, conv_memory])


    exploration_chain = LLMChain(
        llm=sota_llm,
        prompt=prompt,
        verbose=True,
        memory=memory,
    )
    return exploration_chain