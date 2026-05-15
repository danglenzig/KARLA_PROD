from dotenv import load_dotenv
from agents import Agent, Runner, RunResult
from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from pathlib import Path
import sys
import asyncio
import json
from enum import Enum

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from scene_beat_agent import SceneBeatSheet, SceneBeat

load_dotenv()   



class LineEvent(BaseModel):
    """A line of dialogue text is displayed in the dialogue text area"""
    type: Literal["line"]
    character_uuid: str = Field(..., description="The UUID of the character speaking this dialogue line")
    text: str           = Field(..., description="The text of the dialogue line itself")

class ShowCharacterEvent(BaseModel):
    """A character dialogue portrait is shown"""
    type: Literal["show_character"]
    character_uuid: str                                 = Field(..., description="The UUID of the character whose dialogue portrait is displayed")
    screen_position: Literal['center', 'left', 'right'] = Field(..., description="The screen position of the dialogue portrait: 'center', 'right', or 'left'")


class HideCharacterEvent(BaseModel):
    """A visible character portrait is removed"""
    type: Literal["hide_character"]
    character_uuid: str = Field(..., description="The UUID of the character whose dialogue portrait is to be un-displayed")

class SetBackgroundEvent(BaseModel):
    """A scene background image is shown"""
    type: Literal["set_background"]
    location_uuid: str = Field(..., description="The UUID of the location being displayed as a background image")

class NarrationEvent(BaseModel):
    """A line of narration text is displayed in the dialogue text area"""
    type: Literal["narration"]
    text: str = Field(..., description="The text of the narration line itself")

DialogueBranchEvent = Annotated[
    Union[
        LineEvent,
        ShowCharacterEvent,
        HideCharacterEvent,
        SetBackgroundEvent,
        NarrationEvent
    ],
    Field(discriminator="type")
]
class DialogueChoiceOption(BaseModel):
    """Contains information about the dialogue choice option"""
    option_id: str                                           = Field(..., description="A short, stable identifier for this choice option, for example 'flirt', or 'leave'")
    option_text: str                                         = Field(..., description="The text of this choice option that is presented to the player, for example 'Flirt with Jesse', or 'End conversation'")
    branch_label: str                                        = Field(..., description="An identifier for the narrative branch created by this choice option, for example 'flirt'")
    non_choice_dialogue_events: list[DialogueBranchEvent] = Field(..., description="A list of non-choice dialogue events that are triggered by this choice option")

class ChoiceEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["choice"]
    choice_name: str                    = Field(..., description="A stable choice name, for example act1_scene1_beat_02_choice_01")
    prompt: str                         = Field(..., description="Short description of the player decision")
    options: list[DialogueChoiceOption] = Field(..., description="A list of dialogue choice options presented to the player")
    ends_beat: bool                     = Field(..., description="Whether or not this choice event ends the current beat")


DialogueEvent = Annotated[
    Union[
        LineEvent,
        ChoiceEvent,
        ShowCharacterEvent,
        HideCharacterEvent,
        SetBackgroundEvent,
        NarrationEvent
    ],
    Field(discriminator="type")
]

class DialogueBeat(BaseModel):
    beat_index: int             = Field(..., description="1-based position of this dialogue beat in the scene")
    beat_name: str              = Field(..., description="Stable beat name, for example act1_scene1_beat_01.")
    source_purpose: str         = Field(..., description="Why this dialogue beat exists in the scene.")
    source_exit_state: str      = Field(..., description="What has changed by the end of the beat.")
    events: list[DialogueEvent] = Field(..., description="A list of dialogue events triggered by this dialogue beat")

class DialogueScene(BaseModel):
    scene_uuid: str                     = Field(..., description="The UUID for this scene")
    scene_name: str                     = Field(..., description="The human-readable, unique and stable ID for this scene.")
    location_uuid: str                  = Field(..., description="The UUID of this scene's location")
    dialogue_beats: list[DialogueBeat]  = Field(..., description="A list of dialogue beats in this scene")
    scene_exit_state: str               = Field(..., description="What changes by the end of the scene.")

# The DialogueAgent is the last thing I'll do. Ignore this for now.
class DialogueAgent():
    async def run_workflow(self, beat_sheet_json: str) -> DialogueScene:
        try:
            beat_sheet: SceneBeatSheet = SceneBeatSheet.model_validate_json(beat_sheet_json)
        except Exception as e:
            print(e)


async def main():
    dialogue_scene_schema = json.dumps(DialogueScene.model_json_schema(), indent=2)
    print(f"=== DialogueScene ===\n{dialogue_scene_schema}\n\n")





if __name__ == "__main__":
    asyncio.run(main())