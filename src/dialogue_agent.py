from dotenv import load_dotenv
from agents import Agent, Runner, RunResult
from pydantic import BaseModel, Field
from typing import Union, Literal, Annotated
from pathlib import Path
import sys
import asyncio
import json

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from scene_beat_agent import SceneBeatSheet, SceneBeat

load_dotenv()

class LineEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["line"]
    #       TODO: LineEvent fields

class ShowCharacterEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["show_character"]
    #       TODO: ShowCharacterEvent fields

class HideCharacterEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["hide_character"]
    #       TODO: HideCharacterEvent fields

class SetBackgroundEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["set_background"]
    #       TODO: SetBackground fields

class NarrationEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["narration"]
    #       TODO: NarrationEvent fields

NonChoiceDialogueEvent = Annotated[
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
    option_id: str                                  = Field(..., description="...")
    option_text: str                                = Field(..., description="...")
    branch_label: str                               = Field(..., description="...")
    branch_events: list[NonChoiceDialogueEvent]     = Field(..., description="...") # 

class ChoiceEvent(BaseModel):
    """...""" # TODO: class docstring
    type: Literal["choice"]
    choice_id: str                      = Field(..., description="...") # TODO: field description
    prompt: str                         = Field(..., description="...") # TODO: field description
    options: list[DialogueChoiceOption] = Field(..., description="...") # TODO: field description
    ends_beat: bool                     = Field(..., description="...") # TODO: field description

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
    beat_index: int             = Field(..., description="...") # TODO: field description
    beat_name: str              = Field(..., description="...") # TODO: field description
    source_purpose: str         = Field(..., description="...") # TODO: field description
    source_exit_state: str      = Field(..., description="...") # TODO: field description
    events: list[DialogueEvent] = Field(..., description="...") # TODO: field description

class DialogueScene(BaseModel):
    scene_uuid: str                     = Field(..., description="...") # TODO: field description
    scene_name: str                     = Field(..., description="...") # TODO: field description
    location_uuid: str                  = Field(..., description="...") # TODO: field description
    dialogue_beats: list[DialogueBeat]  = Field(..., description="...") # TODO: field description
    scene_exit_state: str               = Field(..., description="...") # TODO: field description

# The DialogueAgent is the last thing I'll do. Ignore this for now.
class DialogueAgent():
    async def run_workflow(self, beat_sheet_json: str) -> DialogueScene:
        try:
            beat_sheet: SceneBeatSheet = SceneBeatSheet.model_validate_json(beat_sheet_json)
        except Exception as e:
            print(e)


async def main():
    dialogue_scene_schema = json.dumps(DialogueScene.model_json_schema(), indent=2)
    dialogue_beat_schema = json.dumps(DialogueBeat.model_json_schema(), indent=2)
    dialogue_choice_option_schema = json.dumps(DialogueChoiceOption.model_json_schema(), indent= 2)

    choice_event_schema = json.dumps(ChoiceEvent.model_json_schema(), indent=2)
    narration_event_schema = json.dumps(NarrationEvent.model_json_schema(), indent=2)
    set_bg_event_schema = json.dumps(SetBackgroundEvent.model_json_schema(), indent=2)
    show_char_event_schema = json.dumps(ShowCharacterEvent.model_json_schema(), indent=2)
    hide_char_event_schema = json.dumps(HideCharacterEvent.model_json_schema(), indent=2)
    line_event_schema = json.dumps(LineEvent.model_json_schema(), indent=2)

    print("=========SCHEMAS==========\n\n")
    print(f"=== DialogueScene ===\n{dialogue_scene_schema}\n\n")
    print(f"=== DialogueBeat ===\n{dialogue_beat_schema}\n\n")
    print(f"=== DialogueChoiceOption ===\n{dialogue_choice_option_schema}\n\n")





if __name__ == "__main__":
    asyncio.run(main())