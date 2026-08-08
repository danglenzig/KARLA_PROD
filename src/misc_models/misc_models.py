from pydantic import BaseModel
from pathlib import Path
import sys

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from image_generator_agent.image_generator_models import ArtAssetManifest
from discovery_agent.discovery_agent_models import StoryConcept
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput
from beat_sheet_agent.beat_sheet_models import SceneBeatSheet
from gui_colors_agent.gui_colors_models import GuiColorScheme
from dialogue_agent.dialogue_agent_models import DialogueScene

class DemoCreativeData(BaseModel):
    """
    The combined output of the creative agents.
    """
    concept: StoryConcept
    narrative_design_spec: NarrativeDesignOutput
    art_assets: ArtAssetManifest
    beat_sheets: list[SceneBeatSheet]
    color_scheme: GuiColorScheme

class DemoBuildData(BaseModel):
    art_assets: ArtAssetManifest
    dialogue_scenes: list[DialogueScene]
    gui_colors: GuiColorScheme
    character_dict: dict[str, str]

