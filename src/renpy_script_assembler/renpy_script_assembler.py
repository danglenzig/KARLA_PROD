import sys
from pathlib import Path
from typing import Literal
import random
import asyncio

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from image_generator_agent.image_generator_models import ArtAssetManifest
from misc_models.misc_models import DemoBuildData, DemoCreativeData
from dialogue_agent.dialogue_agent_models import (
    DialogueScene,
    DialogueBeat,
    BranchEvent,
    SetBackgroundEvent,
    ChoiceEvent,
    HideCharacterEvent,
    LineEvent,
    NarrationEvent,
    ShowCharacterEvent,
    DialogueChoiceOption,
    DialogueEvent,
    CharacterDialogueData
)
from dialogue_agent.dialogue_agent import DialogueAgent

_PREAMBLE = """
transform screen_right:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720 ("show" keyword needs you to set scale on both x and y)
    xoffset 640

transform screen_left:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720
    xoffset 0

transform screen_center:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720
    xoffset 320

transform bg_xform:
    xzoom 1.25
    # ^^ 1024 -> 1280 ("scene" keyword applies scale to both x and y)

label start:

"""

class RenPyScriptAssembler():

    _char_names: dict[str, str] = {}
    _current_scene_bg: str
    _choice_branches: dict[str,str] = {}

    def _fix_double_quotes(self, in_str: str)-> str:
        return(in_str.replace('"', "'"))

    def _get_set_background_code(self, event: SetBackgroundEvent)->str:
        return f"    scene bg {event.location_uuid} at bg_xform with fade\n\n"

    def _get_line_code(self, event: LineEvent)->str:
        try:
            speaker_name: str = self._fix_double_quotes(
                self._char_names[event.character_uuid]
            )
        except Exception as e:
            print(e)

        line: str = self._fix_double_quotes(event.text)

        return f"    \"{speaker_name}\" \"{line}\"\n\n"

    def _get_narration_code(self, event: NarrationEvent)->str:
        out_str: str = f"    scene bg {self._current_scene_bg} at bg_xform\n\n"
        line: str = self._fix_double_quotes(event.text)
        out_str += f"    \"{line}\"\n\n"
        return out_str

    def _get_show_character_code(self, event: ShowCharacterEvent)->str:
        position: Literal[
            'left',
            'center',
            'right'
        ] = event.screen_position
        screen_pos: str = f"screen_{position}"
        movein_str: str = "movein"
        match position:
            case 'left':
                movein_str += 'left'
            case 'right':
                movein_str += 'right'
            case _:
                if random.randint(0,1) == 0:
                    movein_str += 'left'
                else:
                    movein_str += 'right'
        return f"    show {event.character_uuid} at {screen_pos} with {movein_str}\n\n"

    def _get_hide_character_code(self, event: HideCharacterEvent)->str:
        return f"    hide {event.character_uuid}\n\n"

    def _get_option_branch_code(self, option: DialogueChoiceOption, option_label: str, rejoin_label: str):
        out_str: str = f"\nlabel {option_label}:\n\n"
        for event in option.branch_events:
            out_str += self.renpy_code_functions[event.type](self, event)

        out_str += f"    jump {rejoin_label}\n"

        #print(f"{out_str}\n\n")

        return out_str

    def _get_choice_code(self, event: ChoiceEvent)->str:
        choice_id: str = event.choice_id
        rejoin_label: str = f"{choice_id}_rejoin"
        out_str: str = f"    \"{event.prompt}\"\n"
        out_str += "    menu:\n"

        print(f"{event.choice_id} number of options: {len(event.options)}")
        print("\n\n")

        for option in event.options:

            option_label = f"{choice_id}_{option.option_id}"
            #print(option_label)

            out_str += f"        \"{option.option_text}\":\n"
            out_str += f"            jump {option_label}\n"
            option_code = self._get_option_branch_code(option, option_label, rejoin_label)
            #self._choice_branches[option.option_id] = option_code
            self._choice_branches[option_label] = option_code
        out_str += f"label {rejoin_label}:\n"
        out_str += f"    scene bg {self._current_scene_bg} at bg_xform\n\n"
        return out_str

    renpy_code_functions: dict = {
        'set_background': _get_set_background_code,
        'line': _get_line_code,
        'narration': _get_narration_code,
        'show_character': _get_show_character_code,
        'hide_character': _get_hide_character_code,
        'choice': _get_choice_code
    }

    async def run_workflow(self, data: DemoBuildData)->str:
        self._char_names = data.character_dict
        intro_scene: DialogueScene = data.dialogue_scenes[0]
        first_scene: DialogueScene = data.dialogue_scenes[1]

        script_rpy = f"{_PREAMBLE}"

        # THE INTRO SCENE
        self._current_scene_bg = intro_scene.location_uuid
        for beat in intro_scene.dialogue_beats:
            beat_events: list[DialogueEvent] = beat.events

            script_rpy += f"# ==== BEAT: {beat.beat_name} ====\n\n"

            for event in beat_events:
                if event.type in self.renpy_code_functions:
                    script_rpy += self.renpy_code_functions[event.type](self, event)
                else:
                    print("FOOOOOO!")
                    raise ValueError(f"### RenPyScriptAssembler: UNKNOWN EVENT TYPE: {event.type}")

        # ACT ONE, SCENE ONE
        self._current_scene_bg = first_scene.location_uuid
        for beat in first_scene.dialogue_beats:
            beat_events: list[DialogueEvent] = beat.events

            script_rpy += f"# ==== BEAT: {beat.beat_name} ====\n\n"

            for event in beat_events:
                if event.type in self.renpy_code_functions:
                    script_rpy += self.renpy_code_functions[event.type](self, event)
                else:
                    raise ValueError(f"### RenPyScriptAssembler: UNKNOWN EVENT TYPE: {event.type}")

        script_rpy += "\nreturn\n\n"




        script_rpy += "#==== Choice Option Branches ===="
        for branch in self._choice_branches:

            print(f"***{branch}****:\n{self._choice_branches[branch]}\n\n")

            script_rpy += f"\n{self._choice_branches[branch]}\n"

        return script_rpy

async def main():
    # use for module testing
    pass

if __name__ == "__main__":
    asyncio.run(main())