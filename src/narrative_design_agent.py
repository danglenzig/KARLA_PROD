# src/narrative_design_agent.py
# this is the main file for the narrative design agent. It will contain the main logic for generating the story, 
# characters, and dialogue for the visual novel game. It will also define the output schema for the narrative 
# design agent, which will be used to structure the output data that is given to downstream agents.

import asyncio
from pydantic import BaseModel, Field
from agents import Agent, ModelSettings, TResponseInputItem, Runner, RunResult, RunConfig, trace, function_tool
from openai.types.shared.reasoning import Reasoning
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

#========
# Schemas
#========

class CharacterData(BaseModel):
    uuid: str                       = Field(..., description="A unique ID string for this character")
    name: str                       = Field(..., description="The name of the character")
    portrait_image_prompt: str      = Field(..., description="A descriptive prompt to generate the dialogue portrait image of the character")
    dialogue_examples: list[str]    = Field(..., description="A list of example dialogue lines for the character. These will be used to generate " \
    "actual dialogue lines for the character in the game.")


class LocationData(BaseModel):
    uuid: str                       = Field(..., description="A unique ID string for this location")
    name: str                       = Field(..., description="The name of the location")
    location_image_prompt: str      = Field(..., description="A descriptive prompt to generate the background image of the location")

class Location(BaseModel):
    location_data: LocationData      = Field(..., description="The data for the location, including name and location image prompt")

class PlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the player character, including name, portrait image prompt, and dialogue examples")

class NonPlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the non-player character, including name, portrait image prompt, and dialogue examples")

class SceneData(BaseModel):
    uuid: str                        = Field(..., description="A unique ID string for this scene")
    location:Location                = Field(..., description="The data for the location of the scene")
    non_player_characters: list[NonPlayerCharacter] = Field(..., description="A list of non-player characters that are present in the scene")
    narrtive_summary: str = Field(..., description="A brief summary of the narrative that takes place in the scene. This will be used to generate " \
    "the dialogue and player choices for the scene.")    

class Scene(BaseModel):
    scene_data: SceneData            = Field(..., description="The data for the scene, including location, non-player characters, and narrative summary")

class NarrativeDesignOutputSchema(BaseModel):
    story_title: str
    player_character: PlayerCharacter
    non_player_characters: list[NonPlayerCharacter]
    locations: list[Location]
    intro_scene: Scene
    act_one: list[Scene]
    act_two: list[Scene]
    act_three: list[Scene]
    outro_scene: Scene

class WorkflowTextInput(BaseModel):
    input_as_text: str = Field(..., description="The high-level concept for the story")

class OutputSchema(BaseModel):
    output_text: str    = Field(..., description="A JSON string of the agent output")
    output_dict: dict   = Field(..., description="A Python dictionary of the agent output")
    reasoning_dump: str = Field(..., description="All the reasoning steps the agent took")


#===============
# Function Tools
#===============

@function_tool
def get_uuid_string():
    """Returns a unique UUID string"""
    myuuid = uuid.uuid4()
    return str(myuuid)

#=============
# Instructions
#=============

narrative_design_agent_instructions = f"""
You are a senior Narrative Designer at an indie game Studio that makes visual novel games in Ren'Py.
Your task is to turn the input story concept into detailed narrative design specification for a visual novel.
Your output will be used by downstream agents to generate visual assets, write dialogue, and code the game in Ren'Py. 

Every game shall have:
- Exactly one player character.
- Three or more non-player characters
- Three or more locations
- Exactly one intro scene, which introduces the narrative and orients the player
- Exactly three acts, each act conisting of 2-3 scenes
- Exactly one outro scene -- the game's denouement

Use the get_uuid_string tool to get UUID strings
"""

#==============
# Model strings
#==============

NARRATIVE_DESIGN_AGENT_MODEL: str   = "gpt-5.4"
MINI_MODEL: str                     = "gpt-5.4-mini"

#=======
# Agents
#=======

narrative_design_agent = Agent(
    name="narrative_design_agent",
    instructions = narrative_design_agent_instructions,
    model=NARRATIVE_DESIGN_AGENT_MODEL,
    output_type=NarrativeDesignOutputSchema,
    model_settings=ModelSettings(
        reasoning=Reasoning(
            effort="high",
            summary="detailed"
        )
    ),
    tools=[get_uuid_string]
)


# This module's main class
class NarrativeDesignAgent:
    def __init__(self):
        self.agent: Agent = narrative_design_agent

    async def run_workflow(self, workflow_text_input: WorkflowTextInput) -> OutputSchema:
        workflow = workflow_text_input.model_dump()
        input_text = workflow["input_as_text"]

        run_result: RunResult = await Runner.run(
            narrative_design_agent,
            input=input_text
        )

        # TODO: fix this...
        _reasoning_dump = ""
        for item in run_result.new_items:
            if item.type == "reasoning_item":
                _reasoning_dump += f"\nREASONING: {item.raw_item.content}\n"
        
        return OutputSchema(
            output_text=run_result.final_output.model_dump_json(),
            output_dict=run_result.final_output.model_dump(),
            reasoning_dump=_reasoning_dump
        )

# # Code entry point.
# async def run_workflow(workflow_text_input: WorkflowTextInput) -> OutputSchema:
    
#     workflow = workflow_text_input.model_dump()
#     input_text = workflow["input_as_text"]

#     run_result: RunResult = await Runner.run(
#         narrative_design_agent,
#         input=input_text
#     )

#     _reasoning_dump = ""
#     for item in run_result.new_items:
#         if item.type == "reasoning_item":
#             _reasoning_dump += f"\nREASONING: {item.raw_item.content}\n"

#     return OutputSchema(
#         output_text=run_result.final_output.model_dump_json(),
#         output_dict=run_result.final_output.model_dump(),
#         reasoning_dump=_reasoning_dump
#     )

#===============
# Testing logic
#===============


test_input: str = "A sequel to the cult film Manos, The Hands Of Fate"

# test_input: str = "A scary story about a derelict deep space station called the U.S.S. Calliope, where xeno-biological research was conducted." \
# "The player character is tasked with investigating why the station went dark, and recovering the precious research data."

async def main():
    #user_input: str = input("--> ")

    wf_input = WorkflowTextInput(
        input_as_text=test_input
    )

    test_agent: NarrativeDesignAgent = NarrativeDesignAgent()
    output: OutputSchema = await test_agent.run_workflow(wf_input)

    # output: OutputSchema = await run_workflow(wf_input)

    print(f"{json.dumps(output.output_dict, indent=2)}")


if __name__ == "__main__":
    asyncio.run(main())