from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

from llm_chains.helpers.llms import gpt_3_5


template = """{scene}

Add the Dungeon Master's action in the DnD fight scene. The wider context is that the fight following the scene above is \
being played out during a DnD session. The DM's action should follow the DnD 5e rules for combat. The action may \
be a description of what an NPC does or what consequences happen as a result of the player's action. It is extremely important \
that the DM asks the player to roll a dice when appropriate, such as when the player attacks an enemy or when the enemy attacks, \
in accordance with the DnD 5e rules for combat. The DM should narrate vividly and with immersion. \
If the end of the fight is reached (for example if all enemies are vanquished or if the player successfully flees), \
print the text "~End Fight~" verbatim and then stop.

The following is a list of all the enemy types in the fight: 
{monsters}

The fight played up so far:

{history}
Player input: {player_input}
DM action (a single sentence):"""

fighting_prompt = PromptTemplate(
    input_variables=["scene", "history", "player_input", "monsters"],
    template=template
)


monsters_template = """
{history}

List the enemies participating in the above DnD scene. For each kind of enemy (monster or NPC), list all stats (including spells and actions) \
of the enemy type as given in the DnD 5e Monster Manual. For example, if the enemies all are normal goblins, list the goblin's stats, such as hit points, armor class, \
strength, dexterity, constitution, intelligence, wisdom, charisma, speed, and any spells or actions that the goblin can perform. {player_input}\
"""

monsters_prompt = PromptTemplate(
    input_variables=["history", "player_input"],
    template=monsters_template
)

