# src/narrative_design_agent/narrative_design_agent.py

from dotenv import load_dotenv
load_dotenv()

from pathlib import Path
import sys
import asyncio
import json
from agents import (
    Agent, Runner, RunResult, RunResultStreaming
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from narrative_design_agent.narrative_design_agent_models import (
    CharacterData,
    # ...
)
from discovery_agent.discovery_agent_models import StoryConcept
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput
from narrative_design_agent.narrative_design_agent_services import (
    get_narrative_design_agent,
    get_nd_workflow_input,
)




GPT_MODEL = "gpt-5.4"

class NarrativeDesignAgent():
    """
    Agent for generating detailed narrative design specifications from a high-level story concept.

    The NarrativeDesignAgent takes a concise story idea and produces a structured narrative design output,
    including player character, non-player characters, locations, and a full act/scene breakdown suitable for 
    downstream agents (such as beat planners, asset generators, and dialogue writers).

    Key behaviors:
      - Receives a story concept as text input.
      - Runs an LLM-based workflow to expand and structure the narrative, following defined output schemas.
      - Produces a NarrativeDesignOutputSchema containing title, synopsis, characters, act/scene lists, and locations.
      - Ensures all required elements for visual novel generation are present, with explicit schema fields and stable UUIDs.
      - Provides helper methods for testing or retrieving human-readable summaries and catalogs.

    Usage Example:
        agent = NarrativeDesignAgent()
        spec = await agent.run_workflow(WorkflowTextInput(input_as_text="Haunted hotel story..."))

    This class is a central pipeline component, ensuring every generated game has a well-formed narrative blueprint.
    """
    def __init__(self):
        self.agent: Agent = get_narrative_design_agent(GPT_MODEL)
    
    # TODO: replace with streaming output workflow
    async def run_workflow(self, _story_concept: StoryConcept)->NarrativeDesignOutput:
        run_result: RunResult = await Runner.run(
            starting_agent = self.agent,
            input = get_nd_workflow_input(_story_concept),
        )
        return run_result.final_output_as(NarrativeDesignOutput)
    
    async def run_workflow_streaming(self, _story_concept: StoryConcept)->NarrativeDesignOutput:
        run_result: RunResultStreaming = Runner.run_streamed(
            starting_agent=self.agent,
            input=get_nd_workflow_input(_story_concept)
        )
        output_already_started: bool = False

        async for event in run_result.stream_events():

            if event.type == "raw_response_event":
                if event.data.type == "response.reasoning_summary_text.delta":
                    print(f"\033[33m{event.data.delta}\033[0m", end= "", flush= True)
                elif event.data.type == "response.output_text.delta":
                    if not output_already_started:
                        print("\n")
                        output_already_started = True
                    print(f"\033[33m{event.data.delta}\033[0m", end= "", flush= True)

        print(f"\n\n======RUN COMPLETE======\n\n")
        return run_result.final_output_as(NarrativeDesignOutput)


async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())