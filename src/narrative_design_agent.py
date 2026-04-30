# src/narrative_design_agent.py
# this is the main file for the narrative design agent. It will contain the main logic for generating the story, 
# characters, and dialogue for the visual novel game. It will also define the output schema for the narrative 
# design agent, which will be used to structure the output data that is given to downstream agents.

import asyncio
from pydantic import BaseModel, Field
from agents import Agent, ModelSettings, TResponseInputItem, Runner, RunResult, RunConfig, trace, function_tool
from openai.types.shared.reasoning import Reasoning




class CharacterData(BaseModel):
    name: str                       = Field(..., description="The name of the character")
    portrait_image_prompt: str      = Field(..., description="A descriptive prompt to generate the dialogue portrait image of the character")
    dialogue_examples: list[str]    = Field(..., description="A list of example dialogue lines for the character. These will be used to generate actual dialogue lines for the character in the game.")

class LocationData(BaseModel):
    name: str                       = Field(..., description="The name of the location")
    location_image_prompt: str      = Field(..., description="A descriptive prompt to generate the background image of the location")

class Location(BaseModel):
    location_data: LocationData      = Field(..., description="The data for the location, including name and location image prompt")

class PlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the player character, including name, portrait image prompt, and dialogue examples")

class NonPlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the non-player character, including name, portrait image prompt, and dialogue examples")

class SceneData(BaseModel):
    location:Location                 = Field(..., description="The data for the location of the scene")
    non_player_characters: list[NonPlayerCharacter] = Field(..., description="A list of non-player characters that are present in the scene")
    narrtive_summary: str = Field(..., description="A brief summary of the narrative that takes place in the scene. This will be used to generate the dialogue and player choices for the scene.")    

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


class WorkflowTextInput(BaseModel):
    input_as_text: str = Field(..., description="The high-level concept for the story")


# Code entry point.
async def run_workflow(workflow_text_input: WorkflowTextInput):
    pass


async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())