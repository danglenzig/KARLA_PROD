import asyncio
import sys
from pathlib import Path

SRC_ROOT: Path = Path(__file__).parent.parent # this is the src/ folder
sys.path.insert(0, str(SRC_ROOT))

from narrative_design_agent.narrative_design_agent_models import (
    NarrativeDesignOutput,
    NarrativeDesignContentValidationResult,
    SceneData
)

def get_nd_spec_validation_results(nd_spec: NarrativeDesignOutput) -> NarrativeDesignContentValidationResult:
    result: NarrativeDesignContentValidationResult = NarrativeDesignContentValidationResult()
    comment_list: list[str] = []

    loc_ids: list[str] = nd_spec.get_location_uuids()
    char_ids: list[str] = nd_spec.get_character_uuids()

    # check that no location ids are duplicated
    has_duplicate_loc_ids: bool = len(loc_ids) != len(set(loc_ids))
    if has_duplicate_loc_ids:
        result.has_problems = True
        comment_list.append("- One or more of the location UUIDs is a duplicate\n")

    # check that no character uuids are duplicated
    has_duplicate_char_ids = len(char_ids) != len(set(char_ids))
    if has_duplicate_char_ids:
        result.has_problems = True
        comment_list.append("- One or more of the character UUIDs is a duplicate\n")

    intro_scene_data: SceneData = nd_spec.intro_scene.scene_data
    outro_scene_data: SceneData = nd_spec.outro_scene.scene_data

    act_one_scene_datas: list [SceneData] = []
    for scene in nd_spec.act_one:
        act_one_scene_datas.append(scene.scene_data)

    act_two_scene_datas: list [SceneData] = []
    for scene in nd_spec.act_two:
        act_two_scene_datas.append(scene.scene_data)

    act_three_scene_datas: list [SceneData] = []
    for scene in nd_spec.act_three:
        act_three_scene_datas.append(scene.scene_data)

    # check for unknown locations
    unknown_loc_ids: list[str] = []

    if intro_scene_data.location_uuid not in loc_ids:
        unknown_loc_ids.append(f"- Intro scene has a bad location UUID: Location with UUID {intro_scene_data.location_uuid} is not in the locations list\n")

    if outro_scene_data.location_uuid not in loc_ids:
        unknown_loc_ids.append(f"- Outro scene has a bad location UUID: Location with UUID {outro_scene_data.location_uuid} is not in the locations list\n")

    for scene_data in act_one_scene_datas:
        if scene_data.location_uuid not in loc_ids:
            unknown_loc_ids.append(f"- Act one has a scene with a bad location UUID: Location with UUID {scene_data.location_uuid} is not in the locations list\n")

    for scene_data in act_two_scene_datas:
        if scene_data.location_uuid not in loc_ids:
            unknown_loc_ids.append(f"- Act two has a scene with a bad location UUID: Location with UUID {scene_data.location_uuid} is not in the locations list\n")

    for scene_data in act_three_scene_datas:
        if scene_data.location_uuid not in loc_ids:
            unknown_loc_ids.append(f"- Act three has a scene with a bad location UUID: Location with UUID {scene_data.location_uuid} is not in the locations list\n")

    if len(unknown_loc_ids) > 0:
        result.has_problems = True
        comment_list.append("".join(unknown_loc_ids))

    #validate scene character IDs
    unknown_chars_list: list[str] = []

    if intro_scene_data.non_player_character_uuids != None: # if the scene has npcs
        for npc_uuid in intro_scene_data.non_player_character_uuids:
            if npc_uuid not in char_ids:
                unknown_chars_list.append(f"- Intro has a bad NPC UUID: NPC with UUID {npc_uuid} is not in the non-player-characters list")
        
    if outro_scene_data.non_player_character_uuids != None:
        for npc_uuid in outro_scene_data.non_player_character_uuids:
            if npc_uuid not in char_ids:
                unknown_chars_list.append(f"- Outro has a bad NPC UUID: NPC with UUID {npc_uuid} is not in the non-player-characters list")

    for scene_data in act_one_scene_datas:
        # TODO correect the syntax to 'if not ... is None'
        # TODO add len(...) >0 check
        if scene_data.non_player_character_uuids != None:
            for npc_uuid in scene_data.non_player_character_uuids:
                if npc_uuid not in char_ids:
                    unknown_chars_list.append(f"- Act one has a bad NPC UUID: NPC with UUID {npc_uuid} is not in the non-player-characters list")

    for scene_data in act_two_scene_datas:
        # TODO correect the syntax to 'if not ... is None'
        # TODO add len(...) >0 check
        if scene_data.non_player_character_uuids != None:
            for npc_uuid in scene_data.non_player_character_uuids:
                if npc_uuid not in char_ids:
                    unknown_chars_list.append(f"- Act two has a bad NPC UUID: NPC with UUID {npc_uuid} is not in the non-player-characters list")


    for scene_data in act_three_scene_datas:
        # TODO correect the syntax to 'if not ... is None'
        # TODO add len(...) >0 check
        if scene_data.non_player_character_uuids != None:
            for npc_uuid in scene_data.non_player_character_uuids:
                if npc_uuid not in char_ids:
                    unknown_chars_list.append(f"- Act three has a bad NPC UUID: NPC with UUID {npc_uuid} is not in the non-player-characters list")

    if len(unknown_chars_list) > 0:
        result.has_problems = True
        comment_list.append("".join(unknown_chars_list))


    if result.has_problems:
        result.comments = "".join(comment_list)
    else:
        result.comments = "The spec is problem-free"

    return result

async def main():
    #file: str = 'test_nd_spec.json'
    file: str = 'duplicate_char_ids.json'
    try:
        with open(f'/mnt/c/SchoolRepos/PYTHON/KARLA_RECOVER/KARLA_REFACTOR/json/{file}', 'r') as f:
            json_str = f.read().strip()
            nd_spec: NarrativeDesignOutput = NarrativeDesignOutput.model_validate_json(json_str)

            val_result: NarrativeDesignContentValidationResult = get_nd_spec_validation_results(nd_spec)

            print(val_result.comments)

    except Exception as e:
        print(e)



if __name__ == "__main__":
    asyncio.run(main())