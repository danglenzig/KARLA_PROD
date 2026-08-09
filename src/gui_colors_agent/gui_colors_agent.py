# src/gui_colors_agent/gui_colors_agent.py

from dotenv import load_dotenv
from pathlib import Path
import asyncio
import sys
from agents import (
    Runner,
    RunResult
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from gui_colors_agent.gui_colors_models import GuiColorScheme
from gui_colors_agent.gui_colors_services import(
    get_gui_color_agent,
    get_gui_color_agent_instructions
)
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput


load_dotenv()

class GuiColorAgent():

    async def run_workflow(self, nd_spec: NarrativeDesignOutput) -> GuiColorScheme:

        run_result: RunResult = await Runner.run(
            get_gui_color_agent(),
            get_gui_color_agent_instructions(nd_spec)
        )

        return run_result.final_output

async def main():
    # use for module testing
    pass

if __name__ == "__main__":
    asyncio.run(main())