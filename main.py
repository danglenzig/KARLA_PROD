import asyncio
from src.narrative_design_agent import NarrativeDesignAgent, NarrativeDesignOutputSchema, WorkflowTextInput
from src.scene_beat_agent import SceneBeatAgent
from pydantic import BaseModel, Field
import json

async def program_entry():

    nd_agent: NarrativeDesignAgent = NarrativeDesignAgent()

    user_input: str = input("--> ")
    wf_input: WorkflowTextInput = WorkflowTextInput(
        input_as_text=user_input
    )

    # TODO: pipeline entry guardrail

    #=========================
    # INITIAL NARRATIVE DESIGN
    #=========================
    nd_agent_output: NarrativeDesignOutputSchema = await nd_agent.run_workflow(wf_input)
    human_readable = nd_agent_output.human_readable()

    print(f"\n\n{human_readable}\n\n")

    #========================
    # WRITING THE SCENE BEATS
    #========================
    nd_json = nd_agent_output.model_dump_json()
    sb_agent: SceneBeatAgent = SceneBeatAgent()
    await sb_agent.run_workflow(nd_json)


async def main():
    await program_entry()

if __name__ == "__main__":
    asyncio.run(main())

