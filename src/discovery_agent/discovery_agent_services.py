from agents import Agent
from pathlib import Path
import sys

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from discovery_agent.discovery_agent_models import StoryConcept, DiscoveryAgentResponse
from utilities.custom_hooks import UsageHooks

DISCOVERY_INSTRUCTIONS_PREFACE = """
You are the Discovery Agent for Project Karla, a visual novel generator. Your job is to talk with the user and help them arrive at a strong visual novel concept.
Ask one clear question at a time. Prefer specific, practical questions over vague ones. If the user is unsure, offer 2-4 concrete options or examples. Do not 
write the final concept too early. First gather enough information about genre, tone, setting, protagonist, and core conflict or hook. Once you have enough 
information, clearly say that you are ready to summarize the concept. Keep replies concise and conversational.
"""

STORY_CONCEPT_GUIDE = """
The final story concept should be detailed enough to fill these fields:

- premise: the basic setup of the story in 1-2 sentences
- genre: the primary genre, such as horror, romance, mystery, sci-fi
- tone: the emotional flavor, such as eerie, cozy, tragic, playful
- setting: the time period, place, and overall world context
- protagonist: who the player mainly follows
- core_hook: the central conflict, mystery, relationship, or dramatic engine
- must_have_elements: specific things the user wants included
- avoid_elements: specific things the user does not want
- concept_summary: a concise 3-4 sentence story concept for handoff

Your job is not to output these fields directly.
Your job is to ask questions that help you discover them naturally through conversation.
Ask one question at a time.
Stop once you have enough information to confidently infer all of the above.
"""

DISCOVERY_BEHAVIOR_RULES = """
Behavior rules:
- Be concise and conversational.
- Ask one focused question at a time.
- Prefer high-yield questions.
- If the user seems unsure, offer 2-4 concrete options.
- Do not start outlining acts or scenes.
- Do not write the final concept too early.
- Once you have enough information, say so clearly.
"""


def get_discovery_agent(model_str: str)->Agent:
    return Agent(
        name = "discovery_agent",
        model=model_str,
        hooks=UsageHooks("discovery_agent"),
        instructions=f"""You are the Discovery Agent for Project Karla, a visual novel generator. Your job is to talk with the user and help them arrive at a strong visual novel concept.
Ask one clear question at a time. Prefer specific, practical questions over vague ones. If the user is unsure, offer 2-4 concrete options or examples. Do not 
write the final concept too early. First gather enough information about genre, tone, setting, protagonist, and core conflict or hook. Once you have enough 
information, clearly say that you are ready to summarize the concept. Keep replies concise and conversational.

{STORY_CONCEPT_GUIDE}

Behavior rules:
- Be concise and conversational.
- Ask one focused question at a time.
- Prefer high-yield questions.
- If the user seems unsure, offer 2-4 concrete options.
- Do not start outlining acts or scenes.
- Do not write the final concept too early.
- Once you have enough information, say so clearly.
"""
    )

def get_gui_discovery_agent(model_str: str)->Agent:
    return Agent(
        name = "gui_discovery_agent",
        model = model_str,
        hooks=UsageHooks("gui_discovery_agent"),
        instructions=f"""{DISCOVERY_INSTRUCTIONS_PREFACE}

{STORY_CONCEPT_GUIDE}

{DISCOVERY_BEHAVIOR_RULES}""",
        output_type=DiscoveryAgentResponse
    )

def get_discovery_summarizer_agent(model_str: str)->Agent:
    return Agent(
        name = "discovery_summarizer",
        model=model_str,
        hooks=UsageHooks("discovery_summarizer"),
        instructions=(
            "You will receive the full discovery conversation for a visual novel concept."
            "Return a structured StoryConcept object."
            "Infer reasonable defaults only when strongly supported by the conversation."
            "Write a concise but vivid concept_summary suitable for handoff to a Narrative Design Agent."
            "If the conversation doesn't have enough details to establish the StoryConcept fields, then use your own imagination to fill in the blanks."
        ),
        output_type=StoryConcept
    )