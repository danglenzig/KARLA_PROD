# src/narrative_design_agent/narrative_design_agent_services.py

from agents import Agent, function_tool, ModelSettings
from openai.types.shared.reasoning import Reasoning
from openai.types.responses import ResponseTextDeltaEvent, ResponseReasoningSummaryTextDeltaEvent
from pathlib import Path
import sys
import uuid
import time

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from discovery_agent.discovery_agent_models import StoryConcept
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput, NarrativeDesignContentValidationResult
from utilities.custom_hooks import PrintToTerminalAgentHooks, UsageHooks

@function_tool
def get_uuid_string():
    return str(uuid.uuid4())

ND_AGENT_INSTRUCTIONS = f"""
You are a senior Narrative Designer at an indie game Studio that makes visual novel games in Ren'Py.
Your task is to turn the input story concept into detailed narrative design specification for a visual novel.
Your output will be used by downstream agents to generate visual assets, write dialogue, and code the game in Ren'Py. 

Every game shall have:
- Exactly one player character.
- Three or more non-player characters
- Three or more locations
- Exactly one intro scene, which introduces the narrative and orients the player
- Exactly three acts, each act conisting of 2-3 scenes
- Exactly one outro scene -- the game's denouement

Use the get_uuid_string tool to get UUID strings.

IMPORTANT: Remember that your visual descriptions will serve as input prompts AI image-generation agents. The image outputs of those agents will be the image assets for a Ren'Py visual novel game. In your character descriptions describe ONLY the character, not their surroundings, lighting, etc. The image generation agent already has strict rules about framing, composition, etc. so don't mention anything that might confuse it.
"""

def get_nd_workflow_input(story_concept: StoryConcept)->str:
    wf_input: str = f"""
Generate the NarrativeDesignOutput for the following story concept:
- PREMISE: {story_concept.premise}
- GENRE: {story_concept.genre}
- TONE: {story_concept.tone}
- SETTING: {story_concept.setting}
- PROTAGONIST: {story_concept.protagonist}
- CORE HOOK: {story_concept.core_hook}
- MUST-HAVE ELEMENTS: {story_concept.must_have_elements}
- AVOID ELEMENTS: {story_concept.avoid_elements}
- CONCEPT SUMMARY: {story_concept.concept_summary}
"""
    return wf_input


def get_narrative_design_agent(model_str: str)->Agent:
    return Agent(
        name="narrative_design_agent",
        model=model_str,
        instructions=ND_AGENT_INSTRUCTIONS,
        tools=[get_uuid_string],
        output_type=NarrativeDesignOutput,
        model_settings=ModelSettings(
            reasoning=Reasoning(
                effort="high",
                summary="detailed"
            )
        ),
        hooks=UsageHooks("narrative_design_agent")
    )

