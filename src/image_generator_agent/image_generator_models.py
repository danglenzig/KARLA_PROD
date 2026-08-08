# src/image_generator_agent/image_generator_models.py
from typing import Literal
from pydantic import (
    BaseModel, ValidationError, Field
)

class ArtAssetManifest(BaseModel):
    character_portrait_paths: list[str]
    scene_background_paths: list[str]

class ArtStyle(BaseModel):
    art_style: Literal[
        "COMIC",
        "ANIME",
        "PAINTERLY",
        "NOIR",
        "PULP",
        "WATERCOLOR",
        "CLEAN",
        "HORROR_VHS",
        "SCI_FI",
        "SATURDAY_MORNING",
        "PIXEL_ART",
        "CYBERPUNK",
        "GOTHIC_DARK_FANTASY",
        "SYNTHWAVE",
        "CHARCOAL_SKETCH",
        "CHIBI",
        "UKIYO_E",
        "PAPER_CUTOUT",
        "CINEMATIC_CG",
        "STAINED_GLASS",
        
    ] = Field(..., description="The chosen art style")
    reasoning: str = Field(..., description = "A brief summary of your reasoning about why this style was chosen")