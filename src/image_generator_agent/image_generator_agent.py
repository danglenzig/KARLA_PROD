# src/image_generator_agent/image_generator_agent.py

from dotenv import load_dotenv
import sys
from pathlib import Path
import asyncio
from pydantic import(
    BaseModel
)
from agents import(
    Agent,
    Runner,
    RunResult
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    CharacterData,
    LocationData,
    SceneData
)
from image_generator_agent.image_generator_models import(
    ArtAssetManifest,
    ArtStyle
)
from discovery_agent.discovery_agent_models import StoryConcept
from image_generator_agent.image_generator_services import(
    get_portrait_image_generator_agent,
    get_scene_image_generator_agent,
    get_style_prompt,
    get_art_style_chooser_agent,
    generate_and_save_bg,
    generate_and_save_portrait,
    get_image_folder_path
)
from image_generator_agent.image_styles import ImageStyle


def get_npc_uuids_from_scene_data(sd: SceneData) -> list[str]:
    uuids: list[str] = []
    if 'non_player_character_uuids' in sd.__dict__:
        if not sd.non_player_character_uuids is None:
            for uuid in sd.non_player_character_uuids:
                uuids.append(uuid)
    return uuids

class ImageGenerator:

    async def _run_scene_bg_workflow(
            self,
            game_name: str,
            nd_spec: NarrativeDesignOutput,
            location_uuid: str,
            style: str
    )->str:
        
        image_folder_path:str = get_image_folder_path(game_name)

        loc_catalog = nd_spec.get_location_catalog()
        if not location_uuid in loc_catalog:
            raise ValueError(f"Location UUID not found: {location_uuid}")

        loc_data: LocationData = LocationData.model_validate(loc_catalog[location_uuid])
        loc_desc: str = loc_data.location_image_prompt
        image_filename: str = f"bg {location_uuid}.png"
        output_path: str = f"{image_folder_path}/{image_filename}"

        await generate_and_save_bg(loc_desc, output_path, style)

        print(f"===IMAGE GENERATED===\n{output_path}")
        return output_path

    async def _run_character_portrait_workflow(
            self,
            game_name: str,
            nd_spec: NarrativeDesignOutput,
            character_uuid: str,
            style: str
    )->str:
        
        image_folder_path = get_image_folder_path(game_name)

        character_catalog = nd_spec.get_character_catalog()
        if not character_uuid in character_catalog:
            raise ValueError(f"Character UUID not found: {character_uuid}")

        char_data: CharacterData = CharacterData.model_validate(character_catalog[character_uuid])
        char_desc: str = char_data.portrait_image_prompt
        image_filename = f"{character_uuid}.png"
        output_path: str = f"{image_folder_path}/{image_filename}"

        await generate_and_save_portrait(char_desc, output_path, style)

        print(f"===IMAGE GENERATED===\n{output_path}")
        return output_path

    async def get_demo_manifest(
            self,
            game_name: str,
            nd_spec: NarrativeDesignOutput,
            #style: str
    )->ArtAssetManifest:
        #=====================================================================
        # get the prompt style here and feed it into the two image generators
        #=====================================================================
        synopsis: str = nd_spec.synopsis
        chooser_agent: Agent = get_art_style_chooser_agent()
        style_run_result: RunResult = await Runner.run(
            chooser_agent,
            f"""Choose a thematically appropriate art style for this visual novel story concept:
            {synopsis}"""
        )
        chosen_style: ArtStyle = style_run_result.final_output_as(ArtStyle)
        style_prompt: str = get_style_prompt(chosen_style)

        print(f"\n### ART STYLE PROMT:{style_prompt}")
        print(f"\n### ART STYLE REASONING:{chosen_style.reasoning} ")
        

        intro_scene_data: SceneData = nd_spec.intro_scene.scene_data
        first_scene_data: SceneData = nd_spec.act_one[0].scene_data

        intro_location_uuid: str = intro_scene_data.location_uuid
        first_scene_uuid: str = first_scene_data.location_uuid

        character_uuids: list[str] = []

        player_character_uuid: str = nd_spec.player_character.character_data.uuid
        character_uuids.append(player_character_uuid)

        intro_npcs       = get_npc_uuids_from_scene_data(intro_scene_data)
        first_scene_npcs = get_npc_uuids_from_scene_data(first_scene_data)

        if len(intro_npcs) > 0:
            for npc in intro_npcs:
                if not npc in character_uuids:
                    character_uuids.append(npc)
        if len(first_scene_npcs) > 0:
            for npc in first_scene_npcs:
                if not npc in character_uuids:
                    character_uuids.append(npc)

        portrait_coroutines = [
            self._run_character_portrait_workflow(game_name, nd_spec, _id, style_prompt) for _id in character_uuids
        ]
        portrait_gather = asyncio.gather(*portrait_coroutines)
        portrait_paths = await portrait_gather

        bg_coroutines = [
            self._run_scene_bg_workflow(game_name, nd_spec, intro_location_uuid, style_prompt),
            self._run_scene_bg_workflow(game_name, nd_spec, first_scene_uuid, style_prompt)
        ]
        bg_gather = asyncio.gather(*bg_coroutines)
        bg_paths = await bg_gather

        return ArtAssetManifest(
            character_portrait_paths=portrait_paths,
            scene_background_paths=bg_paths
        )


async def main():
    try:
        with open('/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_REFACTOR/json/test_nd_spec.json', 'r') as f:

            json_str = f.read().strip()
            nd_spec: NarrativeDesignOutput = NarrativeDesignOutput.model_validate_json(json_str)
            synopsis: str = nd_spec.synopsis
            print(f"\n{synopsis}\n\n")

            chooser_agent: Agent = get_art_style_chooser_agent()
            run_result: RunResult = await Runner.run(
                chooser_agent,
                f"""Choose a thematically appropriate art style for this visual novel story concept:
                {synopsis}"""
            )
            art_style: ArtStyle = run_result.final_output_as(ArtStyle)
            print(art_style.model_dump_json(indent=2))
            style_prompt: str = get_style_prompt(art_style)
            print(f"\n{style_prompt}")

            manifest: ArtAssetManifest = await ImageGenerator().get_demo_manifest("test_game", nd_spec, style_prompt)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())