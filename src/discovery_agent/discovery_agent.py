# src/discovery_agent/discovery_agent.py

# TODO: discovery -> summarizer handoff with hitl approval
# https://openai.github.io/openai-agents-python/handoffs/
# https://openai.github.io/openai-agents-python/human_in_the_loop/

from dotenv import load_dotenv
load_dotenv()

import asyncio
from pathlib import Path
import sys
import uuid
from agents import (
    Agent, Runner, RunResult, SQLiteSession
)

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from discovery_agent.discovery_agent_models import StoryConcept
from discovery_agent.discovery_agent_services import (
    get_discovery_agent,
    get_discovery_summarizer_agent
)

GPT_MODEL = "gpt-5.4"

class DiscoveryAgent():
    def __init__(self):
        self.discovery_agent: Agent = get_discovery_agent(GPT_MODEL)
        self.discovery_summarizer: Agent = get_discovery_summarizer_agent(GPT_MODEL)

    async def say_hello(self)->str:
        return("DiscoveryAgent says hello.")
    
    def get_new_session_id(self) -> str:
        return str(uuid.uuid4())
    
    async def run_workflow(self) -> StoryConcept:
        """
        Conducts the user interview and returns a StoryConcept.
        """
        convo_session: SQLiteSession = SQLiteSession(self.get_new_session_id())
        user_message = "Hello, I'm ready to talk about my visual novel. Go ahead and ask your questions."

        run_result: RunResult = await Runner.run(
            self.discovery_agent,
            user_message,
            session=convo_session
        )
        print(f"AGENT: {run_result.final_output}\n")

        while True:

            items = await convo_session.get_items()
            session_length = len(items)

            user_message = input("--> ").strip()
            if not user_message:
                continue
            if user_message.lower() in {"done", "summarize", "enough"}:
                break

            run_result: RunResult = await Runner.run(
                self.discovery_agent,
                user_message,
                session=convo_session
            )
            print(f"{run_result.final_output}\n")

        summary_result: RunResult = await Runner.run(
            self.discovery_summarizer,
            "Summarize the conversation session into a StoryConcept",
            session=convo_session
        )

        return summary_result.final_output_as(StoryConcept)
    
async def main():
    pass

if __name__ == "__main__":
    asyncio.run(main())