# src/beat_sheet_agent/beat_sheet_models.py

from pydantic import BaseModel, Field, ValidationError
from typing import Literal, Optional

class SceneBeat(BaseModel):
    beat_index: int = Field(...,description="1-based position of this beat in the scene.")
    beat_name: str = Field(...,description="Stable beat name, for example act1_scene1_beat_01.")
    purpose: str = Field(...,description="Why this beat exists in the scene.")
    summary: str = Field(...,description="What happens in this beat, in 1-3 sentences.")
    location_uuid: str = Field(...,description="The UUID of the location where this beat takes place.")
    present_character_uuids: list[str] = Field(
        description="Player character UUID plus UUIDs of any NPCs actively present in the beat."
    )
    focal_character_uuid: Optional[str] = Field(
        default=None,
        description="The character driving the beat emotionally or narratively."
    )
    mood: str = Field(description="The emotional tone of the beat.")
    revelation: Optional[str] = Field(
        default=None,
        description="New information learned in this beat, if any."
    )
    tension_change: Literal["rise", "fall", "twist", "hold"] = Field(
        description="How this beat changes dramatic tension."
    )
    player_goal: Optional[str] = Field(
        default=None,
        description="What the player character is trying to do in this beat."
    )
    interactive: bool = Field(
        description="Whether this beat contains a player choice or interactive moment."
    )
    choice_prompt: Optional[str] = Field(
        default=None,
        description="Short description of the player decision, if interactive."
    )
    branch_outcomes: Optional[list[str]] = Field(
        default=None,
        description="High-level outcomes for the available choices, if interactive."
    )
    exit_state: str = Field(
        description="What has changed by the end of the beat."
    )

class SceneBeatSheet(BaseModel):
    story_title: str = Field(...,description="The title of the story")
    scene_name: str = Field(...,description="The human-readable, unique and stable ID for this scene.")
    scene_uuid: str = Field(...,description="The UUID for this scene.")
    source_scene_summary: str = Field(...,description="The narrative summary of this scene.")
    location_name: str = Field(...,description="The human-readable name of this scene's location")
    location_uuid: str = Field(...,description="The UUID of this scene's location")
    player_character_uuid: str = Field(...,description="The UUID of the player character")
    non_player_character_uuids: list[str] = Field(description="A list of the UUIDs for the non-player characters in this scene")
    dramatic_question: str = Field(
        description="The core uncertainty driving the scene."
    )
    scene_goal: str = Field(
        description="What the player character wants in the scene."
    )
    scene_turn: str = Field(
        description="What changes by the end of the scene."
    )
    beats: list[SceneBeat] = Field(
        description="Ordered beat list for this scene, usually 5-8 beats."
    )