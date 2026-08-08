from typing import Literal, Annotated, Union
from pydantic import (
    BaseModel, ValidationError, Field
)

class LineEvent(BaseModel):
    """A line of dialogue spoken by a character."""
    type: Literal["line"]
    character_uuid: str = Field(..., description="The UUID of the character speaking this line.")
    text: str = Field(..., description="The spoken dialogue text.")

class NarrationEvent(BaseModel):
    """A line of narration shown in the dialogue box."""
    type: Literal["narration"]
    text: str = Field(..., description="The narration text.")

class ShowCharacterEvent(BaseModel):
    """Display a character portrait on screen."""
    type: Literal["show_character"]
    character_uuid: str = Field(..., description="The UUID of the character to display.")
    character_expression: Literal['neutral', 'happy', 'sad', 'surprised', 'angry', 'confused', 'cocky'] = Field(
        ...,
        description="The facial expression and body language of the character."
    )
    screen_position: Literal['left', 'center', 'right'] = Field(
        ...,
        description="The screen position for the displayed character portrait.",
    )

class HideCharacterEvent(BaseModel):
    """Remove a visible character portrait from the screen."""
    type: Literal["hide_character"]
    character_uuid: str = Field(..., description="The UUID of the character to hide.")

class SetBackgroundEvent(BaseModel):
    """Display a background image for the current location."""
    type: Literal["set_background"]
    location_uuid: str = Field(..., description="The UUID of the location to display as background.")

BranchEvent = Annotated[
    Union[
        LineEvent,
        NarrationEvent,
        ShowCharacterEvent,
        HideCharacterEvent,
        SetBackgroundEvent,
    ],
    Field(discriminator="type"),
]

class DialogueChoiceOption(BaseModel):
    """A single player-selectable option within a choice."""
    option_id: str = Field(
        ...,
        description="A short stable identifier for this option, for example 'flirt' or 'leave'.",
    )
    option_text: str = Field(
        ...,
        description="The text shown to the player for this option.",
    )
    branch_events: list[BranchEvent] = Field(
        ...,
        min_length=1,
        description="The non-choice events triggered after this option is selected.",
    )

class ChoiceEvent(BaseModel):
    """A player choice event that presents multiple selectable options."""
    type: Literal["choice"]
    choice_id: str = Field(
        ...,
        description="A stable choice identifier, for example 'act1_scene1_beat_02_choice_01'.",
    )
    prompt: str = Field(
        ...,
        description="A short description of the player decision.",
    )
    options: list[DialogueChoiceOption] = Field(
        ...,
        min_length=2,
        description="The list of dialogue choice options presented to the player.",
    )
    ends_beat: bool = Field(
        ...,
        description="Whether this choice event ends the current beat.",
    )

DialogueEvent = Annotated[
    Union[
        LineEvent,
        NarrationEvent,
        ShowCharacterEvent,
        HideCharacterEvent,
        SetBackgroundEvent,
        ChoiceEvent,
    ],
    Field(discriminator="type"),
]

class DialogueBeat(BaseModel):
    """A structured dialogue beat within a scene."""
    beat_index: int = Field(
        ...,
        ge=1,
        description="The 1-based position of this dialogue beat in the scene.",
    )
    beat_name: str = Field(
        ...,
        description="A stable beat identifier, for example 'act1_scene1_beat_01'.",
    )
    source_purpose: str = Field(
        ...,
        description="Why this dialogue beat exists in the scene.",
    )
    source_exit_state: str = Field(
        ...,
        description="What has changed by the end of the beat.",
    )
    events: list[DialogueEvent] = Field(
        ...,
        min_length=1,
        description="The ordered list of dialogue events in this beat.",
    )

class DialogueScene(BaseModel):
    """The complete dialogue output for a single scene."""
    scene_uuid: str = Field(..., description="The UUID for this scene.")
    scene_name: str = Field(
        ...,
        description="The stable identifier for this scene.",
    )
    location_uuid: str = Field(
        ...,
        description="The UUID of this scene's location.",
    )
    dialogue_beats: list[DialogueBeat] = Field(
        ...,
        min_length=1,
        description="The ordered list of dialogue beats in this scene.",
    )
    scene_exit_state: str = Field(
        ...,
        description="What changes by the end of the scene.",
    )
    notes_and_work_product_summary: str = Field(
        ...,
        description="A brief summary of your workflow output, and any notes that might be helpful to the RenPy program assembler agent."
    )

class CharacterDialogueData(BaseModel):
    character_uuid: str
    character_name: str
    character_description: str
    example_dialogue_lines: list[str]

