# src/beat_sheet_agent/beat_sheet_services.py

import sys
from pathlib import Path
from agents import(
    Agent,
    RunContextWrapper,
    ModelSettings,
)
from openai.types.shared.reasoning import Reasoning

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from beat_sheet_agent.beat_sheet_models import(
    SceneBeat,
    SceneBeatSheet
)
from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    SceneData
)
from utilities.custom_hooks import PrintToTerminalAgentHooks, UsageHooks

MODEL = "gpt-5.4"

def get_sb_agent_input(
        nd_spec: NarrativeDesignOutput,
        scene_uuid: str
) -> str:
    # extract all the relevant data from the context
    scene_catalog       = nd_spec.get_scene_catalog() # scenes indexed by UUID
    if not scene_uuid in scene_catalog:
        raise ValueError ("scene_uuid not in catalogue")
    scene_data: SceneData = SceneData.model_validate(scene_catalog[scene_uuid])
    scene_name: str = scene_data.scene_name
    narrative_summary: str = scene_data.narrative_summary
    
    # write the promt string
    prompt_str = f"""Write the scene beats for {scene_name}.
Scene UUID: {scene_uuid}
Here is the scene's narrative summary from the Narrative Designer: {narrative_summary}"""
    
    return prompt_str

def get_sb_agent_instructions(
        wrapper: RunContextWrapper[NarrativeDesignOutput],
        agent: Agent[NarrativeDesignOutput]
) -> str:
    return f"""You are part of the narrative design team at a game studio that makes visual novel games in RenPy. Your specific job is to write scene beats.
For each scene, you create ordered beats, emptional turns, and choice opportunities that enrich the gameplay experience and preserve end-to-end narrative continuity.
Here is the story plan for the game you are currently working on, this is your context:\n
{wrapper.context.model_dump_json()}
"""

def get_sb_agent()->Agent:
    return Agent[NarrativeDesignOutput](
        name = "scene_beat_agent",
        instructions=get_sb_agent_instructions,
        output_type = SceneBeatSheet,
        model=MODEL,
        model_settings=ModelSettings(
            reasoning=Reasoning(
                effort='high',
                summary='detailed'
            )
        ),
        hooks=UsageHooks("scene_beat_agent")
    )