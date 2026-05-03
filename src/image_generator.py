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

from narrative_design_agent import NarrativeDesignOutputSchema, LocationData, CharacterData
from prompt_catalog import ImageStyle

load_dotenv()


MODEL = "gpt-5-4-mini"

PROMPT_APPENDIX: str = "Produce only visual content. Do not generate any readable or decorative text of any kind." \
"No letters, numbers, words, glyphs, symbols, logos, UI text, captions, signs, plaques, posters, screens, or package " \
"labels. If text would normally appear, leave the area blank or replace it with neutral texture."


scene_bg_generator = Agent(
    name="scene_bg_generator",
    instructions = f"""You generate visual novel background art for Ren'Py visual novel scenes.

Always create exactly one background image per request.
The image must be a clean 16:9 landscape composition suitable for a Ren'Py scene background.
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
            "quality": "high",
            "output_format": "png",
            "background": "opaque",
            "moderation": "low"
        }
    )]
)




test_game_name = 'TEST_GAME_04'

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
            raise ValueError("That location UUID is not in the spec")
        
        loc_data: LocationData = LocationData.model_validate(loc_catalog[location_uuid])
        loc_desc: str = loc_data.location_image_prompt
        image_filename = f"bg {location_uuid}.png"
        output_path = f"{image_folder_path}/{image_filename}"

        await generate_and_save_bg(loc_desc, output_path, style)

        print(f"===IMAGE GENERATED===\n{output_path}")
        return output_path

async def main():
    try:
        with open('dummy_data.json', 'r') as f:
            json_str = f.read().strip()

        nd_output: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(json_str)
        intro_uuid = nd_output.intro_scene.scene_data.uuid
        first_scene_uuid = nd_output.act_one[0].scene_data.uuid

        intro_loc_uuid: str = nd_output.intro_scene.scene_data.location_uuid
        first_scene_uuid: str = nd_output.act_one[0].scene_data.location_uuid

        image_gather = asyncio.gather(
            ImageGenerator().run_bg_workflow(test_game_name, json_str, intro_loc_uuid, ImageStyle.CLEAN),
            ImageGenerator().run_bg_workflow(test_game_name, json_str, first_scene_uuid, ImageStyle.CLEAN)
        )

        

        await image_gather

        print(f"\n\nDone\n\n")


    except Exception as e:
        print(e)
    



if __name__ == "__main__":
    asyncio.run(main())