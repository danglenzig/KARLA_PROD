from dotenv import load_dotenv
import asyncio
from pathlib import Path
import sys
from datetime import datetime
import os

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignAgent, NarrativeDesignOutputSchema, WorkflowTextInput
from scene_beat_agent import SceneBeatAgent, SceneBeatSheet
from prompt_catalog import ImageStyle
from image_generator import ImageGenerator
from tools.foo import get_uuid_string

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

async def run_program(user_input: str):

    temp_game_name: str = get_uuid_string()
    image_style = ImageStyle.COMIC

    # STAGE 1: generate a story plan
    print(f"{get_dt_str()}\nGenerating story plan for user concept:\n{user_input}\n\n")
    wf: WorkflowTextInput = WorkflowTextInput(
        input_as_text=user_input
    )
    nd_out: NarrativeDesignOutputSchema = await NarrativeDesignAgent().run_workflow(wf)
    nd_out_json: str = nd_out.model_dump_json(indent=2)
    await write_output_json(temp_game_name, nd_out_json, f'{temp_game_name}_story_plan')

    story_title: str = nd_out.story_title
    intro_uuid: str = nd_out.intro_scene.scene_data.uuid
    first_scene_uuid: str = nd_out.act_one[0].scene_data.uuid

    # STAGE 2: image assets & scene beats
    print(f"\nGenerating background image assets and scene beats for story: {story_title}\n\n")
    intro_loc_uuid: str = nd_out.intro_scene.scene_data.location_uuid
    first_scene_loc_uuid: str = nd_out.act_one[0].scene_data.location_uuid

    stage_two_gather = asyncio.gather(
        ImageGenerator().run_bg_workflow(temp_game_name, nd_out_json, intro_loc_uuid, image_style),
        ImageGenerator().run_bg_workflow(temp_game_name, nd_out_json, first_scene_loc_uuid, image_style),
        # TODO: character portraits
        SceneBeatAgent().run_workflow(nd_out_json, intro_uuid),
        SceneBeatAgent().run_workflow(nd_out_json, first_scene_uuid)
    )
    stage_two = await stage_two_gather

    print(f"SAVED BG IMAGE: {stage_two[0]}")
    print(f"SAVED BG IMAGE: {stage_two[1]}")

    # NOTE TEMPORARY -- THESE INDEXES WILL CHANGE!!!!!
    intro_bs: SceneBeatSheet        = stage_two[2]
    intro_bs_json: str              = intro_bs.model_dump_json(indent=2)
    first_scene_bs: SceneBeatSheet  = stage_two[3]
    first_scene_bs_json: str        = first_scene_bs.model_dump_json(indent=2)

    save_beats_gather = asyncio.gather(
        write_output_json(temp_game_name, intro_bs_json, 'intro_beat_sheet'),
        write_output_json(temp_game_name, first_scene_bs_json, 'first_scene_beat_sheet')
    )
    save_beats = await save_beats_gather
    print(f"SAVED BEATS DATA: {save_beats[0]}")
    print(f"SAVED BEATS DATA: {save_beats[1]}")

    # STAGE 3: Write dialog (TODO...)



if __name__ == "__main__":

    concept: str = input("--> ")
    if concept.lower() != "exit":
        asyncio.run(run_program(concept))


