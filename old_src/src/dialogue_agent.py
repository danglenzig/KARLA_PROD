#from __future__ import annotations

from dotenv import load_dotenv
from agents import Agent, Runner, RunResult, ModelSettings
from openai.types.shared.reasoning import Reasoning
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
from narrative_design_agent import NarrativeDesignOutputSchema, SceneData, CharacterData, LocationData

load_dotenv()

MODEL: str = "gpt-5.4"

PREAMBLE = """
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
- preserves the end-to-end narrative continuity of the game's story
- sounds like a real visual novel scene
- gives each character a distinct voice
- is easy for a downstream program assembler agent to compile into Ren'Py command language

INPUT ASSUMPTIONS
The input beat sheet already contains:
- scene identity
- location identity
- player and non-player character UUIDs
- ordered beats
- each beat's purpose, summary, mood, focal character, present characters, interactivity flag, choice prompt, branch outcomes, and exit state

You must use that information as the source of truth.

The narrative design spec contains a detailed outline of the end to end story, and is provided to help you preserve end-to-end narrative continuity when you write the dialogue.

OUTPUT RULES
- Output exactly one DialogueScene object.
- Preserve the input character_uuid for each character, scene_uuid, scene_name, and location_uuid.
- Create one DialogueBeat for each source beat, in the same order.
- Preserve each beat's beat_index and beat_name.
- Map source purpose -> source_purpose.
- Map source exit state -> source_exit_state.
- Write events in the order they should play on screen.

SCENE AND BEAT DISCIPLINE
- Every beat must feel like a dramatized version of the source beat summary.
- The dialogue should move the scene toward the beat's exit state.
- Do not skip major information from the beat sheet.
- Do not invent new plot turns that contradict the source scene summary, beat summaries or end-to-end narrative.
- Escalation, revelations, and tone must remain consistent with the source material.

EVENT USAGE
You may only use these top-level event types:
- set_background: 
- show_character: Shows a character's dialogue portrait in the game display 
- hide_character: Removes a character's dialogue portrait from the game display.
- line: Displays a line of character dialogue
- narration: Displays a line of narration. A narration line has no speaker name, and no associated dialogue portrait.
- choice: Presents a dialogue choice to the player
When a character begins speaking, use show_character to display their dialogue portrait. When another character begins speaking, use hide_character to un-display the previous speaking character and show_character to display the current speaking character.
Remember that only one character dialogue portrait may be visible at a time, and ONLY when they are the speaker of the current line.
No dialogue portrait should be visible during narration lines. Use hide_character as needed before narration lines.

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
- Use hide_character when removing a character from focus.
- Only show one character at at time, and only when they are speaking.
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
- Preserve the story's tone: bawdy, campy, fast-talking, character-driven, with retro horror, screwball workplace-comedy, etc. energy where appropriate.
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
    notes_and_work_product_summary: str = Field(
        ...,
        description="A brief summary of your workflow output, and any notes that might be helpful to the RenPy program assembler agent."
    )


class CharacterDialogueData(BaseModel):
    character_uuid: str
    character_name: str
    character_description: str
    example_dialogue_lines: list[str]


# The DialogueAgent is the last thing I'll do. Ignore this for now.
class DialogueAgent():
    async def get_agent_instructions(self, nd_spec_json: str)->str:
        try:
            nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(nd_spec_json)
            #scene_bs: SceneBeatSheet = SceneBeatSheet.model_validate_json(scene_bs_json)
        except Exception as e:
            print(e)

        synopsis: str = nd_spec.get_scene_by_scene_synopsis()

        #=================
        # Add the preamble
        #=================
        instructions_str = "#======================\n# INSTRUCTIONS PREAMBLE\n#======================\n"
        instructions_str += f"{PREAMBLE}\n"

        #=============
        # Add synopsis
        #=============
        instructions_str += f"\n#==============\n# STORY CONTEXT\n#==============\n"
        instructions_str += f"""\nHere are scene-by-scene synopses of the whole story to help you preserve end-to-end narrative continuity:
{synopsis}\n"""
            
        return instructions_str



    async def run_workflow(self, nd_spec_json: str, scene_bs_json: str) -> DialogueScene:
        agent_instructions: str = await self.get_agent_instructions(nd_spec_json)
        agent: Agent = Agent(
            name="dialogue_agent",
            instructions=agent_instructions,
            model=MODEL,
            output_type=DialogueScene,
            model_settings=ModelSettings(
                reasoning=Reasoning(
                    effort="high"
                )
            )
        )
        
        scene_bs: SceneBeatSheet = SceneBeatSheet.model_validate_json(scene_bs_json)
        input_str = f"\n#======\n# INPUT\n#======\n"
        input_str += f"""\nProduce a DialogueScene output for the scene indicated by this beat sheet. The beat sheet contains contextual information about:
- scene identity
- location identity
- player and non-player character UUIDs
- ordered beats
- each beat's purpose, summary, mood, focal character, present characters, interactivity flag, choice prompt, branch outcomes, and exit state. Here is the beat sheet for this scene:
\n{scene_bs.model_dump_json(indent=2)}\n\n"""
        
        # add character data
        # player:
        nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(nd_spec_json)
        player_data = CharacterDialogueData(
            character_uuid=nd_spec.player_character.character_data.uuid,
            character_name=nd_spec.player_character.character_data.name,
            character_description=nd_spec.player_character.character_data.portrait_image_prompt,
            example_dialogue_lines = nd_spec.player_character.character_data.dialogue_examples
        )
        input_str += f"""\nHere is contextual information about the player character:
{player_data.model_dump_json(indent=2)}\n\n"""

        # npcs
        character_catalog = nd_spec.get_character_catalog()
        npcs_list: list[CharacterDialogueData] = []
        if not scene_bs.non_player_character_uuids is None:
            if len(scene_bs.non_player_character_uuids) > 0:
                for id in scene_bs.non_player_character_uuids:
                    char_dict = character_catalog[id]
                    char_name = char_dict["name"]
                    char_desc = char_dict["portrait_image_prompt"]
                    example_lines = char_dict["dialogue_examples"]
                    data: CharacterDialogueData = CharacterDialogueData(
                        character_uuid=id,
                        character_name=char_name,
                        character_description=char_desc,
                        example_dialogue_lines=example_lines
                    )
                    npcs_list.append(data)

        if len(npcs_list) > 0:
            npcs_info_str = ""
            for data in npcs_list:
                npcs_info_str += f"{data.model_dump_json(indent=2)}\n"
            input_str += f"""\nHere is contextual information about the non-player characters in this scene:
{npcs_info_str}\n"""

        
        #print(f"{input_str}\n\n\n")
        print(f"\nGenerating dialogue data for {scene_bs.scene_name}\n")
        run_result: RunResult = await Runner.run(
            agent,
            input=input_str
        )

        ds: DialogueScene = run_result.final_output

        return ds


async def main():

    with open('KARLA_GAMES/TEST_DATA/DATA/nd_spec.json', 'r') as f:
        nd_spec_json = f.read().strip()
    with open('KARLA_GAMES/TEST_DATA/DATA/intro_bs.json', 'r') as f:
        intro_bs_json = f.read().strip()
    with open('KARLA_GAMES/TEST_DATA/DATA/first_scene_bs.json', 'r') as f:
        first_scene_bs_json = f.read().strip()

    instructs: str = await DialogueAgent().get_agent_instructions(nd_spec_json)
    print(f"{instructs}\n\n\n")

    ds: DialogueScene = await DialogueAgent().run_workflow(nd_spec_json, first_scene_bs_json)
    print(ds.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())