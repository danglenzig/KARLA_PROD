import PySimpleGUI as sg
import asyncio
from uuid import uuid4
import json

from pathlib import Path
import sys

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from discovery_agent.discovery_agent import GUIDiscoveryAgent
from discovery_agent.discovery_agent_models import StoryConcept, DiscoveryAgentResponse

class ChatWindow():

    def __init__(self):
        self.layout = [
           [sg.Multiline(size=(100,26), key='-CHAT_LOG-', disabled=True)],
           [sg.Input(size=(100,10),key='-INPUT-')],
           [sg.Button('Submit'), sg.Button('Generate VN', disabled=True), sg.Button('Quit')],
           [sg.Button('Get Started')]
        ]
        self.session_id = str(uuid4())
        self.discovery_agent: GUIDiscoveryAgent = GUIDiscoveryAgent(self.session_id)
        self.window = sg.Window(f'Karla Chat {self.session_id}', self.layout)

    async def run_event_loop(self):

        initializing = True
        first_response: DiscoveryAgentResponse = await self.discovery_agent.handle_user_input("Okay let's get started.")
        initial_response = f"AGENT: {first_response.response_text}"
        print(initial_response) # <-- this prints to the log

        while True:
            event, values = self.window.read()

            if initializing:
                initializing = False
                self.window['-CHAT_LOG-'].update(initial_response)
                self.window.refresh() # <-- This doesn't do shit

            if event == 'Get Started':
                self.window['Get Started'].update(disabled= True)
                # This is stupid, but you need to press a button before the initial response text shows
                # up in -CHAT_LOG-

            if event == 'Submit' and values['-INPUT-']:

                user_message = values['-INPUT-']

                # add user msg to chat log
                log_str: str = values['-CHAT_LOG-']
                log_str += f"\n\nUSER: {user_message}"
                self.window['-CHAT_LOG-'].update(log_str)
                self.window['-INPUT-'].update("")
                
                response = await self.discovery_agent.handle_user_input(user_message)
                response_text = response.response_text
                print(response_text)

                log_str += f"\n\nAGENT: {response_text}"
                self.window['-CHAT_LOG-'].update(log_str)

                if response.concept_is_ready:
                    self.window['Submit'].update(disabled =True)
                    self.window['Generate VN'].update(disabled =False)

            if event == 'Generate VN':
                # TODO: hand off the concept to the game creation pipeline
                #  ^^this can take up to 5 minutes
                # for now just print the concept json dump.
                concept: StoryConcept = await self.discovery_agent.get_concept_summary()
                concept_json = concept.model_dump_json(indent=2)
                print(concept_json)
                break




            if event == sg.WINDOW_CLOSED or event == 'Quit':
                break



        self.window.close()

async def main():
    chat_window: ChatWindow = ChatWindow()
    await chat_window.run_event_loop()
    print("all done")

if __name__ == "__main__":
    asyncio.run(main())