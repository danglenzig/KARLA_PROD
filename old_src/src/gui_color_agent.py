from dotenv import load_dotenv
from agents import Agent, Runner, RunResult
from pydantic import BaseModel, Field, computed_field
from pathlib import Path
import sys
import json
import asyncio

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent import NarrativeDesignOutputSchema, LocationData




class RBGA8(BaseModel):
    """Standard 8-bit color model."""
    r: int = Field(..., ge=0, le=255, description="Red channel between 0 and 255")
    g: int = Field(..., ge=0, le=255, description="Green channel between 0 and 255")
    b: int = Field(..., ge=0, le=255, description="Blue channel between 0 and 255")
    a: int = Field(255, ge=0, le=255, description="Alpha channel between 0 and 255")

    @computed_field
    @property
    def hex_string(self) -> str:
        """Returns the color as a CSS-style hex string"""
        return f"#{self.r:02X}{self.g:02X}{self.b:02X}"

DEFAULT_ACCENT_COLOR: RBGA8         = RBGA8.model_validate({ "r":   0, "g": 153, "b": 204 })
DEFAULT_IDLE_COLOR: RBGA8           = RBGA8.model_validate({ "r": 136, "g": 136, "b": 136 })
DEFAULT_IDLE_SMALL_COLOR: RBGA8     = RBGA8.model_validate({ "r": 170, "g": 170, "b": 170 })
DEFAULT_HOVER_COLOR: RBGA8          = RBGA8.model_validate({ "r": 102, "g": 193, "b": 224 })
DEFAULT_SELECTED_COLOR: RBGA8       = RBGA8.model_validate({ "r": 255, "g": 255, "b": 255 })
DEFAULT_INSENSITIVE_COLOR: RBGA8    = RBGA8.model_validate({ "r":  85, "g":  85, "b":  85 })
DEFAULT_MUTED_COLOR: RBGA8          = RBGA8.model_validate({ "r":   0, "g":  61, "b":  81 })
DEFAULT_HOVER_MUTED_COLOR: RBGA8    = RBGA8.model_validate({ "r":   0, "g":  91, "b": 122 })
DEFAULT_TEXT_COLOR: RBGA8           = RBGA8.model_validate({ "r": 255, "g": 255, "b": 255 })
DEFAULT_INTERFACE_TEXT_COLOR: RBGA8 = RBGA8.model_validate({ "r": 255, "g": 255, "b": 255 })

class GuiColorScheme(BaseModel):
    """Color scheme for the visual novel text"""
    accent_color: RBGA8         = Field(DEFAULT_ACCENT_COLOR, description="An accent color used throughout the interface to label and highlight text.")
    idle_color: RBGA8           = Field(DEFAULT_IDLE_COLOR, description="The color used for a normal text button when it is neither selected nor hovered.")
    idle_small_color: RBGA8     = Field(DEFAULT_IDLE_SMALL_COLOR, description="The used for a small text button when it is neither selected nor hovered.")
    hover_color: RBGA8          = Field(DEFAULT_HOVER_COLOR, description="The color that is used for buttons and bars that are hovered.")
    selected_color: RBGA8       = Field(DEFAULT_SELECTED_COLOR, description="The color used for a text button when it is selected but not focused. A button is selected if it is the current screen or preference value.")
    insensitive_color: RBGA8    = Field(DEFAULT_INSENSITIVE_COLOR, description="The color used for a text button when it cannot be selected.")
    muted_color: RBGA8          = Field(DEFAULT_MUTED_COLOR, description="Color used for the portions of bars that are not filled in. This is not used directly, but is used when re-generating bar image files.")
    hover_muted_color: RBGA8    = Field(DEFAULT_HOVER_MUTED_COLOR, description="Color used for the portions of bars that are hovered but not filled in. This is not used directly, but is used when re-generating bar image files.")
    text_color: RBGA8           = Field(DEFAULT_TEXT_COLOR, description="The colors used for dialogue text")
    interface_text_color: RBGA8 = Field(DEFAULT_INTERFACE_TEXT_COLOR, description="The colors used for menu choice text")
    reasoning: str              = Field(..., description="A brief summary of why these particular colors were selected")


color_agent: Agent = Agent(
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

Your output_type is GuiColorScheme, which is a Pydantic BaseModel containing descriptive fields for each of these. The type for each of these fields is RGBA8 (also a Pydantic BaseModel) which is a standard 8-bit color model (0-255 for each channel).
""",
    output_type=GuiColorScheme
)



class GuiColorAgent():
    async def run_workflow(self, in_json: str) -> GuiColorScheme:

        try:
            nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(in_json)
        except Exception as e:
            print(e)

        visual_data: str = nd_spec.human_readable()

        agent_instructions = f"""Generate a GUI color scheme for the visual novel based on the following input from the Narrative Designer:
{visual_data}"""

        result: RunResult = await Runner.run(
            color_agent,
            agent_instructions   
        )

        return result.final_output

async def main():
    try:
        with open('KARLA_GAMES/COLOR_AGENT_TESTING/test_data.json') as f:
            json_str = f.read().strip()
        nd_spec: NarrativeDesignOutputSchema = NarrativeDesignOutputSchema.model_validate_json(json_str)
        gui_color_scheme: GuiColorScheme = await GuiColorAgent().run_workflow(json_str)
        print(gui_color_scheme.model_dump_json(indent=2))   

    except Exception as e:
        print(e)

if __name__ == "__main__":
    #schema = GuiColorScheme.model_json_schema()
    #print(json.dumps(schema, indent=2))
    asyncio.run(main())


# TEST OUTPUT:
# {
#   "accent_color": {
#     "r": 255,
#     "g": 106,
#     "b": 58,
#     "a": 255,
#     "hex_string": "#FF6A3A"
#   },
#   "idle_color": {
#     "r": 216,
#     "g": 201,
#     "b": 181,
#     "a": 255,
#     "hex_string": "#D8C9B5"
#   },
#   "idle_small_color": {
#     "r": 190,
#     "g": 173,
#     "b": 155,
#     "a": 255,
#     "hex_string": "#BEAD9B"
#   },
#   "hover_color": {
#     "r": 255,
#     "g": 146,
#     "b": 92,
#     "a": 255,
#     "hex_string": "#FF925C"
#   },
#   "selected_color": {
#     "r": 255,
#     "g": 178,
#     "b": 118,
#     "a": 255,
#     "hex_string": "#FFB276"
#   },
#   "insensitive_color": {
#     "r": 117,
#     "g": 104,
#     "b": 94,
#     "a": 255,
#     "hex_string": "#75685E"
#   },
#   "muted_color": {
#     "r": 88,
#     "g": 78,
#     "b": 71,
#     "a": 255,
#     "hex_string": "#584E47"
#   },
#   "hover_muted_color": {
#     "r": 112,
#     "g": 97,
#     "b": 86,
#     "a": 255,
#     "hex_string": "#706156"
#   },
#   "text_color": {
#     "r": 241,
#     "g": 228,
#     "b": 214,
#     "a": 255,
#     "hex_string": "#F1E4D6"
#   },
#   "interface_text_color": {
#     "r": 248,
#     "g": 236,
#     "b": 222,
#     "a": 255,
#     "hex_string": "#F8ECDE"
#   },
#   "reasoning": "I chose a palette that feels like faded neon, rust, cigarette smoke, and desert dusk. The accent and hover colors lean into hot motel-sign orange for a cursed, attention-grabbing 1980s roadside feel, while the text and interface colors stay warm, bone-colored, and highly readable against dark, grimy backgrounds. Muted browns and soot tones support the abandoned interior and pool-courtyard mood without clashing with the more saturated neon highlights."
# }