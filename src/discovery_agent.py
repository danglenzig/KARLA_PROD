# src/discovery_agent.py

from dotenv import load_dotenv
from pydantic import BaseModel, Field
import asyncio
import uuid
from agents import (
    Agent,
    Runner,
    RunResult,
    SQLiteSession
)

load_dotenv()

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

class StoryConcept(BaseModel):
    premise: str = Field(..., description="Core story premise")
    genre: str | None = Field(default=None, description="The genre of the story")
    tone: str | None = Field(default=None, description="The emotional tone of the story")
    setting: str | None = Field(default=None, description="A description of the place and time that the story takes place in")
    protagonist: str | None = Field(default=None, description="Information for the Narrative Designer about the player-character/protagonist. Gender, age, personality, etc")
    core_hook: str = Field(...,description="Main dramatic hook or conflict")
    must_have_elements: list[str] = Field(default_factory=list, description="Story elements, tropes, etc. that the Narrative Designer MUST include")
    avoid_elements: list[str] = Field(default_factory=list, description="Story elements, tropes, etc. that the Narrative Designer SHOUL avoid")
    concept_summary: str = Field(..., description="3-4 sentence handoff summary for the Narrative Design Agent")

class DiscoveryAgent():

    def __init__(self):
        self.discovery_agent = Agent(
            name="discovery_agent",
            model="gpt-5.4",
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
""",
)

    def get_new_session_id(self) -> str:
        return str(uuid.uuid4())
    
    async def run_workflow(self) -> StoryConcept:
        convo_session: SQLiteSession = SQLiteSession(self.get_new_session_id())
        user_message = "Hello, I'm ready to talk about my visual novel. Go ahead and ask your questions."

        run_result: RunResult = await Runner.run(
            self.discovery_agent,
            user_message,
            session=convo_session
        )

        print(f"AGENT: {run_result.final_output}\n")

        while True:
            user_message = input("--> ").strip()
            if not user_message:
                continue
            if user_message.lower() in {"done", "summarize", "enough"}:
                break

            run_result = await Runner.run(
                self.discovery_agent,
                user_message,
                session=convo_session
            )
            print(f"{run_result.final_output}\n")

        discovery_summarizer: Agent = Agent(
            name="discovery_summarizer",
            model="gpt-5.4",
            instructions=(
                "You will receive the full discovery conversation for a visual novel concept. "
                "Return a structured StoryConcept object. "
                "Infer reasonable defaults only when strongly supported by the conversation. "
                "Write a concise but vivid concept_summary suitable for handoff to a Narrative Design Agent."
            ),
            output_type=StoryConcept
        )

        summary_result: RunResult = await Runner.run(
            discovery_summarizer,
            "Summarize the conversation session into a StoryConcept",
            session=convo_session
        )

        return summary_result.final_output
        

        



async def main():
    # run as module to test:
    # $ python3 -m src.discovery_agent
    result: StoryConcept = await DiscoveryAgent().run_workflow()
    print("====FINAL CONCEPT====\n")
    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(main())