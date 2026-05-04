from dotenv import load_dotenv
from pydantic import BaseModel
import asyncio
from pathlib import Path
import sys
from datetime import datetime
import os

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignAgent, NarrativeDesignOutputSchema, WorkflowTextInput, SceneData
from scene_beat_agent import SceneBeatAgent, SceneBeatSheet
from prompt_catalog import ImageStyle
from image_generator import ImageGenerator, ArtAssetManifest
from tools.foo import get_uuid_string


class DemoCreativeData(BaseModel):
    narrative_design_spec: NarrativeDesignOutputSchema
    art_assets: ArtAssetManifest
    beat_sheets: list[SceneBeatSheet]

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

async def run_program(user_input: str):

    temp_game_name: str = get_uuid_string()
    image_style = ImageStyle.PULP

    # STAGE 1: generate a story plan and extract needed data
    print(f"{get_dt_str()}\nGenerating story plan for user concept:\n{user_input}\n\n")
    wf: WorkflowTextInput = WorkflowTextInput(
        input_as_text=user_input
    )
    nd_out: NarrativeDesignOutputSchema = await NarrativeDesignAgent().run_workflow(wf) #####
    nd_out_json: str = nd_out.model_dump_json(indent=2)

    intro_scene_uuid: str = nd_out.intro_scene.scene_data.uuid
    first_scene_uuid: str = nd_out.act_one[0].scene_data.uuid

    # STAGE 2: Art assets and scene beats
    stage_two_coroutines = [
        ImageGenerator().get_demo_manifest(temp_game_name, nd_out_json, image_style), # returns ArtAssetManifest
        SceneBeatAgent().run_workflow(nd_out_json, intro_scene_uuid),
        SceneBeatAgent().run_workflow(nd_out_json, first_scene_uuid)
    ]
    stage_two_gather = asyncio.gather(*stage_two_coroutines)
    stage_two = await stage_two_gather
    art_manifest: ArtAssetManifest = stage_two[0] #####
    beat_sheet_list: list[SceneBeatSheet] = [
        stage_two[1],
        stage_two[2]
    ]

    creative_data: DemoCreativeData = DemoCreativeData(
        narrative_design_spec   = nd_out,
        art_assets              = art_manifest,
        beat_sheets             =beat_sheet_list
    )
    creative_data_json: str = creative_data.model_dump_json(indent=2)
    await write_output_json(temp_game_name, creative_data_json, 'creative_data')

    

    
    
    # await write_output_json(temp_game_name, nd_out_json, f'{temp_game_name}_story_plan')

    # story_title: str = nd_out.story_title
    # intro_uuid: str = nd_out.intro_scene.scene_data.uuid
    # first_scene_uuid: str = nd_out.act_one[0].scene_data.uuid
    
    # player_uuid: str = nd_out.player_character.character_data.uuid
    # demo_character_uuids: list[str] = []
    # demo_character_uuids.append(player_uuid)
    # intro_scene_data: SceneData = nd_out.intro_scene.scene_data
    # first_scene_data: SceneData = nd_out.act_one[0].scene_data
    # intro_npc_uuids             = get_npc_uuids_from_scene_data(intro_scene_data)
    # first_scene_npc_uuids       = get_npc_uuids_from_scene_data(first_scene_data)

    # if len(intro_npc_uuids) > 0:
    #     for npc_uuid in intro_npc_uuids:
    #         if npc_uuid not in demo_character_uuids:
    #             demo_character_uuids.append(npc_uuid)
    
    # if len(first_scene_npc_uuids) > 0:
    #     for npc_uuid in first_scene_npc_uuids:
    #         if npc_uuid not in demo_character_uuids:
    #             demo_character_uuids.append(npc_uuid)
    
    # # STAGE 1.5 portrait images
    
    # demo_character_count = len(demo_character_uuids)
    # portrait_coroutines = [
    #     ImageGenerator().run_character_portrait_workflow(
    #         temp_game_name, nd_out_json, _id, image_style
    #     ) for _id in demo_character_uuids
    # ]
    # portrait_gather = asyncio.gather(*portrait_coroutines) # * unpacks the coros
    # portrait_results = await portrait_gather
    # for r in portrait_results:
    #     print(f"SAVED PORTRAIT IMAGE: {r}")
    

    # # STAGE 2: background image assets & scene beats
    # print(f"\nGenerating background image assets and scene beats for story: {story_title}\n\n")
    # intro_loc_uuid: str = nd_out.intro_scene.scene_data.location_uuid
    # first_scene_loc_uuid: str = nd_out.act_one[0].scene_data.location_uuid

    # stage_two_gather = asyncio.gather(
    #     ImageGenerator().run_bg_workflow(temp_game_name, nd_out_json, intro_loc_uuid, image_style),
    #     ImageGenerator().run_bg_workflow(temp_game_name, nd_out_json, first_scene_loc_uuid, image_style),
    #     # TODO: character portraits
    #     SceneBeatAgent().run_workflow(nd_out_json, intro_uuid),
    #     SceneBeatAgent().run_workflow(nd_out_json, first_scene_uuid)
    # )
    # stage_two = await stage_two_gather

    # print(f"SAVED BG IMAGE: {stage_two[0]}")
    # print(f"SAVED BG IMAGE: {stage_two[1]}")

    # # NOTE TEMPORARY -- THESE INDEXES WILL CHANGE!!!!!
    # intro_bs: SceneBeatSheet        = stage_two[2]
    # intro_bs_json: str              = intro_bs.model_dump_json(indent=2)
    # first_scene_bs: SceneBeatSheet  = stage_two[3]
    # first_scene_bs_json: str        = first_scene_bs.model_dump_json(indent=2)

    # save_beats_gather = asyncio.gather(
    #     write_output_json(temp_game_name, intro_bs_json, 'intro_beat_sheet'),
    #     write_output_json(temp_game_name, first_scene_bs_json, 'first_scene_beat_sheet')
    # )
    # save_beats = await save_beats_gather
    # print(f"SAVED BEATS DATA: {save_beats[0]}")
    # print(f"SAVED BEATS DATA: {save_beats[1]}")

    # STAGE 3: Write dialog (TODO...)



if __name__ == "__main__":

    concept: str = input("--> ")
    if concept.lower() != "exit":
        asyncio.run(run_program(concept))


