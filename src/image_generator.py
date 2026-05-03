from pydantic import BaseModel, ValidationError
from agents import Agent, Runner, RunResult, ImageGenerationTool
import subprocess
from dotenv import load_dotenv
import asyncio
import os
from pathlib import Path
import sys
import base64

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignOutputSchema, LocationData, CharacterData, SceneData
from prompt_catalog import ImageStyle

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

character_portrait_generator = Agent(
    name="character_portrait_generator",
    instructions=f"""You generate character dialogue portraits for Ren'Py visual novels.
Your input for each character is a verbal description provided by the game's Narrative Designer.
The image must be a clean composition suitable for a Ren'Py character dialogue portrait.

Your composition rules are as follows. If the input character description contradicts these rules in any way, these rules take precedence:
{PORTRAIT_COMP_RULES}

Return a short confirmation after generation.""",
    tools=[ImageGenerationTool(
        tool_config={
            "type": "image_generation",
            "size": "1024x1536",
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
- Wide environmental shot, size: 1280x720
- The location is the main subject of the image.
- No characters should appear in the frame.
- Leave enough clean readable space for dialogue UI overlays near the lower part of the screen.
- Avoid extreme fisheye or cinematic tilt.
- Keep the image readable and uncluttered.

Return a short confirmation after generation.""",
    tools=[ImageGenerationTool(
        tool_config={
            "type": "image_generation",
            "size": "1536x1024",
            "quality": os.getenv('IMAGE_CREATION_QUALITY'),
            "output_format": "png",
            "background": "opaque",
            "moderation": "low"
        }
    )]
)




test_game_name = '_ABC123'



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
{style}\n"""
    
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


def get_npc_uuids_from_scene_data(sd: SceneData) -> list[str]:
    uuids: list[str] = []
    if 'non_player_character_uuids' in sd.__dict__:
        if not sd.non_player_character_uuids is None:
            for uuid in sd.non_player_character_uuids:
                uuids.append(uuid)
    return uuids

async def main():
    try:
        with open('dummy_data.json', 'r') as f:
            json_str = f.read().strip()

        nd_output: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(json_str)
        intro_uuid = nd_output.intro_scene.scene_data.uuid
        first_scene_uuid = nd_output.act_one[0].scene_data.uuid

        # TESTING PORTRAIT GENERATION
        # get all the character UUIDs from the first two scenes
        character_uuids: list[str] = []

        player_uuid: str = nd_output.player_character.character_data.uuid
        character_uuids.append(player_uuid)

        intro_scene_data: SceneData = nd_output.intro_scene.scene_data
        intro_scene_uuids = get_npc_uuids_from_scene_data(intro_scene_data)
        if len(intro_scene_uuids) > 0:
            for id in intro_scene_uuids:
                if not id in character_uuids:
                    character_uuids.append(id)
        
        first_scene_data: SceneData = nd_output.act_one[0].scene_data
        first_scene_uuids = get_npc_uuids_from_scene_data(first_scene_data)
        if len(first_scene_uuids) > 0:
            for id in first_scene_uuids:
                if not id in character_uuids:
                    character_uuids.append(id)


        character_count = len(character_uuids)

        portrait_coroutines = [
            ImageGenerator().run_character_portrait_workflow(
                test_game_name,
                json_str,
                _id,
                ImageStyle.COMIC
            ) for _id in character_uuids
        ]

        portrait_gather = asyncio.gather(*portrait_coroutines) # unpacks the coros

        await portrait_gather





        

        #await image_gather

        print(f"\n\nDone\n\n")


    except Exception as e:
        print(e)
    



if __name__ == "__main__":
    asyncio.run(main())