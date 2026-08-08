# src/beat_sheet_agent/beat_sheet_agent.py

import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import sys
import asyncio
from agents import(
    Agent,
    Runner,
    RunResult
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from beat_sheet_agent.beat_sheet_models import (
    SceneBeatSheet
)
from beat_sheet_agent.beat_sheet_services import(
    get_sb_agent,
    get_sb_agent_input,
    get_sb_agent_instructions
)
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput

load_dotenv()

class SceneBeatAgent():

    async def run_workflow(
            self,
            nd_spec: NarrativeDesignOutput,
            scene_uuid: str
    )->SceneBeatSheet:
        
        sb_agent_input = get_sb_agent_input(nd_spec, scene_uuid)

        agent: Agent[NarrativeDesignOutput] = get_sb_agent()

        run_result: RunResult = await Runner.run(
            agent,
            input=sb_agent_input,
            context=nd_spec
        )

        return run_result.final_output

async def main():
    try:
        with open('/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_REFACTOR/json/test_nd_spec.json', 'r') as f:
            json_str = f.read().strip()
            nd_spec: NarrativeDesignOutput = NarrativeDesignOutput.model_validate_json(json_str)

            intro_uuid: str = nd_spec.intro_scene.scene_data.uuid
            first_scene_uuid = nd_spec.act_one[0].scene_data.uuid

            test_coros = [
                SceneBeatAgent().run_workflow(nd_spec, intro_uuid),
                SceneBeatAgent().run_workflow(nd_spec, first_scene_uuid)
            ]
            test_gather = asyncio.gather(*test_coros)
            test = await test_gather
            sheets: list[SceneBeatSheet] = [
                test[0], test[1]
            ]

            print(sheets[0].model_dump_json(indent=2))
            print("\n\n")
            print(sheets[1].model_dump_json(indent=2))

            
            #print(beat_sheet.model_dump_json(indent=2))

    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())
