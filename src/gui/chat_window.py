import PySimpleGUI as sg
import asyncio
from uuid import uuid4
import json
from pydantic import BaseModel, Field
import threading
import gc

from pathlib import Path
import sys

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from discovery_agent.discovery_agent import GUIDiscoveryAgent
from discovery_agent.discovery_agent_models import StoryConcept, DiscoveryAgentResponse


# These are custom event names (consts) that our background workers will send
# back into the PySimpleGUI event loop.
#
# PySimpleGUI works best when the window loop handles events like:
# - button clicks
# - window close
# - "background task finished"
#
# So instead of waiting directly for the agent call inside the GUI loop,
# we will have a worker thread send one of these events when it finishes.
EVENT_INITIAL_RESPONSE = "-INITIAL_RESPONSE-"
EVENT_DISCOVERY_RESPONSE = "-DISCOVERY_RESPONSE-"
EVENT_CONCEPT_SUMMARY = "-CONCEPT_SUMMARY-"
EVENT_WORK_ERROR = "-WORK_ERROR-"
EVENT_VN_BUILD_COMPLETE = "-VN_BUILD_COMPLETE-"
EVENT_QUIT_HANDLED = "-QUIT_HANDLED-"


class ChatState(BaseModel):
    chat_lines: list[str]
    busy: bool
    concept_is_ready: bool


class KarlaGUI():
    def __init__(self):

        # Give this chat session a unique ID so the discovery agent can keep
        # one SQLite-backed conversation history for this window instance.
        self.session_id = str(uuid4())

        # This is the Stage 1 backend wrapper.
        # The GUI talks to this object rather than to the OpenAI runner directly.
        self.discovery_agent = GUIDiscoveryAgent(self.session_id)

        # Keep actual app state in Python variables, not inside the widgets.
        # widgets are for display and input, not for being your source of truth.
        self.chat_state: ChatState = ChatState(
            chat_lines=[],
            busy=False,
            concept_is_ready=False
        )

        sg.theme('NeonYellow1')

        # Build the layout
        # Multiline:
        # - used as read-only transcript display
        # - disabled=True prevents the user from editing it
        #
        # Status text:
        # - gives the user feedback while requests are in flight
        #
        # Input:
        # - single-line message box for the user's message
        #
        # Buttons:
        # - Submit sends a chat turn
        # - Generate VN is disabled until the discovery agent says the concept is ready
        # - Quit exits the app
        self.layout = [
            # row 0
            [
                sg.Multiline(
                    default_text = "",
                    key          = "-CHAT_LOG-",
                    size         = (100,26),
                    disabled     = True,
                    autoscroll   = True,
                    expand_x     = True,
                    expand_y     = True
                )
            ],
            # row 1
            [
                sg.Text(
                    "Status: starting discovery interview...",
                    key      = "-STATUS-",
                    expand_x = True
                )
            ],
            # row 2
            [
                # col 0
                [
                    sg.Input(
                        key      = "-INPUT-",
                        expand_x = True,
                        disabled = True
                    )
                ],
                # col 1
                [
                    sg.Button(
                        "Submit",
                        bind_return_key = True,
                        disabled        = True
                    )
                ]
            ],
            # row 3
            [
                # col 0
                [
                    sg.Button(
                        "Generate VN",
                        disabled = True
                    )
                ],
                # col 1
                [
                    sg.Button(
                        "Quit"
                    )
                ]
            ]
        ]

        # create the actual window
        self.window = sg.Window(
            f"Karla Chat {self.session_id}",
            self.layout,
            finalize  = True, # gives us a fully created window immediately, so we can start background work
            resizable = True  # quality-of-life
        )

    def append_chat(self, speaker: str, text: str) -> None:

        # store the transcrpt in the local state first
        self.chat_state.chat_lines.append(f"{speaker}: {text}")

        # Then rebuild the widget display from that state
        self.window["-CHAT_LOG-"].update("\n\n".join(self.chat_state.chat_lines))

    def set_busy(self, busy: bool, status_text: str) -> None:

        # track whether the app is currently waiting for a background request
        self.chat_state.busy = busy

        # update the gui status text, so the user knows what's up
        self.window["-STATUS-"].update(f"Status: {status_text}")

        # prevent new data entry when busy
        self.window["Submit"].update(disabled=busy)
        self.window["-INPUT-"].update(disabled=busy)

        # Generate VN should only be enabled when:
        # 1. we're not busy
        # 2. the discovery agent has said the concept is ready
        self.window["Generate VN"].update(
            disabled = busy or (not self.chat_state.concept_is_ready)
        )

    def run_async_task(self, coro_factory, finished_event_name: str) -> None:

        # this helper is the core of the pattern
        #
        # Here we...
        # 1. start a background thread
        # 2. run one async coroutine inside that thread with asyncio.run(...)
        # 3. send the result back to the gui with write_event_value(...)
        #
        # NOTE: we pass in a *factory* (a callable that returns a coroutine),
        # as a "lambda: ..." not an actual coroutine object. This keeps the
        # coroutine creation inside the worker thread.
        def worker() -> None:
            try:
                result = asyncio.run(coro_factory()) # asyncio.run(...) vs. await ...
                self.window.write_event_value(finished_event_name, result)
            except Exception as e:
                print(f"### KarlaGUI: {e}")
                self.window.write_event_value(EVENT_WORK_ERROR, str(e))

        # daemon=True means the thread won't prevent program exit
        threading.Thread(target=worker, daemon=True).start()

    def request_initial_prompt(self) -> None:

        # this gets the discovery agent's first interview question
        self.set_busy(True, "starting user interview...")

        # Start the agent call in the background with run_async_task
        self.run_async_task(
            # here's our coro factory
            lambda: self.discovery_agent.handle_user_input(
                "Okay let's get started."
            ),
            # here's the event string for the gui loop
            EVENT_INITIAL_RESPONSE
        )

    def handle_submit(self, user_message: str):

        # clean up the input
        clean_message = user_message.strip()

        # Ignore empty messages and refuse to submit if busy
        if not clean_message or self.chat_state.busy:
            print("### KarlaGUI: Bitch I'm busy!")
            return

        # show the user message immediately in the transcript
        self.append_chat("USER", clean_message)

        # Clear the input box after submitting
        self.window["-INPUT-"].update("")

        # Lock the GUI while waiting for the agent response
        self.set_busy(True, "awaiting agent response...")

        # Start the agent call in the background with run_async_task
        self.run_async_task(
            lambda: self.discovery_agent.handle_user_input(clean_message),
            EVENT_DISCOVERY_RESPONSE
        )

    def handle_discovery_response(self, response: DiscoveryAgentResponse) -> None:

        # when the agent call is finished, the GUI will receive one of the following
        # events:
        # 1. EVENT_INITIAL_RESPONSE, or...
        # 2. EVENT_DISCOVERY_RESPONSE
        #
        # In both cases, the payload is the same kind of object: a DiscoveryAgentResponse BaseModel
        self.append_chat("AGENT", response.response_text)

        # save whether or not the agent is ready to summarize
        self.chat_state.concept_is_ready = response.concept_is_ready

        # if the concept is ready, tell the user and enable Generate VN
        # they can continue chatting, and the summarizer agent will still
        # get new chat lines after this point from the SQLiteSession that
        # it shares with the convo agent
        if self.chat_state.concept_is_ready:
            self.window["-STATUS-"].update(
                "Status: The story concept is ready. You can keep chatting or generate the VN."
            )

        # unlock the input again
        self.set_busy(False, "ready")

    def handle_generate_vn(self) -> None:

        # Refuse to proceed if...
        # - a task is running
        # - the concept is not ready
        if self.chat_state.busy or not self.chat_state.concept_is_ready:
            print(f"### KarlaGUI: Something weird happened")
            return

        # Set busy and ask the summarizer for a StoryConcept
        self.set_busy(True, "building story concept...")
        self.run_async_task(
            # get_concept_summary takes no arguments, so we don't need "lambda: ..." syntax(?)
            self.discovery_agent.get_concept_summary,
            EVENT_CONCEPT_SUMMARY
        )

    def handle_concept_summary(self, concept: StoryConcept):

        # The summary is ready
        #self.set_busy(False, "concept summary ready")

        # disable further interaction
        #self.window["Submit"].update(disabled=True)
        #self.window["-INPUT-"].update(disabled=True)


        sg.popup_scrolled(
            concept.model_dump_json(indent=2),
            title="Story Concept",
            non_blocking=True, # <--let's think about how we want this
            size=(100, 30),
        )

    def start_vn_build(self, build_callable, concept: StoryConcept):
        self.set_busy(True, "Starting VN build")
        self.run_async_task(
            lambda: build_callable(concept),
            EVENT_VN_BUILD_COMPLETE
        )

    def notify_quit(self, quit_callable):
        self.run_async_task(
            lambda: quit_callable(),
            EVENT_QUIT_HANDLED
        )

    def handle_error(self, error_message: str) -> None:
        # do this if we get the evant EVENT_WORK_ERROR
        self.append_chat("SYSTEM", f"Error: {error_message}")

        # Also unlock the app so the user can try again
        self.set_busy(False, "request failed")

    def handle_status_update(self, status_message: str) -> None:
        self.window["-STATUS-"].update(status_message)


    def run(self, callback_dict: dict[str, callable]) -> None:

        # Kick it off with the initial discovery question
        # This will pop off EVENT_INITIAL_RESPONSE when complete
        self.request_initial_prompt()

        # And here's our main GUI event loop
        # all this is from the PySimpleGUI conventions
        # read an event, inspect it, update the GUI, repeat...
        while True:
            # here's our loop data
            event, values = self.window.read()

            # standard exit path
            if event == sg.WINDOW_CLOSED or event == "Quit":
                break
                #self.notify_quit(callback_dict['handle_gui_quit']) # <--I'd like to do this instead: let KarlaMain notify permission to quit

            #==============================
            # catch user interaction events
            #==============================
            # user clicked Submit
            if event == "Submit":
                self.handle_submit(values["-INPUT-"])

            # user clicked Generate VN
            elif event == "Generate VN":
                self.handle_generate_vn()

            #=====================================================
            # catch "work completed" events from our async workers
            #=====================================================
            elif event == EVENT_INITIAL_RESPONSE or event == EVENT_DISCOVERY_RESPONSE:
                response: DiscoveryAgentResponse = values[event]
                self.handle_discovery_response(response)

            elif event == EVENT_CONCEPT_SUMMARY:
                concept: StoryConcept = values[event]
                self.handle_concept_summary(concept)
                self.start_vn_build(callback_dict['build_from_concept'], concept)

            elif event == EVENT_VN_BUILD_COMPLETE:
                self.set_busy(False, "VN Build complete")

            #=========================
            # catch updates and errors
            #=========================
            elif event == EVENT_WORK_ERROR:
                self.handle_error(values[event])

            elif event == "-STATUS_UPDATE-":
                self.handle_status_update(values[event])

            elif event == EVENT_QUIT_HANDLED:
                break
        
        # Best practice from the PySimpleGUI docs
        # close the app, clean up, and force garbage collection
        self.window.close()
        self.layout = None
        self.window = None
        gc.collect()

def main():
    pass

if __name__ == "__main__":
    main()
