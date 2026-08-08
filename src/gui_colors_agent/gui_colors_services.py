# src/gui_colors_agent/gui_colors_services.py

from pathlib import Path
import sys
from agents import(
    Agent
)


SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from gui_colors_agent.gui_colors_models import GuiColorScheme
from narrative_design_agent.narrative_design_agent_models import NarrativeDesignOutput
from utilities.custom_hooks import PrintToTerminalAgentHooks, UsageHooks

def get_gui_color_agent_instructions(nd_spec: NarrativeDesignOutput):
    visual_data: str = nd_spec.human_readable()
    agent_instructions = f"""Generate a GUI color scheme for the visual novel based on the following input from the Narrative Designer:
{visual_data}"""
    return agent_instructions

def get_gui_color_agent() -> Agent:
    return Agent(
        name="gui_color_agent",
        model="gpt-5.4-mini",
        instructions="""You are an expert in UI design and color theory. Your inputs are text comments from the game's narrative designer, which describe the story synopsis and visual descriptions of a few scene locations. Your task is to select interface text colors that are readable and consistent with the mood and tone of the game.
        You select colors for the following:
            accent_color: An accent color used throughout the interface to label and highlight text.
            idle_color: The color used for a normal text button when it is neither selected nor hovered.
            idle_small_color: "The used for a small text button when it is neither selected nor hovered.
            hover_color: The color that is used for buttons and bars that are hovered.
            selected_color: The color used for a text button when it is selected but not focused. A button is selected if it is the current screen or preference value.
            insensitive_color: The color used for a text button when it cannot be selected.
            muted_color: Color used for the portions of bars that are not filled in. This is not used directly, but is used when re-generating bar image files.
            hover_muted_color: Color used for the portions of bars that are hovered but not filled in. This is not used directly, but is used when re-generating bar image files.
            text_color: The colors used for dialogue text
            interface_text_color: The colors used for menu choice text

        Your output_type is GuiColorScheme, which is a Pydantic BaseModel containing descriptive fields for each of these. The type for each of these fields is RGBA8 (also a Pydantic BaseModel) which is a standard 8-bit color model (0-255 for each channel).""",
        output_type=GuiColorScheme,
        hooks=UsageHooks("gui_color_agent")
        )