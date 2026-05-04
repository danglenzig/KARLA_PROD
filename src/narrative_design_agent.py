# src/narrative_design_agent.py
# this is the main file for the narrative design agent. It will contain the main logic for generating the story, 
# characters, and dialogue for the visual novel game. It will also define the output schema for the narrative 
# design agent, which will be used to structure the output data that is given to downstream agents.

import asyncio
from pydantic import BaseModel, Field
from typing import Optional
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
    uuid: str                       = Field(..., description="A unique UUID string for this character")
    name: str                       = Field(..., description="The name of the character")
    portrait_image_prompt: str      = Field(..., description="A descriptive prompt to generate the dialogue portrait image of the character")
    dialogue_examples: list[str]    = Field(..., description="A list of example dialogue lines for the character. These will be used to generate " \
    "actual dialogue lines for the character in the game.")


class LocationData(BaseModel):
    uuid: str                       = Field(..., description="A unique UUID string for this location")
    name: str                       = Field(..., description="The name of the location")
    location_image_prompt: str      = Field(..., description="A descriptive prompt to generate the background image of the location")

class Location(BaseModel):
    location_data: LocationData      = Field(..., description="The data for the location, including name and location image prompt")

class PlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the player character, including name, portrait image prompt, and dialogue examples")

class NonPlayerCharacter(BaseModel):
    character_data: CharacterData    = Field(..., description="The data for the non-player character, including name, portrait image prompt, and dialogue examples")

class SceneData(BaseModel):
    uuid: str                                           = Field(...,description="A unique UUID for this scene")
    scene_name: str                                     = Field(...,description="A human-readable, unique and stable ID for this scene. For example 'intro', 'outro', 'act1_scene1', 'act1_scene2', " \
    "'act2_scene1', 'act2_scene2', and so on.")
    location_uuid: str                                  = Field(..., description="The UUID of the scene's location")
    non_player_character_uuids: Optional[list[str]]     = Field(..., description="A list of UUIDs for any non-player characters that are present in the scene")
    narrtive_summary: str                               = Field(..., description="A brief summary of the narrative that takes place in the scene. This will be used to generate " \
    "the dialogue and player choices for the scene.")    

class Scene(BaseModel):
    scene_data: SceneData            = Field(..., description="The data for the scene, including location, non-player characters, and narrative summary")

class NarrativeDesignOutputSchema(BaseModel):
    story_title: str                                = Field(..., description="The title of the story")
    synopsis: str                                   = Field(..., description="A brief overview of the plot, setting, tone, and characters")
    player_character: PlayerCharacter               = Field(..., description="The story protagonist and player character of the visual novel")
    non_player_characters: list[NonPlayerCharacter] = Field(..., description="A list of non-player characters")
    locations: list[Location]                       = Field(..., description="A list of scene locations")
    intro_scene: Scene                              = Field(..., description="The first scene of the visual novel -- a prologue")
    act_one: list[Scene]                            = Field(..., description="An ordered list of scenes in the story's first act")
    act_two: list[Scene]                            = Field(..., description="An ordered list of scenes in the story's second act")
    act_three: list[Scene]                          = Field(..., description="An ordered list of scenes in the story's third act")
    outro_scene: Scene                              = Field(..., description="The final scene of the visual novel -- the story's denouement")

    def get_location_name(self, uuid: str) -> str:
        loc_name = "LOC NAME"
        loc_name = next(loc.location_data.name for loc in self.locations if loc.location_data.uuid == uuid)
        return loc_name
    
    def get_npc_name(self, uuid: str) -> str:
        npc_name = "NPC NAME"
        npc_name = next(npc.character_data.name for npc in self.non_player_characters if npc.character_data.uuid == uuid)
        return npc_name

    def human_readable(self) -> str:
        output_str = f"\nTITLE: {self.story_title}\n"
        output_str += f"\n\nSYNOPSIS: {self.synopsis}\n"
        
        output_str += f"\n\nPLAYER CHARCTER: {self.player_character.character_data.name}\n"
        output_str += f"\n  VISUAL: {self.player_character.character_data.portrait_image_prompt}\n"
        output_str += f"\n  DIALOGUE EXAMPLES:\n"
        for line in self.player_character.character_data.dialogue_examples:
            output_str += f"    '{line}'\n"
        output_str += f"\n  UUID: {self.player_character.character_data.uuid}\n"

        output_str += f"\n\nNON-PLAYER CHARACTERS:\n"
        for npc in self.non_player_characters:
            output_str += f"\n  NPC: {npc.character_data.name}\n"
            output_str += f"\n    VISUAL: {npc.character_data.portrait_image_prompt}\n"
            output_str += f"\n    DIALOGUE EXAMPLES:\n"
            for line in npc.character_data.dialogue_examples:
                output_str += f"      '{line}'\n"
            output_str += f"\n    UUID: {npc.character_data.uuid}\n"

        output_str += f"\n\nLOCATIONS:\n"
        for location in self.locations:
            output_str += f"\n  {location.location_data.name}:\n"
            output_str += f"\n    VISUAL: {location.location_data.location_image_prompt}\n"
            output_str += f"\n    UUID: {location.location_data.uuid}\n"
            
        output_str += f"\n\nINTRO:\n"
        loc_name = self.get_location_name(self.intro_scene.scene_data.location_uuid)
        output_str += f"\n  LOCATION: {loc_name}\n"

        if 'non_player_character_uuids' in self.intro_scene.scene_data.__dict__:
            if not self.intro_scene.scene_data.non_player_character_uuids is None:
                output_str += f"\n  NON-PLAYER  CHARACTERS:\n"
                for npc_uuid in self.intro_scene.scene_data.non_player_character_uuids:
                    npc_name = self.get_npc_name(npc_uuid)
                    output_str += f"    {npc_name},\n"

        output_str += f"\n  SCENE SYNOPSIS: {self.intro_scene.scene_data.narrtive_summary}\n"

        output_str += f"\n\nACT I:\n"
        scene_idx = 1
        for scene in self.act_one:
            loc_name = self.get_location_name(scene.scene_data.location_uuid)
            output_str += f"\n  SCENE {scene_idx}, LOCATION {loc_name}\n"

            if 'non_player_character_uuids' in scene.scene_data.__dict__:

                if not scene.scene_data.non_player_character_uuids is None:
                    output_str += f"\n  NON-PLAYER CHARACTERS:\n"
                    for npc_uuid in scene.scene_data.non_player_character_uuids:
                        npc_name = self.get_npc_name(npc_uuid)
                        output_str += f"    {npc_name},\n"
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrtive_summary}\n"
            scene_idx += 1

        output_str += f"\n\nACT II:\n"
        scene_idx = 1
        for scene in self.act_two:
            loc_name = self.get_location_name(scene.scene_data.location_uuid)
            output_str += f"\n  SCENE {scene_idx}, LOCATION {loc_name}\n"

            if 'non_player_character_uuids' in scene.scene_data.__dict__:
                if not scene.scene_data.non_player_character_uuids is None:
                    output_str += f"\n  NON-PLAYER CHARACTERS:\n"
                    for npc_uuid in scene.scene_data.non_player_character_uuids:
                        npc_name = self.get_npc_name(npc_uuid)
                        output_str += f"    {npc_name},\n"
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrtive_summary}\n"
            scene_idx += 1
        
        output_str += f"\n\nACT III:\n"
        scene_idx = 1
        for scene in self.act_three:
            loc_name = self.get_location_name(scene.scene_data.location_uuid)
            output_str += f"\n  SCENE {scene_idx}, LOCATION {loc_name}\n"
            if 'non_player_character_uuids' in scene.scene_data.__dict__:
                if not scene.scene_data.non_player_character_uuids is None:
                    output_str += f"\n  NON-PLAYER CHARACTERS:\n"
                    for npc_uuid in scene.scene_data.non_player_character_uuids:
                        npc_name = self.get_npc_name(npc_uuid)
                        output_str += f"    {npc_name},\n"
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrtive_summary}\n"
            scene_idx += 1

        output_str += f"\n\nOUTRO:\n"
        loc_name = self.get_location_name(self.outro_scene.scene_data.location_uuid)
        output_str += f"\n  LOCATION: {loc_name}\n"

        if 'non_player_character_uuids' in self.outro_scene.scene_data.__dict__:
            if not self.outro_scene.scene_data.non_player_character_uuids is None:
                output_str += f"\n  NON-PLAYER  CHARACTERS:\n"
                for npc_uuid in self.outro_scene.scene_data.non_player_character_uuids:
                    npc_name = self.get_npc_name(npc_uuid)
                    output_str += f"    {npc_name},\n"
        
        output_str += f"\n  SCENE SYNOPSIS: {self.outro_scene.scene_data.narrtive_summary}\n"

        return output_str
    
    def get_location_catalog(self) -> dict[dict]:
        """Returns a catalog of game locations, indexed by UUID"""
        data: dict = {}
        for loc in self.locations:
            loc_key = loc.location_data.uuid
            loc_data = loc.location_data.model_dump()
            data[loc_key] = loc_data
        return data

    def get_character_catalog(self) -> dict[dict]:
        """Returns a catalog of game characters, indexed by UUID"""
        data: dict = {}
        player_key = self.player_character.character_data.uuid
        player_data = self.player_character.character_data.model_dump()
        data[player_key] = player_data
        for npc in self.non_player_characters:
            npc_key = npc.character_data.uuid
            npc_data = npc.character_data.model_dump()
            data[npc_key] = npc_data
        return data
    
    def get_scene_catalog(self) -> dict[dict]:
        """Returns a catalog of game scenes, indexed by UUID"""
        data: dict = {}        
        intro_key = self.intro_scene.scene_data.uuid
        data[intro_key] = self.intro_scene.scene_data.model_dump()
        for scene in self.act_one:
            scene_key = scene.scene_data.uuid
            data[scene_key] = scene.scene_data.model_dump()
        outro_key = self.outro_scene.scene_data.uuid
        data[outro_key] = self.outro_scene.scene_data.model_dump()
        return data



class WorkflowTextInput(BaseModel):
    input_as_text: str = Field(..., description="The high-level concept for the story")

#===============
# Function Tools
#===============

def generate_uuid():
    myuuid = uuid.uuid4()
    return str(myuuid)

@function_tool
def get_uuid_string() -> str:
    """Returns a unique UUID string"""
    return generate_uuid()

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

Use the get_uuid_string tool to get UUID strings.

IMPORTANT: Remember that your visual descriptions will serve as input prompts AI image-generation agents. The image outputs of those agents will be the image assets for a Ren'Py visual novel game. In your character descriptions describe ONLY the character, not their surroundings, lighting, etc. The image generation agent already has strict rules about framing, composition, etc. so don't mention anything that might confuse it.
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

    async def run_workflow(self, workflow_text_input: WorkflowTextInput) -> NarrativeDesignOutputSchema:
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
        
        return run_result.final_output

#===============
# Testing logic
#===============

# to unit test, run as module from project root:
#   python3 -m src.narrative_design_agent

#test_input: str = "A sequel to the cult film Manos, The Hands Of Fate"

#test_input: str = "A scary story about a derelict deep space station called the U.S.S. Calliope, where xeno-biological research was conducted." \
#"The player character is tasked with investigating why the station went dark, and recovering the precious research data."



async def main():
    print(generate_uuid())

    # test_input: str = "A scary story about an abandoned roadside motel in the rural New Mexico desert. The story is set in the year 1982."

    # wf_input = WorkflowTextInput(
    #     input_as_text=test_input
    # )

    # #test_agent: NarrativeDesignAgent = NarrativeDesignAgent()
    # output: NarrativeDesignOutputSchema = await NarrativeDesignAgent().run_workflow(wf_input)

    # print(f"{output.model_dump_json(indent=2)}") # model_dump_json(): BaseModel -> clean JSON
    # print(output.human_readable())

    # # write the data to a dummy file
    # # with open('dummy_data.json', 'w') as f:
    # #     f.write(output.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())