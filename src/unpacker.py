from dotenv import load_dotenv
from pydantic import BaseModel
import sys
from pathlib import Path
import asyncio

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from orchestrator import DemoCreativeData
from scene_beat_agent import SceneBeatSheet
from narrative_design_agent import NarrativeDesignOutputSchema

async def main():
    try:
        with open('KARLA_GAMES/TEST_DATA/DATA/creative_data.json') as f:
            json_str = f.read().strip()
        creative_data: DemoCreativeData = DemoCreativeData.model_validate_json(json_str)
        intro_beat_sheet: SceneBeatSheet = creative_data.beat_sheets[0]
        first_scene_beat_sheet: SceneBeatSheet = creative_data.beat_sheets[1]
        nd_spec: NarrativeDesignOutputSchema = creative_data.narrative_design_spec            
    except Exception as e:
        print(e)

    nd_spec_path: str = 'KARLA_GAMES/TEST_DATA/DATA/nd_spec.json'
    intro_bs_path: str = 'KARLA_GAMES/TEST_DATA/DATA/intro_bs.json'
    first_scene_bs_path: str = 'KARLA_GAMES/TEST_DATA/DATA/first_scene_bs.json'

    with open(nd_spec_path, 'w') as f:
        f.write(nd_spec.model_dump_json(indent=2))
    with open(intro_bs_path, 'w') as f:
        f.write(intro_beat_sheet.model_dump_json(indent=2))
    with open(first_scene_bs_path, 'w') as f:
        f.write(first_scene_beat_sheet.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())





