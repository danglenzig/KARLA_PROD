import sys
from pathlib import Path
from pydantic import BaseModel
from typing import Literal
import random
import asyncio

# LOCAL MODULES
SRC_ROOT: Path = Path(__file__).parent # the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from renpy_script_assembler import DemoBuildData
from gui_color_agent import GuiColorScheme
from gui_script_helper import GUI_PREAMBLE, GUI_POSTAMBLE




class GuiScriptAssembler():

    async def run_workflow(self, color_scheme: GuiColorScheme)->str:
        script_rpy = f"{GUI_PREAMBLE}\n"

        accent_hex         = color_scheme.accent_color.hex_string
        idle_hex           = color_scheme.idle_color.hex_string
        idle_small_hex     = color_scheme.idle_small_color.hex_string
        hover_hex          = color_scheme.hover_color.hex_string
        selected_hex       = color_scheme.selected_color.hex_string
        insensitive_hex    = color_scheme.insensitive_color.hex_string
        muted_hex          = color_scheme.muted_color.hex_string
        hover_muted_hex    = color_scheme.hover_muted_color.hex_string
        text_hex           = color_scheme.text_color.hex_string
        interface_text_hex = color_scheme.interface_text_color.hex_string

        script_rpy += f"\ndefine gui.accent_color = '{accent_hex}'\n"
        script_rpy += f"\ndefine gui.idle_color = '{idle_hex}'\n"
        script_rpy += f"\ndefine gui.idle_small_color = '{idle_small_hex}'\n"
        script_rpy += f"\ndefine gui.hover_color = '{hover_hex}'\n"
        script_rpy += f"\ndefine gui.selected_color = '{selected_hex}'\n"
        script_rpy += f"\ndefine gui.insensitive_color = '{insensitive_hex}'\n"
        script_rpy += f"\ndefine gui.muted_color = '{muted_hex}'\n"
        script_rpy += f"\ndefine gui.hover_muted_color = '{hover_muted_hex}'\n"
        script_rpy += f"\ndefine gui.text_color = '{text_hex}'\n"
        script_rpy += f"\ndefine gui.interface_text_color = '{interface_text_hex}'\n"

        script_rpy += f"{GUI_POSTAMBLE}"

        return script_rpy

async def main():
    with open('KARLA_GAMES/intern of the _sundog/DATA/build_data.json', 'r') as f:
        build_data_json = f.read().strip()
    bd: DemoBuildData = DemoBuildData.model_validate_json(build_data_json)
    colors: GuiColorScheme = bd.gui_colors

    gui_script = await GuiScriptAssembler().run_workflow(colors)

    print(gui_script)

    import os
    path = "KARLA_GAMES/intern of the _sundog/DATA/gui.rpy"
    with open(path, 'w') as f:
        f.write(gui_script)


if __name__ == "__main__":
    asyncio.run(main())