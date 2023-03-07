from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from helpers.llms import sota_llm


def get_fight_chain(previous_memory):
    template = """{scene}

    Add the Dungeon Master's action in the DnD fight scene. The wider context is that the fight following the scene above is \
    being played out during a DnD session. The DM's action should follow the DnD 5e rules for combat. The action may \
    be a description of what an NPC does or what consequences happen as a result of the player's action. It is extremely important \
    that the DM asks the player to roll a dice when appropriate, such as when the player attacks an enemy or when the enemy attacks, \
    in accordance with the DnD 5e rules for combat. The DM should narrate vividly and with immersion.
    

    {history}
    Player input: {player_input}
    DM action:"""

    prompt = PromptTemplate(
        input_variables=["scene", "history", "player_input"],
        template=template
    )

    fight_chain = LLMChain(
        llm=sota_llm,
        prompt=prompt,
        verbose=True,
        memory=previous_memory,
    )
    return fight_chain