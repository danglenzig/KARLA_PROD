from dotenv import load_dotenv
from pathlib import Path
import asyncio
import sys
from agents import (
    Runner,
    RunResult,
    Agent
)
from pydantic import ValidationError

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))
from dialogue_agent.dialogue_agent_services import get_dialogue_agent
from dialogue_agent.dialogue_agent_models import (
    DialogueScene,
    CharacterDialogueData
)
from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    CharacterData
)
from beat_sheet_agent.beat_sheet_models import SceneBeatSheet
from misc_models.misc_models import DemoCreativeData

load_dotenv()

class DialogueAgent():

    async def run_scene_workflow(self, nd_spec: NarrativeDesignOutput, beat_sheet: SceneBeatSheet)->DialogueScene:
        agent: Agent = get_dialogue_agent(nd_spec)

        input_str = f"\n#======\n# INPUT\n#======\n"
        input_str += f"""\nProduce a DialogueScene output for the scene indicated by this beat sheet. The beat sheet contains contextual information about:
        - scene identity
- location identity
- player and non-player character UUIDs
- ordered beats
- each beat's purpose, summary, mood, focal character, present characters, interactivity flag, choice prompt, branch outcomes, and exit state. Here is the beat sheet for this scene:
\n{beat_sheet.model_dump_json(indent=2)}\n\n"""

        # add player character data to input string
        player_data: CharacterDialogueData = CharacterDialogueData(
            character_uuid         = nd_spec.player_character.character_data.uuid,
            character_name         = nd_spec.player_character.character_data.name,
            character_description  = nd_spec.player_character.character_data.portrait_image_prompt,
            example_dialogue_lines = nd_spec.player_character.character_data.dialogue_examples
        )
        input_str += f"""\nHere is contextual information about the player character:
{player_data.model_dump_json(indent=2)}\n\n"""

        # add npc data to input string
        character_catalog = nd_spec.get_character_catalog()
        npcs_list: list[CharacterDialogueData] = []
        if not beat_sheet.non_player_character_uuids is None:
            if len(beat_sheet.non_player_character_uuids) > 0:
                for id in beat_sheet.non_player_character_uuids:
                    char_dict = character_catalog[id]
                    try:
                        char_data: CharacterData = CharacterData.model_validate(char_dict)
                    except ValidationError as e:
                        print(e)
                    char_name     = char_data.name
                    char_desc     = char_data.portrait_image_prompt
                    example_lines = char_data.dialogue_examples
                    dialogue_data: CharacterDialogueData = CharacterDialogueData(
                        character_uuid         = id,
                        character_name         = char_name,
                        character_description  = char_desc,
                        example_dialogue_lines = example_lines
                    )
                    npcs_list.append(dialogue_data)
        if len(npcs_list) > 0:
            npcs_info_str = ""
            for data in npcs_list:
                npcs_info_str += f"{data.model_dump_json(indent=2)}\n"
            input_str += f"""\nHere is contextual information about the non-player characters in this scene:
{npcs_info_str}\n"""

            print(f"\nGenerating dialogue data for {beat_sheet.scene_name}\n")
            run_result: RunResult = await Runner.run(
                agent,
                input=input_str
            )

            return run_result.final_output_as(DialogueScene)

async def main():
    print("FOO")
    file: str = 'test_creative_data.json'
    try:
        with open(f'/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_REFACTOR/json/{file}', 'r') as f:
            json_str = f.read().strip()
            creative_data: DemoCreativeData = DemoCreativeData.model_validate_json(json_str)

            nd_spec: NarrativeDesignOutput = creative_data.narrative_design_spec
            intro_beat_sheet: SceneBeatSheet = creative_data.beat_sheets[0]
            first_scene_beat_sheet: SceneBeatSheet = creative_data.beat_sheets[1]

            #print(f"{nd_spec.model_dump_json(indent=2)}\n\n")
            #print(f"{intro_beat_sheet.model_dump_json(indent=2)}\n\n")

            result_intro: DialogueScene = await DialogueAgent().run_scene_workflow(nd_spec,intro_beat_sheet)
            result_first_scene: DialogueScene = await DialogueAgent().run_scene_workflow(nd_spec, first_scene_beat_sheet)

            test_folder_path = f"/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_REFACTOR/json"
            intro_path: str = f"{test_folder_path}/intro_dialogue_scene.json"
            first_scene_path: str = f"{test_folder_path}/first_scene_dialogue_scene.json"

            with open(intro_path, 'w') as f:
                f.write(result_intro.model_dump_json(indent=2))
            with open (first_scene_path, 'w') as f:
                f.write(result_first_scene.model_dump_json(indent=2))

            

    except Exception as e:
        print(e)

if __name__ == "__main__":
    asyncio.run(main())

