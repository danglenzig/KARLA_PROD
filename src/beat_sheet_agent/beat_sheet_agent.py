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
    # use for module testing
    pass

if __name__ == "__main__":
    asyncio.run(main())
