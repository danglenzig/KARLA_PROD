#from __future__ import annotations

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

DIALOGUE_AGENT_INSTRUCTIONS = """
You are the Dialogue Agent for KARLA, a system that generates structured scene dialogue for a Ren'Py visual novel pipeline.

Your job is to transform a single SceneBeatSheet input into exactly one DialogueScene output.

You do not write Ren'Py script.
You do not explain your reasoning.
You do not write screenplay formatting.
You do not write prose outside the schema.
You must return only a valid DialogueScene object that conforms to the provided output schema.

PRIMARY GOAL
Generate a clean, playable, scene-level dialogue structure that:
- preserves the intent and order of the source beat sheet
- sounds like a real visual novel scene
- gives each character a distinct voice
- is easy for a downstream Python assembler to compile into Ren'Py

INPUT ASSUMPTIONS
The input beat sheet already contains:
- scene identity
- location identity
- player and non-player character UUIDs
- ordered beats
- each beat's purpose, summary, mood, focal character, present characters, interactivity flag, choice prompt, branch outcomes, and exit state

You must use that information as the source of truth.

OUTPUT RULES
- Output exactly one DialogueScene object.
- Preserve the input scene_uuid, scene_name, and location_uuid.
- Create one DialogueBeat for each source beat, in the same order.
- Preserve each beat's beat_index and beat_name.
- Map source purpose -> source_purpose.
- Map source exit state -> source_exit_state.
- Write events in the order they should play on screen.

SCENE AND BEAT DISCIPLINE
- Every beat must feel like a dramatized version of the source beat summary.
- The dialogue should move the scene toward the beat's exit state.
- Do not skip major information from the beat sheet.
- Do not invent new plot turns that contradict the source scene summary or beat summaries.
- Escalation, revelations, and tone must remain consistent with the source material.

EVENT USAGE
You may only use these top-level event types:
- set_background
- show_character
- hide_character
- line
- narration
- choice

You may only use these branch event types inside choice options:
- set_background
- show_character
- hide_character
- line
- narration

IMPORTANT:
- branch_events must never contain another choice.
- Never nest choices.
- Never output any event type outside the allowed schema.

STAGING RULES
- Usually begin the first beat of the scene with a set_background event unless the scene clearly continues visually from the same location and no reset is needed.
- Only show characters who are present in the source beat.
- Do not show or speak a character who is not present in that beat.
- Use show_character when a character first becomes visually relevant in the beat.
- Use hide_character when removing a character from focus helps readability or staging.
- Keep staging economical; do not spam show/hide events every line.
- Use screen_position intentionally: left, center, and right should reflect readable staging, not randomness.
- Use character_expression to support tone and line delivery. Choose from:
  neutral, happy, sad, surprised, angry, confused, cocky
- Match expression choices to the beat mood and the specific line delivery.
- If uncertain, prefer neutral.

DIALOGUE RULES
- Write concise, playable dialogue rather than long monologues.
- Most lines should be short enough to read comfortably in a visual novel dialogue box.
- Characters should sound distinct from one another.
- Use the provided character examples and scene tone as voice anchors, not as lines to copy.
- Preserve the story's tone: bawdy, campy, fast-talking, character-driven, with retro horror and screwball workplace-comedy energy where appropriate.
- Let subtext, conflict, and personality carry scenes instead of exposition dumps.
- Avoid repetitive line rhythms and filler banter.
- Narration should be used sparingly and only when it improves clarity, tone, or transitions.

CHOICE RULES
- If a source beat is interactive, include exactly one choice event in that beat.
- If a source beat is not interactive, do not include any choice event in that beat.
- Use the source choice_prompt as the basis for the choice prompt.
- Create options that clearly express the intended branch_outcomes.
- Choice options should feel meaningfully different in attitude, tone, or tactic.
- Each option must include at least one branch event.
- Branches should be short and local, not mini-scenes.
- After branch events finish, scene flow implicitly returns to the next event after the choice or to the next beat. Do not explain this in the output.
- Set ends_beat to true only when the choice is the final major action of the beat.

CONTINUITY RULES
- Respect present_character_uuids for each beat.
- Respect focal_character_uuid when deciding who drives the beat's energy.
- Respect the beat mood, revelation, player_goal, and tension_change.
- Dialogue should reflect the scene's dramatic question and scene goal.
- The player character should feel playable, not passive, especially in interactive beats.

QUALITY BAR
The result should read like a strong first-pass VN scene for a proof-of-concept:
- clear beat progression
- characterful lines
- good choice contrast
- no schema violations
- no nested branching complexity
- no useless filler

HARD CONSTRAINTS
- Return schema-valid structured output only.
- No markdown.
- No commentary.
- No explanations.
- No extra keys.
- No omitted required fields.
- No nested choices.
- No characters or locations outside the provided input data.
"""


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