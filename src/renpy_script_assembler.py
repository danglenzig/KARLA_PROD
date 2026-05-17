import sys
from pathlib import Path
from pydantic import BaseModel
import asyncio

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from image_generator import ArtAssetManifest
from dialogue_agent import DialogueScene, DialogueBeat, DialogueEvent, BranchEvent, SetBackgroundEvent, ChoiceEvent, HideCharacterEvent, LineEvent, NarrationEvent, ShowCharacterEvent
from gui_color_agent import GuiColorScheme

class DemoBuildData(BaseModel):
    art_assets: ArtAssetManifest
    dialogue_scenes: list[DialogueScene]
    gui_colors: GuiColorScheme
    character_dict: dict[str, str]

class RenPyScriptAssembler():

    def _get_set_background_code(self, event: SetBackgroundEvent)->str:
        out_str = f"scene {event.location_uuid} at bg_xform with fade"
        return out_str
    
    def _get_line_code(self, event: LineEvent)->str:
        return "# line event code"
    
    def _get_narration_code(self, event: NarrationEvent)->str:
        return "# narration event code"
    
    def _get_show_character_code(self, event: ShowCharacterEvent)->str:
        return "# show character event code"
    
    def _get_hide_character_code(self, event: HideCharacterEvent)->str:
        return "# hide character event code"
    
    def _get_choice_code(self, event: ChoiceEvent)->str:
        return "# choice event code"

    renpy_code_functions: dict = {
        'set_background': _get_set_background_code,
        'line': _get_line_code,
        'narration': _get_narration_code,
        'show_character': _get_show_character_code,
        'hide_character': _get_hide_character_code,
        'choice': _get_choice_code
    }

    async def run_workflow(self, data: DemoBuildData):

        char_names_by_uuid = data.character_dict
        intro_scene: DialogueScene = data.dialogue_scenes[0]
        first_scene: DialogueScene = data.dialogue_scenes[1]

        for beat in intro_scene.dialogue_beats:
            beat_events: list[DialogueEvent] = beat.events

            for event in beat_events:
                if event.type in self.renpy_code_functions:
                    print(self.renpy_code_functions[event.type](self, event))
                else:
                    raise Exception("UNKOWN EVENT TYPE!")
                


async def main():
    with open('KARLA_GAMES/threnody _protocol/DATA/build_data.json', 'r') as f:
        build_data_json = f.read().strip()

    bd: DemoBuildData = DemoBuildData.model_validate_json(build_data_json)
    await RenPyScriptAssembler().run_workflow(bd)

if __name__ == "__main__":
    asyncio.run(main())
