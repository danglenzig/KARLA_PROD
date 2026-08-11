# src/orchestrator.py

from dotenv import load_dotenv
from pydantic import BaseModel # this is what provides the validation magic
import asyncio
from pathlib import Path
import sys
from datetime import datetime
from camel_converter import to_camel, to_snake
import os
import json
from camel_converter import to_snake

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from misc_models.misc_models import DemoCreativeData
from misc_models.misc_models import DemoBuildData
from discovery_agent.discovery_agent_models import StoryConcept
from discovery_agent.discovery_agent import DiscoveryAgent
from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    NarrativeDesignContentValidationResult,
)
from narrative_design_agent.narrative_design_agent import NarrativeDesignAgent
from narrative_design_agent.narrative_design_content_validator import get_nd_spec_validation_results
from image_generator_agent.image_styles import ImageStyle
from image_generator_agent.image_generator_agent import ImageGenerator
from image_generator_agent.image_generator_models import ArtAssetManifest
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

async def main():

    game_title: str = ""

    #===============================
    #  Stage 1: Get the StoryConcept
    #===============================
    print("+=============================")
    print("| Stage 1: Interview the user.")
    print("+=============================\n\n")

    story_concept: StoryConcept = await DiscoveryAgent().run_workflow()

    #=======================================
    # Stage 2: Get the NarrativeDesignOutput
    #=======================================

    print("+=========================================")
    print("| Stage 2: Generate narrative design spec.")
    print("+=========================================\n\n")

    nd_output: NarrativeDesignOutput = await NarrativeDesignAgent().run_workflow_streaming(story_concept)

    # Content validation
    nd_validation: NarrativeDesignContentValidationResult = get_nd_spec_validation_results(nd_output)
    if nd_validation.has_problems:
        raise ValueError(f"### NarrativeDesignAgent output content validation failed:\n\n{nd_validation.comments}")
    else:
        print("### NarrativeDesignAgent output content validated")

    game_title = to_snake(nd_output.story_title).replace(" ","")

    stage_two_json_dumps = [
        write_json_data(game_title, story_concept.model_dump_json(indent=2), "story_concept.json"),
        write_json_data(game_title, nd_output.model_dump_json(indent=2), "narrative_design_output.json")
    ]
    stage_two_gather_json_dumps = asyncio.gather(*stage_two_json_dumps)
    await stage_two_gather_json_dumps

    print(f"\n\n{nd_output.model_dump_json(indent=2)}")

    #=================================================
    # Stage 3: Async gather art assets and scene beats
    #=================================================

    print("+================================================")
    print("| Stage 3: Generate & gather art and beat sheets.")
    print("+================================================\n\n")
    
    stage_three_coroutines = [
        ImageGenerator().get_demo_manifest(game_title, nd_output),
        SceneBeatAgent().run_workflow(nd_output, nd_output.intro_scene.scene_data.uuid), # intro beats
        SceneBeatAgent().run_workflow(nd_output, nd_output.act_one[0].scene_data.uuid), # first scene beats
        GuiColorAgent().run_workflow(nd_output)
    ]

    #============================================
    # TODO: Content validation on the beat sheets
    # - check UUIDs on scenes and beats
    #============================================

    stage_three_gather = asyncio.gather(*stage_three_coroutines)
    stage_three_products = await stage_three_gather
    art_manifest: ArtAssetManifest = stage_three_products[0]
    intro_beats: SceneBeatSheet = stage_three_products[1]
    first_scene_beats: SceneBeatSheet = stage_three_products[2]
    color_scheme: GuiColorScheme = stage_three_products[3]
    beat_sheet_list: list[SceneBeatSheet] = [intro_beats, first_scene_beats]

    creative_data: DemoCreativeData = DemoCreativeData(
        concept               = story_concept,
        narrative_design_spec = nd_output,
        art_assets            = art_manifest,
        beat_sheets           = beat_sheet_list,
        color_scheme          = color_scheme
    )

    await write_json_data(game_title, creative_data.model_dump_json(indent=2), "creative_data.json")

    creative_data_json = creative_data.model_dump_json(indent=2)

    #============================
    # Stage 4: The dialogue stage
    #============================

    print("+==================================")
    print("| Stage 4: Generate dialogue assets")
    print("+===================================\n\n")

    stage_four_coroutines = [
        DialogueAgent().run_scene_workflow(nd_output, intro_beats),
        DialogueAgent().run_scene_workflow(nd_output, first_scene_beats)
    ]
    stage_four_gather = asyncio.gather(*stage_four_coroutines)
    stage_four = await stage_four_gather

    dialogue_scene_list: list[DialogueScene] = [
        stage_four[0],
        stage_four[1]
    ]

    #=========================================
    # TODO: Content validation on the dialogue
    #=========================================

    #=========================
    # Stage 5: The build stage
    #=========================
    
    print("+===============================")
    print("| Stage 5: Build Ren'Py scripts.")
    print("+===============================\n\n")

    char_dict: dict[str,str] = {}
    character_catalogue = nd_output.get_character_catalog()
    for id in character_catalogue:
        char_dict[id] = character_catalogue[id]['name']
        
    build_data: DemoBuildData = DemoBuildData(
        art_assets=creative_data.art_assets,
        dialogue_scenes=dialogue_scene_list,
        gui_colors=color_scheme,
        character_dict=char_dict
    )
    await write_json_data(game_title, build_data.model_dump_json(indent=2), 'build_data.json')

    script_rpy = await RenPyScriptAssembler().run_workflow(build_data)
    script_path: str = await write_rpy_script(game_title, script_rpy, 'script.rpy')

    print("+==================")
    print("| Stage 6: Publish.")
    print("+==================\n\n")

    publish_success: bool = await RenPyPublisher().run_workflow(
        game_title=game_title,
        script_file_path=script_path,
        art_manifest=art_manifest
    )
    if not publish_success:
        print("Something bad happened")
        # TODO: raise an appropriate error (what?)
    

    

if __name__ == "__main__":
    asyncio.run(main())

