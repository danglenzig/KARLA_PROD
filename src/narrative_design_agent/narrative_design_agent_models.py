# src/narrative_design_agent/narrative_design_agent_models.py

from typing import Optional
from pydantic import (
    BaseModel, Field
)

class CharacterData(BaseModel):
    """
    A model representing a single character in the visual novel story
    """
    uuid: str                    = Field(..., description="A unique UUID string and stable identifier for this character")
    name: str                    = Field(..., description="The name of the character")
    portrait_image_prompt: str   = Field(..., description="A descriptive prompt to generate the dialogue portrait image of the character")
    dialogue_examples: list[str] = Field(..., description="A list of example dialogue lines for the character. These will be used to generate " \
    "actual dialogue lines for the character in the game.")

class LocationData(BaseModel):
    """
    A model representing a single location in the visual novel.
    """
    uuid: str                  = Field(..., description="A unique UUID string for this location")
    name: str                  = Field(..., description="The name of the location")
    location_image_prompt: str = Field(..., description="A descriptive prompt to generate the background image of the location")

class Location(BaseModel):
    """
    Specifies the LocationData for a particular location.
    """
    location_data: LocationData = Field(..., description="The data for the location, including name and location image prompt")

class PlayerCharacter(BaseModel):
    """
    Specifies the CharacterData for the visual novel's player character.
    """
    character_data: CharacterData = Field(..., description="The data for the player character, including name, portrait image prompt, and dialogue examples")

class NonPlayerCharacter(BaseModel):
    """
    Specifies the CharacterData for a particular NPC in the visual novel.
    """
    character_data: CharacterData = Field(..., description="The data for the non-player character, including name, portrait image prompt, and dialogue examples")

class SceneData(BaseModel):
    """
    A model representing a particular scene in the visual novel.
    """
    uuid: str                                       = Field(...,description="A unique UUID for this scene")
    scene_name: str                                 = Field(...,description="A human-readable, unique and stable ID for this scene. For example 'intro', 'outro', 'act1_scene1', 'act1_scene2', " \
    "'act2_scene1', 'act2_scene2', and so on.")
    location_uuid: str                              = Field(..., description="The UUID of the scene's location")
    non_player_character_uuids: Optional[list[str]] = Field(..., description="A list of UUIDs for any non-player characters that are present in the scene")
    narrative_summary: str                          = Field(..., description="A brief summary of the narrative that takes place in the scene. This will be used to generate " \
    "the dialogue and player choices for the scene.")

class Scene(BaseModel):
    """
    Specifies the SceneData for a particular scene.
    """
    scene_data: SceneData = Field(..., description="The data for the scene, including location, non-player characters, and narrative summary")

class NarrativeDesignOutput(BaseModel):
    """
    A model representing the structured output of the narrative design agent.
    """
    story_title: str = Field(..., description="The title of the story")
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
        """
        Returns the name string of the location with the provided UUID or "LOC NAME" if UUID not found.
        """
        loc_name = "LOC NAME"
        loc_name = next(loc.location_data.name for loc in self.locations if loc.location_data.uuid == uuid)
        return loc_name
    
    def get_npc_name(self, uuid: str) -> str:
        """
        Returns the name of the NPC with the provided UUID or "NPC NAME" if UUID not found.
        """
        npc_name = "NPC NAME"
        npc_name = next(npc.character_data.name for npc in self.non_player_characters if npc.character_data.uuid == uuid)
        return npc_name
    
    def get_scene_by_scene_synopsis(self) -> str:
        """
        Returns a human-readable scene-by-scene synopsis of the story.
        """
        output_str = f"\nTITLE: {self.story_title}\n"
        output_str += f"\n\nSTORY SYNOPSIS: {self.synopsis}\n"

        output_str += f"\n\nINTRO SCENE:\n"
        output_str += f"\n  SCENE SYNOPSIS: {self.intro_scene.scene_data.narrative_summary}\n"

        output_str += f"\n\nACT I:\n"
        scene_idx = 1
        for scene in self.act_one:
            output_str += f"\n  SCENE {scene_idx}:\n"
            output_str += f"\n    SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
            scene_idx += 1

        output_str += f"\n\nACT II:\n"
        scene_idx = 1
        for scene in self.act_two:
            output_str += f"\n  SCENE {scene_idx}:\n"
            output_str += f"\n    SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
            scene_idx += 1

        output_str += f"\n\nACT III:\n"
        scene_idx = 1
        for scene in self.act_three:
            output_str += f"\n  SCENE {scene_idx}:\n"
            output_str += f"\n    SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
            scene_idx += 1

        output_str += f"\n\nOUTRO SCENE:\n"
        output_str += f"\n  SCENE SYNOPSIS: {self.outro_scene.scene_data.narrative_summary}\n"

        return output_str
    
    def human_readable(self) -> str:
        """
        Returns a human-readable version of the entire narrative design agent output.
        """
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

        output_str += f"\n  SCENE SYNOPSIS: {self.intro_scene.scene_data.narrative_summary}\n"

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
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
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
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
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
            
            output_str += f"\n  SCENE SYNOPSIS: {scene.scene_data.narrative_summary}\n"
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
        
        output_str += f"\n  SCENE SYNOPSIS: {self.outro_scene.scene_data.narrative_summary}\n"

        return output_str
    
    def get_location_catalog(self) -> dict[dict]:
        """Returns a catalog of game locations, indexed by UUID"""
        data: dict = {}
        for loc in self.locations:
            loc_key = loc.location_data.uuid
            loc_data = loc.location_data.model_dump()
            data[loc_key] = loc_data
        return data

    def get_location_uuids(self)->list[str]:
        out_list: list[str] = []
        for loc in self.locations:
            out_list.append(loc.location_data.uuid)
        return out_list

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

    def get_character_uuids(self) -> list[str]:
        out_list: list[str] = []
        out_list.append(self.player_character.character_data.uuid)
        for npc in self.non_player_characters:
            out_list.append(npc.character_data.uuid)
        return out_list
    
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

class NarrativeDesignContentValidationResult(BaseModel):
    has_problems: bool = False
    comments: str = ""