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


class DiscoveryAgent():

    discovery_agent: Agent = Agent(
        name="discovery_agent",
        model="gpt-5.4",
        instructions="You chat with the user and come up with a visual novel story concept that they will enjoy" ## Placeholder -- need better instructions
    )

    def get_new_session_id(self) -> str:
        return str(uuid.uuid4())
    
    async def run_workflow(self) -> str:

        # called from the orchestrator with:
        #   story_concept: str = await DiscoveryAgent().run_workflow()

        # session for chat continuity
        sesh: SQLiteSession = SQLiteSession(self.get_new_session_id())

        initial_input: str = "Hello, I'm ready to talk about my visual novel. Go ahead ang ask your questions."
        initial_result: RunResult = await Runner.run(
            self.discovery_agent,
            initial_input,
            session=sesh
        )

        # this should be the agent's first question
        print(f" AGENT: {initial_result.final_output}\n")

        ## chat while loop will go here...
        ## the agent asks the user questions until it has enough information
        ##  to write a 3-4 sentence synopsis or story concept to pass to the
        ##  narrative design agent.

        return ""   # <-- this should be the final output of the discovery agent
                    # example: Write a scary story about an abandoned motel in the rural New Mexico desert. It shouuld have a female protagonist and be set in the early 1980s.



async def main():
    # run as module to test:
    # $ python3 -m src.discovery_agent
    result: str = await DiscoveryAgent().run_workflow()
    print(f"\n\n{result}")

if __name__ == "__main__":
    asyncio.run(main())