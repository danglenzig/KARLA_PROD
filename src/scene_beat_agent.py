# src/scene_beat_agent.py
# TODO: figure out a way to unit test this with local data, and without running through the whole pipeline from main

from pydantic import BaseModel, Field
from agents import Agent, Runner, RunResult
from pathlib import Path
from dotenv import load_dotenv
import sys


load_dotenv()

SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))


from narrative_design_agent import NarrativeDesignOutputSchema


scene_beat_agent: Agent = Agent(
    name="scene_beat_agent",
    instructions="You are a helpful and concise agent",
    model="gpt-5.4-mini"
    # TODO: ^^define the actual agent
)

class SceneBeatAgent():
    def __init__(self):
        self.agent: Agent = scene_beat_agent

    async def run_workflow(self, narrative_design_spec: NarrativeDesignOutputSchema):
        print(f"Coming soon: The SceneBeatAgent writes scene beats for {narrative_design_spec.story_title}!!!")