# src/discovery_agent/discovery_agent_models.py

from pydantic import (
    BaseModel, Field
)

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
