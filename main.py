import asyncio
from src.narrative_design_agent import NarrativeDesignAgent, NarrativeDesignOutputSchema, WorkflowTextInput
from src.scene_beat_agent import SceneBeatAgent
from src.image_generator import ImageGenerator
from src.prompt_catalog import ImageStyle
from pydantic import BaseModel, Field
import json

# async def program_entry():

#     nd_agent: NarrativeDesignAgent = NarrativeDesignAgent()

#     user_input: str = input("--> ")
#     wf_input: WorkflowTextInput = WorkflowTextInput(
#         input_as_text=user_input
#     )

#     # TODO: pipeline entry guardrail

#     #=========================
#     # INITIAL NARRATIVE DESIGN
#     #=========================
#     nd_agent_output: NarrativeDesignOutputSchema = await nd_agent.run_workflow(wf_input)
#     human_readable = nd_agent_output.human_readable()

#     print(f"\n\n{human_readable}\n\n")

#     #========================
#     # WRITING THE SCENE BEATS
#     #========================

#     intro_uuid: str     = nd_agent_output.intro_scene.scene_data.uuid
#     first_scene_uuid    = nd_agent_output.act_one[0].scene_data.uuid


#     nd_json = nd_agent_output.model_dump_json()
#     sb_agent: SceneBeatAgent = SceneBeatAgent()

#     # temp...this will return somethong later...
#     await sb_agent.run_workflow(nd_json, intro_uuid)
#     await sb_agent.run_workflow(nd_json, first_scene_uuid)


async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())

