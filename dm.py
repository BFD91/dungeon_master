import json
import os
from datetime import datetime

from llm_chains.adventure_generator import adventure_generation_prompt
from llm_chains.introduction_generator import introduction_generation_prompt
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate
from llm_chains.exploration_chatbot import exploration_prompt
from llm_chains.fight_chatbot import fighting_prompt
from llm_chains.scene_generator import scene_generation_prompt
from llm_chains.helpers.llms import sota_llm
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryMemory, CombinedMemory, ConversationEntityMemory

LEVEL_RANGE = "1-5"

class DM:
    def __init__(self):
        self.history = []
        self.adventure_chain = None
        self.adventure = None
        self.introduction_chain = None
        self.scene_chain = None
        self.fight_chain = None
        self.exploration_chain = None
        self.introduction = None
        self.detailed_scenes = None
        self.adventure_scenes = None
        self.adventure_scenes_iter = None
        self.conv_memory = ConversationBufferWindowMemory(
            k=4,
            memory_key="buffer_memory_key",
            input_key="player_input"
        )
        self.entity_memory = ConversationEntityMemory(llm=sota_llm)
        self.combined_memory = CombinedMemory(memories=[self.conv_memory, self.entity_memory])
        self.state = {'stage': "initialization", 'scene': None}

    def run_dm_loop(self):
        print("Initializing DM...")
        self.initialize_dm()
        export_output(self.introduction)
        self.history.append({"source": "output", "text": self.introduction})
        self.state = {'stage': "exploration", 'scene': next(self.adventure_scenes_iter)}
        while self.state != "done":
            player_input = get_player_input()
            if player_input == "/quit":
                break
            elif player_input == "/save":
                self.save_history()
                continue
            #elif player_input.startswith("/override "):
            #    override_output = player_input.split("/override ")[1]
            #    export_output(override_output)

            self.history.append({"source": "input", "text": player_input})
            output = self.run_dm_step(player_input)
            export_output(output)
            self.history.append({"source": "output", "text": output})
        output = "And this concludes this particular chapter of our brave adventurers' tale. Thank you for playing!"
        self.history.append({"source": "output", "text": output})
        self.save_history()

    def save_history(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Save history to json file with timestamp as name.
        with open(os.path.join("saved_sessions", f"{timestamp}_history.json"), "w") as f:
            json.dump(self.history, f)

    def run_dm_step(self, player_input):
        if self.state["stage"] == "exploration":
            output = self.run_exploration_step(player_input)
        elif self.state["stage"] == "fight":
            output = self.run_fight_step(player_input)
        else:
            raise Exception("Invalid state")
        return output

    def inialize_adventure_chain(self):
        self.adventure_chain = LLMChain(llm=sota_llm, prompt=adventure_generation_prompt)

    def generate_adventure(self):
        self.adventure = self.adventure_chain.run(level_range=LEVEL_RANGE)
        self.adventure_scenes = [scene for scene in self.adventure.split("Scene") if (scene and scene != "\n\n")]
        self.adventure_scenes_iter = iter(self.adventure_scenes)

    def initialize_introduction_chain(self):
        self.introduction_chain = LLMChain(llm=sota_llm, prompt=introduction_generation_prompt)

    def generate_introduction(self):
        self.introduction = self.introduction_chain.run(adventure=self.adventure)

    def initialize_scene_chain(self):
        self.scene_chain = LLMChain(llm=sota_llm, prompt=scene_generation_prompt)

    def generate_detailed_scenes(self):
        self.detailed_scenes = []
        for scene in self.adventure_scenes:
            detailed_scene = self.scene_chain.run({"scene": scene})
            self.detailed_scenes.append(detailed_scene)

    def initialize_fight_chain(self):
        self.fight_chain = LLMChain(llm=sota_llm, prompt=fighting_prompt, verbose=True, memory=self.conv_memory)

    def initialize_exploration_chain(self):
        self.exploration_chain = LLMChain(llm=sota_llm, prompt=exploration_prompt, verbose=True, memory=self.combined_memory)

    def initialize_dm(self):
        self.inialize_adventure_chain()
        self.generate_adventure()
        self.initialize_introduction_chain()
        self.generate_introduction()
        self.initialize_scene_chain()
        self.generate_detailed_scenes()
        self.initialize_fight_chain()
        self.initialize_exploration_chain()

    def run_exploration_step(self, player_input):
        output = self.exploration_chain.run({'scene': self.state['scene'], 'player_input': player_input})
        if "~Next Scene~" in output:
            self.state['scene'] = next(self.adventure_scenes_iter)
            output = output.replace("~Next Scene~", "")
        elif "~End Adventure~" in output:
            self.state["stage"] = "done"
            output = output.replace("~End Adventure~", "")
        elif "~Fight~" in output:
            self.state["stage"] = "fight"
            output = output.replace("~Fight~", "")
            self.initialize_fight_chain()
        return output

    def run_fight_step(self, player_input):
        output = self.fight_chain.run({'player_input': player_input})
        if "~End Fight~" in output:
            self.state["stage"] = "exploration"
            output = output.replace("~End Fight~", "")
            self.initialize_exploration_chain()
        return output


def get_player_input():
    return input()


def export_output(output_text):
    print(output_text)


if __name__ == "__main__":
    dm = DM()
    dm.run_dm_loop()
