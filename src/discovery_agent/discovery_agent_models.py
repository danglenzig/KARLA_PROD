# src/discovery_agent/discovery_agent_models.py

from pydantic import (
    BaseModel, Field
)


class DiscoveryAgentResponse(BaseModel):
    """
    A model representing one user-agent interaction in an ongoing conversation
    """
    session_id: str = Field(..., description="The SQLite session associate with this conversation")
    concept_is_ready: bool = Field(..., description="Whether or not you have enough information yet to formulate story concept. When you set this value to True, the orchectrator will hand off the session history to the next agent, and your work will be complete.")
    response_text: str = Field(..., description="The text of your next message to the user")

class StoryConcept(BaseModel):
    """
    A model representing a high-level visual novel story concept
    """
    premise: str = Field(..., description="The core story premise")
    genre: str | None = Field(default=None, description="The genre of the story")
    tone: str | None = Field(default=None, description="The emotional tone of the story")
    setting: str | None = Field(default=None, description="A description of the place and time that the story takes place in")
    protagonist: str | None = Field(default=None, description="Information for the Narrative Designer about the player-character/protagonist. Gender, age, personality, etc")
    core_hook: str = Field(...,description="Main dramatic hook or conflict")
    must_have_elements: list[str] = Field(default_factory=list, description="Story elements, tropes, etc. that the Narrative Designer MUST include")
    avoid_elements: list[str] = Field(default_factory=list, description="Story elements, tropes, etc. that the Narrative Designer SHOULD avoid")
    concept_summary: str = Field(..., description="3-4 sentence handoff summary for the Narrative Design Agent")
