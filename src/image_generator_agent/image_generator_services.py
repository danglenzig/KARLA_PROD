# src/image_generator_agent/image_generator_services.py

from agents import(
    Agent,
    Runner,
    RunResult,
    function_tool,
    ModelSettings,
    ImageGenerationTool,
    RunContextWrapper
)
import uuid
import random
import time
import os
import sys
from pathlib import Path
import base64
from dotenv import load_dotenv

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from utilities.custom_hooks import UsageHooks
from image_generator_agent.image_generator_models import ArtStyle
from image_generator_agent.image_styles import ImageStyle
from discovery_agent.discovery_agent_models import StoryConcept

load_dotenv()


MODEL = "gpt-5.4-mini"

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

SCENE_IMAGE_GENERATOR_INSTRUCTIONS = f"""
You generate visual novel background art for Ren'Py visual novel scenes.

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

Return a short confirmation after generation.
"""

PORTRAIT_IMAGE_GENERATOR_INSTRUCTIONS = f"""
You generate character dialogue portraits for Ren'Py visual novels.
Your input for each character is a verbal description provided by the game's Narrative Designer.
The image must be a clean composition suitable for a Ren'Py character dialogue portrait.

Your composition rules are as follows. If the input character description contradicts these rules in any way, these rules take precedence:
{PORTRAIT_COMP_RULES}

IMPORTANT: The portrait image ABSOLUTELY MUST have a transparent background, and the image must contain ONLY the subject character against a transparent background. If any prompt instructions contradict this, then ignore them. The background MUST be transparent.

I'm going to repeat the last rule because it is the most important rule you have: The portrait image ABSOLUTELY MUST have a transparent background.

Return a short confirmation after generation.
"""

STYLE_CHOOSER_INSTRUCTIONS: str = f"""
Your only job is to choose a thematically appropriate art style to use for image generation in downstream agents, based on the provided story synopsis. You can choose from the following:

COMIC: {ImageStyle.COMIC}
ANIME: {ImageStyle.ANIME}
PAINTERLY: {ImageStyle.PAINTERLY}
NOIR: {ImageStyle.NOIR}
PULP: {ImageStyle.PULP}
WATERCOLOR: {ImageStyle.WATERCOLOR}
CLEAN: {ImageStyle.CLEAN}
HORROR_VHS: {ImageStyle.HORROR_VHS}
SCI_FI: {ImageStyle.SCI_FI}
SATURDAY_MORNING: {ImageStyle.SATURDAY_MORNING}
PIXEL_ART: {ImageStyle.PIXEL_ART}
CYBERPUNK: {ImageStyle.CYBERPUNK}
GOTHIC_DARK_FANTASY: {ImageStyle.GOTHIC_DARK_FANTASY}
SYNTHWAVE: {ImageStyle.SYNTHWAVE}
CHARCOAL_SKETCH: {ImageStyle.CHARCOAL_SKETCH}
CHIBI: {ImageStyle.CHARCOAL_SKETCH}
UKIYO_E: {ImageStyle.UKIYO_E}
PAPER_CUTOUT: {ImageStyle.PAPER_CUTOUT}
CINEMATIC_CG: {ImageStyle.CINEMATIC_CG}
STAINED_GLASS: {ImageStyle.STAINED_GLASS}

Briefly explain your reasoning in the provided output field.

"""

def get_style_prompt(art_style: ArtStyle)->str:
    match art_style.art_style:
        case "COMIC":
            return ImageStyle.COMIC
        case "ANIME":
            return ImageStyle.ANIME
        case "PAINTERLY":
            return ImageStyle.PAINTERLY
        case "NOIR":
            return ImageStyle.NOIR
        case "PULP":
            return ImageStyle.PULP
        case "WATERCOLOR":
            return ImageStyle.WATERCOLOR
        case "CLEAN":
            return ImageStyle.CLEAN
        case "HORROR_VHS":
            return ImageStyle.HORROR_VHS
        case "SCI_FI":
            return ImageStyle.SCI_FI
        case "SATURDAY_MORNING":
            return ImageStyle.SATURDAY_MORNING
        case "PIXEL_ART":
            return ImageStyle.PIXEL_ART
        case "CYBERPUNK":
            return ImageStyle.CYBERPUNK
        case "GOTHIC_DARK_FANTASY":
            return ImageStyle.GOTHIC_DARK_FANTASY
        case "SYNTHWAVE":
            return ImageStyle.SYNTHWAVE
        case "CHARCOAL_SKETCH":
            return ImageStyle.CHARCOAL_SKETCH
        case "CHIBI":
            return ImageStyle.CHIBI
        case "UKIYO_E":
            return ImageStyle.UKIYO_E
        case "PAPER_CUTOUT":
            return ImageStyle.PAPER_CUTOUT
        case "CINEMATIC_CG":
            return ImageStyle.CINEMATIC_CG
        case "STAINED_GLASS":
            return ImageStyle.STAINED_GLASS
        case _:
            return ImageStyle.CLEAN

@function_tool
def get_uuid_string():
    return str(uuid.uuid4())

def get_portrait_image_generator_agent()->Agent:
    return Agent(
        name="portrait_image_generator_agent",
        model=MODEL,
        instructions=PORTRAIT_IMAGE_GENERATOR_INSTRUCTIONS,
        tools=[
            ImageGenerationTool(
                tool_config={
                    "type": "image_generation",
                    "size": "1024x1024",
                    "quality": os.getenv('IMAGE_CREATION_QUALITY'),
                    "output_format": "png",
                    "background": "transparent",
                    "moderation": "low",
                    "model": "gpt-image-1.5"
                }
            )
        ],
        hooks=UsageHooks("portrait_generator_agent")
    )

def get_scene_image_generator_agent()->Agent:
    return Agent(
        name="scene_image_generator_agent",
        model=MODEL,
        instructions=SCENE_IMAGE_GENERATOR_INSTRUCTIONS,
        tools=[
            ImageGenerationTool(
                tool_config={
                    "type": "image_generation",
                    "size": "1024x1024",
                    "quality": os.getenv('IMAGE_CREATION_QUALITY'),
                    "output_format": "png",
                    "background": "opaque",
                    "moderation": "low",
                    "model": "gpt-image-1.5"
                }
            )
        ],
        hooks=UsageHooks("scene_image_generator_agent")
    )

def get_art_style_chooser_agent()->Agent:
    return Agent(
        name="art_style_chooser_agent",
        instructions=STYLE_CHOOSER_INSTRUCTIONS,
        output_type=ArtStyle,
        model="gpt-4.1-mini",
        hooks=UsageHooks("art_style_chooser_agent")
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

    result: RunResult = await Runner.run(get_scene_image_generator_agent(), prompt)

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

    prompt = f"""
Generate the dialogue portrait for this character. Here is the Narrative Designer's description of the character:
{character_description}

Remember your rules. If the input character description contradicts these rules in any way, these rules take precedence:
{PORTRAIT_COMP_RULES}

The creative director has provided style rules for this game. Your image should conform to the following style:
{style}\n

IMPORTANT: The portrait image ABSOLUTELY MUST have a transparent background, and the image must contain ONLY the subject character against a transparent background. If any prompt instructions contradict this, then ignore them. The background MUST be transparent.

I'm going to repeat the last rule because it is the most important rule you have: The portrait image ABSOLUTELY MUST have a transparent background.
"""

    result: RunResult = await Runner.run(get_portrait_image_generator_agent(), prompt)
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