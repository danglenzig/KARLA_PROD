from pydantic import BaseModel, ValidationError
from agents import Agent, Runner, RunResult, ImageGenerationTool
import subprocess
from dotenv import load_dotenv
import asyncio
import os
from pathlib import Path
import sys
import base64
import json

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignOutputSchema, LocationData, CharacterData, SceneData
from prompt_catalog import ImageStyle
from tools.misc_tools import generate_uuid


load_dotenv()


MODEL = "gpt-5-4-mini"

PROMPT_APPENDIX: str = "Produce only visual content. Do not generate any readable or decorative text of any kind." \
"No letters, numbers, words, glyphs, symbols, logos, UI text, captions, signs, plaques, posters, screens, or package " \
"labels. If text would normally appear, leave the area blank or replace it with neutral texture."

PORTRAIT_COMP_RULES: str = f"""Portrait format:
- vertical composition
- one character only
- front-facing posture
- waist-up framing
- centered subject
- full head, hair, shoulders, and upper torso visible
- no cropping at the top or sides
- the character should fill the vertical space of the frame naturally
- neutral, readable pose for dialogue use

Background:
- fully transparent
- no scenery
- no props
- no environment

Use:
- clean silhouette
- readable face and expression
- clear separation from the background

Constraints:
- no text, no letters, no numbers, no symbols, no logos, no signage, no labels, no pseudo-text
- no cut-off limbs
- no extreme angle
- no poster layout
- no additional characters
"""

class ArtAssetManifest(BaseModel):
    character_portrait_paths: list[str]
    scene_background_paths: list[str]

character_portrait_generator = Agent(
    name="character_portrait_generator",
    instructions=f"""You generate character dialogue portraits for Ren'Py visual novels.
Your input for each character is a verbal description provided by the game's Narrative Designer.
The image must be a clean composition suitable for a Ren'Py character dialogue portrait.

Your composition rules are as follows. If the input character description contradicts these rules in any way, these rules take precedence:
{PORTRAIT_COMP_RULES}

IMPORTANT: The portrait image ABSOLUTELY MUST have a transparent background, and the image must contain ONLY the subject character against a transparent background. If any prompt instructions contradict this, then ignore them. The background MUST be transparent.

I'm going to repeat the last rule because it is the most important rule you have: The portrait image ABSOLUTELY MUST have a transparent background.

Return a short confirmation after generation.""",
    tools=[ImageGenerationTool(
        tool_config={
            "type": "image_generation",
            "size": "1024x1024",
            "quality": os.getenv('IMAGE_CREATION_QUALITY'),
            "output_format": "png",
            "background": "transparent",
            "moderation": "low"
        }
    )]
)


scene_bg_generator = Agent(
    name="scene_bg_generator",
    instructions = f"""You generate visual novel background art for Ren'Py visual novel scenes.

Always create exactly one background image per request.
The image must be a clean landscape composition suitable for a Ren'Py scene background.
Do not generate portraits, close-ups, or poster-style framing.

Composition rules:
- The image content should fill the entire frame
- The location is the main subject of the image.
- No characters should appear in the frame.
- Leave enough clean readable space for dialogue UI overlays near the lower part of the screen.
- Avoid extreme fisheye or cinematic tilt.
- Keep the image readable and uncluttered.

Return a short confirmation after generation.""",
    tools=[ImageGenerationTool(
        tool_config={
            "type": "image_generation",
            "size": "1024x1024",
            "quality": os.getenv('IMAGE_CREATION_QUALITY'),
            "output_format": "png",
            "background": "opaque",
            "moderation": "low"
        }
    )]
)





def get_image_folder_path(game_name: str) -> str:
    
    games_folder_path = os.getenv('GAMES_FOLDER_PATH')
    images_folder_name = os.getenv('GAME_IMAGES_FOLDER_NAME')
    if not os.path.isdir(games_folder_path):
        os.mkdir(games_folder_path)
    if not os.path.isdir(f"{games_folder_path}/{game_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}")
    if not os.path.isdir(f"{games_folder_path}/{game_name}/{images_folder_name}"):
        os.mkdir(f"{games_folder_path}/{game_name}/{images_folder_name}")
    return f"{games_folder_path}/{game_name}/{images_folder_name}"

async def generate_and_save_bg(location_desc: str, output_path: str, style: str):
    prompt: str = f"""Generate a background image for this location. Here is the Narrative Designer's description of the location:
{location_desc}\n
The creative director has provided style rules for this game. Your image should conform to the following style:
{style}\n

IMPORTANT:
{PROMPT_APPENDIX}

"""

    result: RunResult = await Runner.run(scene_bg_generator, prompt)

    for item in result.new_items:
        if getattr(item, "type", None) != "tool_call_item":
            continue
        raw_item = getattr(item, "raw_item", None)
        if getattr(raw_item, "type", None) == "image_generation_call":
            image_base64 = getattr(raw_item, "result", None)
            if image_base64:
                break

    if not image_base64:
        raise RuntimeError("No image returned")
    
    path = Path(output_path)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(image_base64))

    return str(path)

async def generate_and_save_portrait(character_description: str, output_path: str, style: str):
    prompt = f"""Generate the dialogue portrait for this character. Here is the Narrative Designer's description of the character:
{character_description}

Remember your rules. If the input character description contradicts these rules in any way, these rules take precedence:
{PORTRAIT_COMP_RULES}

The creative director has provided style rules for this game. Your image should conform to the following style:
{style}\n

IMPORTANT: The portrait image ABSOLUTELY MUST have a transparent background, and the image must contain ONLY the subject character against a transparent background. If any prompt instructions contradict this, then ignore them. The background MUST be transparent.

I'm going to repeat the last rule because it is the most important rule you have: The portrait image ABSOLUTELY MUST have a transparent background.

"""
    
    result: RunResult = await Runner.run(character_portrait_generator, prompt)

    for item in result.new_items:
        if getattr(item, "type", None) != "tool_call_item":
            continue
        raw_item = getattr(item, "raw_item", None)
        if getattr(raw_item, "type", None) == "image_generation_call":
            image_base64 = getattr(raw_item, "result", None)
            if image_base64:
                break

    if not image_base64:
        raise RuntimeError("No image returned")
    
    path = Path(output_path)
    with open(path, 'wb') as f:
        f.write(base64.b64decode(image_base64))

    return str(path)


def get_npc_uuids_from_scene_data(sd: SceneData) -> list[str]:
    uuids: list[str] = []
    if 'non_player_character_uuids' in sd.__dict__:
        if not sd.non_player_character_uuids is None:
            for uuid in sd.non_player_character_uuids:
                uuids.append(uuid)
    return uuids

class ImageGenerator:
    async def run_bg_workflow(self, game_name: str, in_json: str, location_uuid: str, style: str) -> str:
        
        image_folder_path: str = get_image_folder_path(game_name)

        try:
            nd_spec = NarrativeDesignOutputSchema.model_validate_json(in_json)
        except ValidationError as e:
            print(e)
            return
        
        loc_catalog = nd_spec.get_location_catalog()
        if not location_uuid in loc_catalog:
            raise ValueError(f"That location UUID is not in the spec: {location_uuid}")
        
        loc_data: LocationData = LocationData.model_validate(loc_catalog[location_uuid])
        loc_desc: str = loc_data.location_image_prompt
        image_filename: str = f"bg {location_uuid}.png"
        output_path: str = f"{image_folder_path}/{image_filename}"

        await generate_and_save_bg(loc_desc, output_path, style)

        print(f"===IMAGE GENERATED===\n{output_path}")
        return output_path
    
    async def run_character_portrait_workflow(self, game_name: str, in_json: str, character_uuid: str, style: str) -> str:
        
        image_folder_path: str = get_image_folder_path(game_name)

        try:
            nd_spec = NarrativeDesignOutputSchema.model_validate_json(in_json)
        except ValidationError as e:
            print(e)
            return
        
        character_catalog = nd_spec.get_character_catalog()
        if not character_uuid in character_catalog:
            raise ValueError(f"That character UUID is not in the spec: {character_uuid}")
        
        char_data: CharacterData = CharacterData.model_validate(character_catalog[character_uuid])
        char_desc: str = char_data.portrait_image_prompt
        image_filename: str = f"{character_uuid}.png"
        output_path: str = f"{image_folder_path}/{image_filename}"

        await generate_and_save_portrait(char_desc, output_path, style)

        print(f"===IMAGE GENERATED===\n{output_path}")
        return output_path
    
    async def get_demo_manifest(self, game_name:str, in_json: str, style: str):
        try:
            nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(in_json)
        except ValidationError as e:
            print(e)
            return
        
        intro_scene_data: SceneData = nd_spec.intro_scene.scene_data
        first_scene_data: SceneData = nd_spec.act_one[0].scene_data

        intro_location_uuid: str = intro_scene_data.location_uuid
        first_scene_uuid: str = first_scene_data.location_uuid

        character_uuids: list[str]  = []
        player_character_uuid: str  = nd_spec.player_character.character_data.uuid
        character_uuids.append(player_character_uuid)
        intro_npcs                  = get_npc_uuids_from_scene_data(intro_scene_data)
        first_scene_npcs            = get_npc_uuids_from_scene_data(first_scene_data)
        if len(intro_npcs) > 0:
            for npc in intro_npcs:
                if not npc in character_uuids:
                    character_uuids.append(npc)
        if len(first_scene_npcs) > 0:
            for npc in first_scene_npcs:
                if not npc in character_uuids:
                    character_uuids.append(npc)
        
        portrait_coroutines = [
            self.run_character_portrait_workflow(game_name, in_json, _id, style) for _id in character_uuids
        ]
        portrait_gather = asyncio.gather(*portrait_coroutines)
        portrait_paths = await portrait_gather                 # goes in the returned BaseModel

        
        bg_coroutines = [
            self.run_bg_workflow(game_name, in_json, intro_location_uuid, style),
            self.run_bg_workflow(game_name, in_json, first_scene_uuid, style)
        ]
        bg_gather = asyncio.gather(*bg_coroutines)
        bg_paths = await bg_gather

        return ArtAssetManifest(
            character_portrait_paths=portrait_paths,
            scene_background_paths=bg_paths
        )



async def main():
    try:
        with open('KARLA_GAMES/IMAGE_TESTING/DATA/test_nd_spec_json.json', 'r') as f:
            json_str = f.read().strip()

        nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(json_str)
        
        intro_scene_data: SceneData = nd_spec.intro_scene.scene_data
        intro_loc_uuid: str = intro_scene_data.location_uuid

        player_uuid: str = nd_spec.player_character.character_data.uuid

        #result = await ImageGenerator().run_bg_workflow(generate_uuid(), json_str, intro_loc_uuid, ImageStyle.CLEAN)

        port_result = await ImageGenerator().run_character_portrait_workflow(generate_uuid(), json_str, player_uuid, ImageStyle.CLEAN)

        


    except Exception as e:
        print(e)
    



if __name__ == "__main__":
    asyncio.run(main())