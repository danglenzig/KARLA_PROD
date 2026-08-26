# src/karla_main/karla_main.py

import asyncio
from pathlib import Path
import os
import json
from camel_converter import to_snake

from pathlib import Path
import sys

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))


from misc_models.misc_models import (
    DemoCreativeData,
    DemoBuildData
)

from discovery_agent.discovery_agent_models import StoryConcept
from gui.chat_window import KarlaGUI

from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    NarrativeDesignContentValidationResult
)
from narrative_design_agent.narrative_design_agent import NarrativeDesignAgent
from narrative_design_agent.narrative_design_content_validator import get_nd_spec_validation_results

#from image_generator_agent.image_styles import ImageStyle
from image_generator_agent.image_generator_models import ArtAssetManifest
from image_generator_agent.image_generator_agent import ImageGenerator

from beat_sheet_agent.beat_sheet_models import SceneBeatSheet
from beat_sheet_agent.beat_sheet_agent import SceneBeatAgent

from gui_colors_agent.gui_colors_models import GuiColorScheme
from gui_colors_agent.gui_colors_agent import GuiColorAgent

from dialogue_agent.dialogue_agent_models import DialogueScene
from dialogue_agent.dialogue_agent import DialogueAgent

from renpy_script_assembler.renpy_script_assembler import RenPyScriptAssembler
from renpy_deployment.renpy_publisher import RenPyPublisher

def get_data_folder_path(game_name: str)->str:
    try:
        games_folder_path = os.getenv('GAMES_FOLDER_PATH')
        data_folder_name = os.getenv('CREATION_DATA_FOLDER_NAME')
        if not os.path.isdir(games_folder_path):
            os.mkdir(games_folder_path)
        if not os.path.isdir(f"{games_folder_path}/{game_name}"):
            os.mkdir(f"{games_folder_path}/{game_name}")
        if not os.path.isdir(f"{games_folder_path}/{game_name}/{data_folder_name}"):
            os.mkdir(f"{games_folder_path}/{game_name}/{data_folder_name}")
        return f"{games_folder_path}/{game_name}/{data_folder_name}"
    except Exception as e:
        print(e)

async def write_json_data(game_name: str ,in_json: str, filename: str):
    folder_path: str = get_data_folder_path(game_name)
    file_path: str = f"{folder_path}/{filename}"
    try:
        with open(file_path, 'w') as f:
            f.write(in_json)
    except Exception as e:
        print(e)

async def write_rpy_script(game_name: str, script: str, filename: str)->str:
    games_folder_path = os.getenv('GAMES_FOLDER_PATH')
    rpy_folder_name = os.getenv('RENPY_SCRIPTS_FOLDER_NAME')
    if not os.path.isdir(games_folder_path):
        os.mkdir(games_folder_path)
    if not os.path.isdir(f"{games_folder_path}/{game_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}")
    if not os.path.isdir(f"{games_folder_path}/{game_name}/{rpy_folder_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}/{rpy_folder_name}")
    script_path = f"{games_folder_path}/{game_name}/{rpy_folder_name}/{filename}"
    with open(script_path, 'w') as f:
        f.write(script)
    return script_path

class KarlaMain():
    def __init__(self):
        self.game_title: str = ""
        self.story_concept: StoryConcept | None = None
        self.nd_output: NarrativeDesignOutput | None = None
        self.nd_validation: NarrativeDesignContentValidationResult | None = None
        self.creative_data: DemoCreativeData | None = None
        self.dialogue_scene_lists: list[DialogueScene] | None = None
        self.build_data: DemoBuildData | None = None
        self.script_path: str = ""
        self.callback_dict: dict[str, callable] = {
            'set_story_concept': self.set_story_concept
        } # currently contains only one thing, but want to keep it as dict for future flexibility

    async def get_narrative_design(self):
        if not self.story_concept:
            raise ValueError("### KarlaMain: Can't generate nd_output because story_concept is None")
        
        #self.karla_gui.window["-STATUS-"].update(f"Status: generating narrative design spec...")
        # ^^NO! send an event instead
        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: generating narrative design spec...")
        self.nd_output = await NarrativeDesignAgent().run_workflow_streaming(self.story_concept)

        self.nd_validation = get_nd_spec_validation_results(self.nd_output)
        if self.nd_validation.has_problems:
            raise ValueError(f"### KarlaMain: NarrativeDesignAgent output content validation failed:\n\n{self.nd_validation.comments}")
        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: narrative design output validated. writing jsons...")
        print("### KarlaMain: NarrativeDesignAgent output content validated")

        self.game_title = to_snake(self.nd_output.story_title).replace(" ","")

        stage_two_json_dumps = [
            write_json_data(self.game_title, self.story_concept.model_dump_json(indent=2), "story_concept.json"),
            write_json_data(self.game_title, self.nd_output.model_dump_json(indent=2), "narrative_design_output.json")
        ]
        stage_two_gather = asyncio.gather(*stage_two_json_dumps)
        await stage_two_gather                 

        #========================
        # Stage 2 is now complete
        #========================
        # we don't need to come back to this function, so use asyncio.run(...), versus await
        asyncio.run(self.get_art_assets_and_scene_beats())

    async def get_art_assets_and_scene_beats(self):
        if not self.nd_output:
            raise ValueError("### KarlaMain: Can't generate art assets because nd_output is None")

        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: gathering art assets and scene beats...")

        stage_three_coroutines = [
            ImageGenerator().get_demo_manifest(self.game_title, self.nd_output), # gets art assets for intro and act1 scene 1 only
            SceneBeatAgent().run_workflow(self.nd_output, self.nd_output.intro_scene.scene_data.uuid), # intro beats
            SceneBeatAgent().run_workflow(self.nd_output, self.nd_output.act_one[0].scene_data.uuid), # scene 1 beats
            GuiColorAgent().run_workflow(self.nd_output)
        ]

        stage_three_gather   = asyncio.gather(*stage_three_coroutines)
        stage_three_products = await stage_three_gather

        art_manifest: ArtAssetManifest        = stage_three_products[0]
        intro_beats: SceneBeatSheet           = stage_three_products[1]
        first_scene_beats: SceneBeatSheet     = stage_three_products[2]
        color_scheme: GuiColorScheme          = stage_three_products[3]
        beat_sheet_list: list[SceneBeatSheet] = [intro_beats, first_scene_beats]

        self.creative_data = DemoCreativeData(
            concept               = self.story_concept,
            narrative_design_spec = self.nd_output,
            art_assets            = art_manifest,
            beat_sheets           = beat_sheet_list,
            color_scheme          = color_scheme
        )

        await write_json_data(self.game_title, self.creative_data.model_dump_json(indent=2), "creative_data.json")

        #========================
        # Stage 3 is now complete
        #========================

        asyncio.run(self.get_dialogue_scenes())

    async def get_dialogue_scenes(self):
        if not self.creative_data:
            raise ValueError("### KarlaMain: Can't generate dialogue scenes because creative_data is None")

        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: creating dialogues and branching...")

        stage_four_coroutines = [
            DialogueAgent().run_scene_workflow(self.nd_output, self.creative_data.beat_sheets[0]), # intro
            DialogueAgent().run_scene_workflow(self.nd_output, self.creative_data.beat_sheets[1]), # act1 scene1
        ]

        stage_four_gather         = asyncio.gather(*stage_four_coroutines)
        self.dialogue_scene_lists = await stage_four_gather

        #========================
        # Stage 4 is now complete
        #========================

        asyncio.run(self.build_renpy_assets())

    async def build_renpy_assets(self):
        if not self.dialogue_scene_lists or len(self.dialogue_scene_lists <= 0):
            raise ValueError("### KarlaMain: Can't generate renpy assets because dialogue_scene_lists is None or empty")

        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: creating .rpy scripts...")

        char_dict: dict[str,str] = {}
        character_catalogue = self.nd_output.get_character_catalog()
        for id in character_catalogue:
            char_dict[id] = character_catalogue[id]['name']

        self.build_data = DemoBuildData(
            art_assets      = self.creative_data.art_assets,
            dialogue_scenes = self.dialogue_scene_lists,
            gui_colors      = self.creative_data.color_scheme,
            character_dict  = char_dict
        )

        await write_json_data(self.game_title, self.build_data.model_dump_json(indent=2), 'build_data.json')
        script_rpy = await RenPyScriptAssembler().run_workflow(self.build_data)
        self.script_path: str = await write_rpy_script(self.game_title, script_rpy, 'script.rpy')

        #========================
        # Stage 5 is now complete
        #========================

        asyncio.run(self.publish_renpy_game())

    async def publish_renpy_game(self):
        if not self.build_data:
            raise ValueError("### KarlaMain: Can't publish because buiöd_data is None")

        self.karla_gui.window.write_event_value("-STATUS_UPDATE-", "Status: publishing Ren'Py game...")

        publish_success: bool = await RenPyPublisher().run_workflow(
            game_title       = self.game_title,
            script_file_path = self.script_path,
            art_manifest     = self.creative_data.art_assets
        )

        if not publish_success:
            raise RuntimeError("### KarlaMain: Publishing stage failed")
        


    def set_story_concept(self, delivered_concept: StoryConcept):
        #========================
        # Stage 1 is now complete
        #========================

        if delivered_concept:
            self.story_concept = delivered_concept
            print(f"""
### KarlaMain: Story concept is set:
{self.story_concept.model_dump_json(indent = 2)}
""")
        #=================================================
        # Kick off Stage 2: Generate narrative design spec
        #=================================================
        # This function is not async, so use asyncio.run(...), versus await (and so on down the pipeline...)
        asyncio.run(self.get_narrative_design(self.story_concept))



    def run(self):
        self.karla_gui: KarlaGUI = KarlaGUI()

        #=============================
        # Kicks off Stage 1: Discovery
        #=============================
        self.karla_gui.run(self.callback_dict)

def main():
    KarlaMain().run()

if __name__ == "__main__":
    main()

