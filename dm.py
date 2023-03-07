from llm_chains.adventure_generator import get_adventure_chain
from llm_chains.introduction_generator import get_introduction_chain
from llm_chains.exploration_chatbot import get_exploration_chain
from llm_chains.fight_chatbot import get_fight_chain
from llm_chains.scene_generator import get_scene_chain

LEVEL_RANGE = "1-5"

class DM:
    def __init__(self):
        self.adventure_chain = get_adventure_chain()
        self.adventure = self.adventure_chain.run(level_range=LEVEL_RANGE)
        self.introduction_chain = get_introduction_chain()
        self.introduction = self.introduction_chain.run(adventure=self.adventure)
        self.adventure_scenes = [scene for scene in self.adventure.split("Scene") if (scene and scene != "\n\n")]
        self.detailed_scenes = []
        self.scene_chain = get_scene_chain()
        for scene in self.adventure_scenes:
            detailed_scene = self.scene_chain.run({"scene": scene})
            self.detailed_scenes.append(detailed_scene)
        self.fight_chain = get_fight_chain()
        self.exploration_chain = get_exploration_chain()
        self.state = "initialization"

    def run_dm_loop(self):
        while self.state != "done":
            output_text, self.state = self.run_dm_step()
            if self.state == "done":
                break

    def run_dm_step(self):
        if self.state == "initialization":
            return self.introduction, "exploration"
        elif self.state == "exploration":
            return self.exploration_chain.run(), "fight"
        elif self.state == "fight":
            return self.fight_chain.run(), "exploration"
        elif self.state == "done":
            return "The adventure is over!", "done"
