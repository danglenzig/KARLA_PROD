from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
from pathlib import Path
import sys
from datetime import datetime
from camel_converter import to_camel, to_snake
import os
import json

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignAgent, NarrativeDesignOutputSchema, WorkflowTextInput, SceneData
from scene_beat_agent import SceneBeatAgent, SceneBeatSheet
from prompt_catalog import ImageStyle
from image_generator import ImageGenerator, ArtAssetManifest
from discovery_agent import DiscoveryAgent, StoryConcept
from tools.foo import get_uuid_string
from gui_color_agent import GuiColorAgent, GuiColorScheme
from dialogue_agent import DialogueAgent, DialogueScene
from renpy_script_assembler import DemoBuildData, RenPyScriptAssembler



class DemoCreativeData(BaseModel):
    narrative_design_spec: NarrativeDesignOutputSchema
    art_assets: ArtAssetManifest
    beat_sheets: list[SceneBeatSheet]
    color_scheme: GuiColorScheme

def get_data_folder_path(game_name: str) -> str:
    games_folder_path = os.getenv('GAMES_FOLDER_PATH')
    data_folder_name = os.getenv('CREATION_DATA_FOLDER_NAME')
    if not os.path.isdir(games_folder_path):
        os.mkdir(games_folder_path)
    if not os.path.isdir(f"{games_folder_path}/{game_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}")
    if not os.path.isdir(f"{games_folder_path}/{game_name}/{data_folder_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}/{data_folder_name}")
    return f"{games_folder_path}/{game_name}/{data_folder_name}"

def get_dt_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def write_output_json(game_name: str, in_json: str, filename: str):
    path: str = f'{get_data_folder_path(game_name)}/{filename}.json'
    with open(path, 'w') as f:
        f.write(in_json)
    return path

def get_npc_uuids_from_scene_data(sd: SceneData) -> list[str]:
    uuids: list[str] = []
    if 'non_player_character_uuids' in sd.__dict__:
        if not sd.non_player_character_uuids is None:
            for uuid in sd.non_player_character_uuids:
                uuids.append(uuid)
    return uuids

async def run_program():

    #temp_game_name: str = get_uuid_string()
    image_style = ImageStyle.CLEAN

    # STAGE 0: Interview the user and generate a concept

    concept: StoryConcept = await DiscoveryAgent().run_workflow()


    # STAGE 1: generate a story plan and extract needed data
    print(f"{get_dt_str()}\nGenerating story plan for user concept:\n{concept.concept_summary}\n\n")
    wf: WorkflowTextInput = WorkflowTextInput(
        input_as_text=concept.concept_summary
    )
    nd_out: NarrativeDesignOutputSchema = await NarrativeDesignAgent().run_workflow(wf) #####
    nd_out_json: str = nd_out.model_dump_json(indent=2)

    intro_scene_uuid: str = nd_out.intro_scene.scene_data.uuid
    first_scene_uuid: str = nd_out.act_one[0].scene_data.uuid

    game_title:str = nd_out.story_title
    game_title_snake_case = to_snake(game_title) 

    # STAGE 2: Art assets and scene beats
    stage_two_coroutines = [
        ImageGenerator().get_demo_manifest(game_title_snake_case, nd_out_json, image_style), # returns ArtAssetManifest
        #ImageGenerator().get_demo_manifest(temp_game_name, nd_out_json, image_style), # returns ArtAssetManifest
        SceneBeatAgent().run_workflow(nd_out_json, intro_scene_uuid),
        SceneBeatAgent().run_workflow(nd_out_json, first_scene_uuid),
        GuiColorAgent().run_workflow(nd_out_json)
    ]
    stage_two_gather = asyncio.gather(*stage_two_coroutines)
    stage_two = await stage_two_gather
    art_manifest: ArtAssetManifest = stage_two[0] #####
    beat_sheet_list: list[SceneBeatSheet] = [
        stage_two[1],
        stage_two[2]
    ]
    color_scheme_: GuiColorScheme = stage_two[3]

    creative_data: DemoCreativeData = DemoCreativeData(
        narrative_design_spec   = nd_out,
        art_assets              = art_manifest,
        beat_sheets             = beat_sheet_list,
        color_scheme            = color_scheme_
    )
    creative_data_json: str = creative_data.model_dump_json(indent=2)
    await write_output_json(game_title_snake_case, creative_data_json, 'creative_data')
    #await write_output_json(temp_game_name, creative_data_json, 'creative_data')


    # STAGE 3: The build stage
    stage_three_coroutines = [
        DialogueAgent().run_workflow(nd_out_json, beat_sheet_list[0].model_dump_json(indent=2)),
        DialogueAgent().run_workflow(nd_out_json, beat_sheet_list[1].model_dump_json(indent=2))
    ]
    stage_three_gather = asyncio.gather(*stage_three_coroutines)
    stage_three = await stage_three_gather

    dialogue_scenes_list: list[DialogueScene] = [
        stage_three[0],
        stage_three[1]
    ]

    char_dict: dict[str, str] = {}
    character_catalog = nd_out.get_character_catalog()
    for id in character_catalog:
        char_dict[id] = character_catalog[id]['name']


    build_data: DemoBuildData = DemoBuildData(
        art_assets=creative_data.art_assets,
        dialogue_scenes=dialogue_scenes_list,
        gui_colors=color_scheme_,
        character_dict=char_dict
    )
    build_data_json = build_data.model_dump_json(indent=2)
    await write_output_json(game_title_snake_case, build_data_json, 'build_data')

    rpy_script = await RenPyScriptAssembler().run_workflow(build_data)
    rpy_path = f"{get_data_folder_path(game_title_snake_case)}/script.rpy"
    with open(rpy_path, 'w') as f:
        f.write(rpy_script)



if __name__ == "__main__":

    asyncio.run(run_program())
    #data_schema = json.dumps(DemoCreativeData.model_json_schema(), indent=2)
    #print(data_schema)

