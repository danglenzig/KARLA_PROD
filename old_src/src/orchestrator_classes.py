from pydantic import BaseModel
from pathlib import Path
import sys

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from narrative_design_agent import NarrativeDesignOutputSchema
from image_generator import ArtAssetManifest
from scene_beat_agent import SceneBeatSheet

