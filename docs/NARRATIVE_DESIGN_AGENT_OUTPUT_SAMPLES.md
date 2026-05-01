# NarrativeDesignAgent Output Samples (Model: GPT-5.4)

## Test Logic:

Test entry point in src/narrative_design_agent.py
Run as python module from terminal:
```
$ python3 -m src.narrative_design_agent
```

```python
async def main():

    test_input: str = "A scary story about an abandoned roadside motel in the rural New Mexico desert. The story is set in the year 1982."

    wf_input = WorkflowTextInput(
        input_as_text=test_input
    )

    output: NarrativeDesignOutputSchema = await NarrativeDesignAgent().run_workflow(wf_input)

    print(f"{json.dumps(output.model_dump(), indent=2)}")
    print(output.human_readable())

if __name__ == "__main__":
    asyncio.run(main())
```

## Output as JSON

`json.dumps(NarrativeDesignAgent().run_workflow(wf_input).model_dump(), indent=2)`

```json
{
  "story_title": "Last Light at Red Mesa",
  "synopsis": "In 1982, stranded radio stringer Mara Bell seeks shelter near Dry Wells, New Mexico, at the long-abandoned Red Mesa Motor Lodge, only to find a ghostly night clerk still checking in guests from a ledger that should have burned years ago. With a dust storm sealing the highway and the motel replaying a buried fire, Mara must work with wary locals and a runaway hiding on the property to uncover the truth behind the missing travelers before Red Mesa makes her one more permanent guest. The tone is slow-burn desert gothic horror with haunted Americana, analog-era unease, and escalating supernatural dread.",
  "player_character": {
    "character_data": {
      "uuid": "b2931ee3-23d9-4c71-beef-abe9cfe96e24",
      "name": "Mara Bell",
      "portrait_image_prompt": "A semi-realistic visual novel portrait of a 27-year-old woman in 1982, a traveling radio journalist and field recordist with dusty brown hair tied back, tired intelligent eyes, sun-worn skin, denim jacket over a plaid shirt, small cassette recorder slung on a strap, anxious but determined expression, subtle desert dust on her clothes, moody horror lighting, rural New Mexico atmosphere",
      "dialogue_examples": [
        "I came looking for a bed and a phone. If I get a ghost story instead, I'd at least like the truth.",
        "Static I can explain. A motel that changes shape when I blink, not so much.",
        "Don't tell me to leave unless you're willing to tell me what happened here in '71.",
        "If this place wants my name in that ledger, it'll have to spell it wrong."
      ]
    }
  },
  "non_player_characters": [
    {
      "character_data": {
        "uuid": "9ed7eb88-598b-477f-8db1-b2ded4ca9c85",
        "name": "Deputy Rosa Salazar",
        "portrait_image_prompt": "A semi-realistic visual novel portrait of a Hispanic woman in her late 40s, rural New Mexico county deputy in 1982, weathered face, dark hair streaked with gray pulled back, tan uniform shirt under a worn denim jacket, silver badge, steady stern gaze, practical no-nonsense posture, desert night shadows and patrol car light glow, grounded horror mood",
        "dialogue_examples": [
          "Folks in Dry Wells know better than to chase lights in the desert after midnight.",
          "That motel should be empty. Problem is, it never learned how.",
          "My father wore this badge before me, and some sins stain deeper than silver.",
          "If we're ending this tonight, we do it clean and we do it before dawn."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "cc71cb60-e397-4893-9f29-9e7f04d28df6",
        "name": "Eli Navarro",
        "portrait_image_prompt": "A semi-realistic visual novel portrait of a man in his early 30s, New Mexico mechanic and gas station attendant in 1982, grease-smudged hands, dark curly hair, faded work shirt with rolled sleeves, gentle but uneasy expression, fluorescent diner and gas pump lighting, dusty roadside atmosphere, subtle horror tension",
        "dialogue_examples": [
          "Your distributor cap's shot. I can have you rolling by sunup, if the wind doesn't bury us first.",
          "I don't drive past Red Mesa after dark, and I sure don't stop there.",
          "People around here call it bad luck. That's easier than calling it what it is.",
          "Take the keys, Ms. Bell. And if the radio starts talking back, don't answer."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "86207f8b-564d-4d70-a769-03802e1c0819",
        "name": "Danny Pike",
        "portrait_image_prompt": "A semi-realistic visual novel portrait of a 17-year-old runaway boy in 1982, skinny and sunburned, shaggy hair, oversized denim vest over a faded band shirt, wary eyes, dirt on his face, nervous posture like he is ready to bolt, harsh moonlight and motel neon, tense desert horror atmosphere",
        "dialogue_examples": [
          "I never checked in, okay? That's why it can't keep me.",
          "The hallway's longer after midnight. I counted.",
          "She smiles first. That's how you know you're in trouble.",
          "If you hear knocking from the wall, don't knock back."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "29905c95-87da-455d-822a-2abc5659394a",
        "name": "Miriam Voss",
        "portrait_image_prompt": "A semi-realistic visual novel portrait of a woman appearing in her 50s, eerie motel clerk from another era, immaculate faded turquoise uniform dress, carefully set hair, pale skin, red lipstick, polite smile that feels wrong, faint soot stains at the collar, lit by flickering neon and desk lamp, uncanny ghostly horror mood",
        "dialogue_examples": [
          "Welcome to Red Mesa Motor Lodge. We are always pleased to receive weary travelers.",
          "There is no need to be afraid, dear. Morning is such a short distance away.",
          "Guests who wander tend to lose themselves.",
          "I have kept the rooms ready for years. It would be rude of you not to stay."
        ]
      }
    }
  ],
  "locations": [
    {
      "location_data": {
        "uuid": "0c49de68-2f98-4f5e-9031-d8cb4e0992f4",
        "name": "Dry Wells Diner & Gas",
        "location_image_prompt": "A lonely roadside diner and two-pump gas station in rural New Mexico desert, year 1982, sunset turning to night, dust storm building on the horizon, flickering fluorescent sign, old pickup trucks, cracked asphalt, telephone poles, warm diner windows against vast empty desert, cinematic horror atmosphere"
      }
    },
    {
      "location_data": {
        "uuid": "0a7ad73a-720c-4259-8963-d6a47c4fc4d0",
        "name": "Red Mesa Motor Lodge Exterior",
        "location_image_prompt": "An abandoned U-shaped roadside motel in the rural New Mexico desert, year 1982, cracked neon VACANCY sign still glowing, boarded windows mixed with a few mysteriously lit rooms, rusted ice machine, drifting sand, empty courtyard, hints of a drained swimming pool, night dust storm, analog horror mood"
      }
    },
    {
      "location_data": {
        "uuid": "3f1e0854-6cfa-4750-8c62-d979859e639f",
        "name": "Motel Office and Corridor",
        "location_image_prompt": "The front office of an abandoned roadside motel blending into an impossible corridor, faux-wood paneling, rotary phone, brass room key wall, faded tourist brochures, dusty check-in ledger, patterned carpet stretching too far into darkness, sickly green fluorescent lighting, year 1982, eerie visual novel background"
      }
    },
    {
      "location_data": {
        "uuid": "179cf9f5-59e6-4458-93a6-13c33d623ccc",
        "name": "Room 8",
        "location_image_prompt": "A 1982 motel room interior in rural New Mexico, twin bed with floral bedspread, cigarette burns, analog clock radio, buzzing lamp, stained wallpaper shifting between clean and fire-scorched, ominous mirror, cheap wooden dresser, desert moonlight through venetian blinds, intimate supernatural horror atmosphere"
      }
    }
  ],
  "intro_scene": {
    "scene_data": {
      "location_uuid": "0c49de68-2f98-4f5e-9031-d8cb4e0992f4",
      "non_player_character_uuids": [
        "9ed7eb88-598b-477f-8db1-b2ded4ca9c85",
        "cc71cb60-e397-4893-9f29-9e7f04d28df6"
      ],
      "narrtive_summary": "Near sundown outside Dry Wells, Mara Bell coasts her failing sedan into the only diner and gas station for miles. Eli tells her the car will not be drivable until morning, while Deputy Rosa Salazar warns her not to seek shelter at the abandoned Red Mesa Motor Lodge because travelers connected to that place have a habit of vanishing from local memory as surely as they vanish from the highway. When a dust storm rolls in, the phone lines sputter, and every spare room in town is gone, Mara is forced toward the motel despite the warnings."
    }
  },
  "act_one": [
    {
      "scene_data": {
        "location_uuid": "0a7ad73a-720c-4259-8963-d6a47c4fc4d0",
        "non_player_character_uuids": [
          "86207f8b-564d-4d70-a769-03802e1c0819",
          "29905c95-87da-455d-822a-2abc5659394a"
        ],
        "narrtive_summary": "Mara crosses the storm-lashed road to Red Mesa and finds the supposedly abandoned motel lit by a flickering VACANCY sign, with fresh footprints in the dust and one office lamp burning. A gaunt runaway teen named Danny whispers from the shadows that she must not accept a room, but before he can explain, the front door opens and Miriam Voss greets Mara with the polished courtesy of a clerk who believes the motel is still in business. Drawn by equal parts fear, exhaustion, and professional curiosity, Mara steps inside."
      }
    },
    {
      "scene_data": {
        "location_uuid": "3f1e0854-6cfa-4750-8c62-d979859e639f",
        "non_player_character_uuids": [
          "86207f8b-564d-4d70-a769-03802e1c0819",
          "29905c95-87da-455d-822a-2abc5659394a"
        ],
        "narrtive_summary": "Inside the office, Miriam checks Mara in using a guest ledger whose most recent normal entries stop in 1971, and the corridor beyond the desk stretches farther than the building's exterior should allow. Danny slips in through a side door and urgently explains that he has been hiding on the property for days, watching the motel replay the same night and trap anyone who accepts a key after midnight. Mara takes the room key anyway, deciding to investigate the ledger's missing names and the motel's impossible geometry before the storm or the ghost can close around her."
      }
    }
  ],
  "act_two": [
    {
      "scene_data": {
        "location_uuid": "179cf9f5-59e6-4458-93a6-13c33d623ccc",
        "non_player_character_uuids": [
          "29905c95-87da-455d-822a-2abc5659394a"
        ],
        "narrtive_summary": "Room 8 shifts around Mara as she searches it: burnt wallpaper becomes pristine for a heartbeat, the clock radio spits out emergency calls and half-heard pleas, and mirror reflections lag behind her movements. Miriam appears in flashes as both gracious hostess and soot-streaked corpse while Mara witnesses fragments of the motel fire and hears guests pounding at locked doors that no longer exist. Hidden inside the mattress lining, Mara finds a postcard, scorched receipts, and a newspaper clipping that claims only two people died at Red Mesa, contradicting the many voices she heard."
      }
    },
    {
      "scene_data": {
        "location_uuid": "0a7ad73a-720c-4259-8963-d6a47c4fc4d0",
        "non_player_character_uuids": [
          "86207f8b-564d-4d70-a769-03802e1c0819",
          "9ed7eb88-598b-477f-8db1-b2ded4ca9c85"
        ],
        "narrtive_summary": "Guided by Danny, Mara searches the courtyard and drained pool area, uncovering luggage tags, license plates, and personal effects from travelers who should have been reported missing years earlier. Rosa arrives through the storm and admits that her late father, then a county deputy, helped bury evidence after the motel owner illegally chained a rear exit during the fire panic to stop guests from fleeing without paying. The three realize Miriam's spirit is trapped between guilt and denial, and that the motel's guest ledger anchors the haunting by binding every new check-in to the dead already waiting there."
      }
    }
  ],
  "act_three": [
    {
      "scene_data": {
        "location_uuid": "3f1e0854-6cfa-4750-8c62-d979859e639f",
        "non_player_character_uuids": [
          "86207f8b-564d-4d70-a769-03802e1c0819",
          "29905c95-87da-455d-822a-2abc5659394a"
        ],
        "narrtive_summary": "Mara returns to the office to confront Miriam with the hidden names, the false death count, and the truth of the chained exit. Miriam first pleads with trembling sincerity for Mara to stay until morning, then turns possessive and monstrous when Mara reaches for the ledger and the master keys. As Danny distracts the shifting corridor and the motel begins folding in on itself, Mara learns the final rule of Red Mesa: destroying the ledger before dawn can free the trapped guests, but the last person to sign in risks being taken in their place."
      }
    },
    {
      "scene_data": {
        "location_uuid": "0a7ad73a-720c-4259-8963-d6a47c4fc4d0",
        "non_player_character_uuids": [
          "9ed7eb88-598b-477f-8db1-b2ded4ca9c85",
          "86207f8b-564d-4d70-a769-03802e1c0819",
          "29905c95-87da-455d-822a-2abc5659394a"
        ],
        "narrtive_summary": "In the heart of the storm beneath the flickering VACANCY sign, Mara uses her cassette recorder to play back the voices of the victims, forcing Miriam to relive the night she failed to save them. Rosa overloads the sign's failing transformer while Danny hurls the guest ledger into the shower of sparks, igniting decades of paper, dust, and denial. As the motel peels back from welcoming illusion to blackened ruin, Miriam must choose between dragging Mara into the fire as a replacement guest or opening the way for the dead to finally leave Red Mesa behind."
      }
    }
  ],
  "outro_scene": {
    "scene_data": {
      "location_uuid": "0c49de68-2f98-4f5e-9031-d8cb4e0992f4",
      "non_player_character_uuids": [
        "9ed7eb88-598b-477f-8db1-b2ded4ca9c85",
        "cc71cb60-e397-4893-9f29-9e7f04d28df6",
        "86207f8b-564d-4d70-a769-03802e1c0819"
      ],
      "narrtive_summary": "At dawn, Red Mesa is nothing but a collapsed shell half-buried in sand, with no sign that its lights ever burned through the night. Rosa quietly commits to reopening the old case, Danny accepts a ride out of Dry Wells and his first real chance to start over, and Eli returns Mara's repaired car keys beside a stack of warped cassette tapes recovered from the wreckage. Mara drives east into the sunrise believing she escaped, until Miriam's velvet voice bleeds through the static of the car radio with one final promise: there are still vacancies."
    }
  }
}
```

## Human Readable

`NarrativeDesignAgent().run_workflow(wf_input).human_readable()`

TITLE: Last Light at Red Mesa


SYNOPSIS: In 1982, stranded radio stringer Mara Bell seeks shelter near Dry Wells, New Mexico, at the long-abandoned Red Mesa Motor Lodge, only to find a ghostly night clerk still checking in guests from a ledger that should have burned years ago. With a dust storm sealing the highway and the motel replaying a buried fire, Mara must work with wary locals and a runaway hiding on the property to uncover the truth behind the missing travelers before Red Mesa makes her one more permanent guest. The tone is slow-burn desert gothic horror with haunted Americana, analog-era unease, and escalating supernatural dread.


PLAYER CHARCTER: Mara Bell

  VISUAL: A semi-realistic visual novel portrait of a 27-year-old woman in 1982, a traveling radio journalist and field recordist with dusty brown hair tied back, tired intelligent eyes, sun-worn skin, denim jacket over a plaid shirt, small cassette recorder slung on a strap, anxious but determined expression, subtle desert dust on her clothes, moody horror lighting, rural New Mexico atmosphere

  DIALOGUE EXAMPLES:
    'I came looking for a bed and a phone. If I get a ghost story instead, I'd at least like the truth.'
    'Static I can explain. A motel that changes shape when I blink, not so much.'
    'Don't tell me to leave unless you're willing to tell me what happened here in '71.'
    'If this place wants my name in that ledger, it'll have to spell it wrong.'

  UUID: b2931ee3-23d9-4c71-beef-abe9cfe96e24


NON-PLAYER CHARACTERS:

  NPC: Deputy Rosa Salazar

    VISUAL: A semi-realistic visual novel portrait of a Hispanic woman in her late 40s, rural New Mexico county deputy in 1982, weathered face, dark hair streaked with gray pulled back, tan uniform shirt under a worn denim jacket, silver badge, steady stern gaze, practical no-nonsense posture, desert night shadows and patrol car light glow, grounded horror mood

    DIALOGUE EXAMPLES:
      'Folks in Dry Wells know better than to chase lights in the desert after midnight.'
      'That motel should be empty. Problem is, it never learned how.'
      'My father wore this badge before me, and some sins stain deeper than silver.'
      'If we're ending this tonight, we do it clean and we do it before dawn.'

    UUID: 9ed7eb88-598b-477f-8db1-b2ded4ca9c85

  NPC: Eli Navarro

    VISUAL: A semi-realistic visual novel portrait of a man in his early 30s, New Mexico mechanic and gas station attendant in 1982, grease-smudged hands, dark curly hair, faded work shirt with rolled sleeves, gentle but uneasy expression, fluorescent diner and gas pump lighting, dusty roadside atmosphere, subtle horror tension

    DIALOGUE EXAMPLES:
      'Your distributor cap's shot. I can have you rolling by sunup, if the wind doesn't bury us first.'
      'I don't drive past Red Mesa after dark, and I sure don't stop there.'
      'People around here call it bad luck. That's easier than calling it what it is.'
      'Take the keys, Ms. Bell. And if the radio starts talking back, don't answer.'

    UUID: cc71cb60-e397-4893-9f29-9e7f04d28df6

  NPC: Danny Pike

    VISUAL: A semi-realistic visual novel portrait of a 17-year-old runaway boy in 1982, skinny and sunburned, shaggy hair, oversized denim vest over a faded band shirt, wary eyes, dirt on his face, nervous posture like he is ready to bolt, harsh moonlight and motel neon, tense desert horror atmosphere

    DIALOGUE EXAMPLES:
      'I never checked in, okay? That's why it can't keep me.'
      'The hallway's longer after midnight. I counted.'
      'She smiles first. That's how you know you're in trouble.'
      'If you hear knocking from the wall, don't knock back.'

    UUID: 86207f8b-564d-4d70-a769-03802e1c0819

  NPC: Miriam Voss

    VISUAL: A semi-realistic visual novel portrait of a woman appearing in her 50s, eerie motel clerk from another era, immaculate faded turquoise uniform dress, carefully set hair, pale skin, red lipstick, polite smile that feels wrong, faint soot stains at the collar, lit by flickering neon and desk lamp, uncanny ghostly horror mood

    DIALOGUE EXAMPLES:
      'Welcome to Red Mesa Motor Lodge. We are always pleased to receive weary travelers.'
      'There is no need to be afraid, dear. Morning is such a short distance away.'
      'Guests who wander tend to lose themselves.'
      'I have kept the rooms ready for years. It would be rude of you not to stay.'

    UUID: 29905c95-87da-455d-822a-2abc5659394a


LOCATIONS:

  Dry Wells Diner & Gas:

    VISUAL: A lonely roadside diner and two-pump gas station in rural New Mexico desert, year 1982, sunset turning to night, dust storm building on the horizon, flickering fluorescent sign, old pickup trucks, cracked asphalt, telephone poles, warm diner windows against vast empty desert, cinematic horror atmosphere

    UUID: 0c49de68-2f98-4f5e-9031-d8cb4e0992f4

  Red Mesa Motor Lodge Exterior:

    VISUAL: An abandoned U-shaped roadside motel in the rural New Mexico desert, year 1982, cracked neon VACANCY sign still glowing, boarded windows mixed with a few mysteriously lit rooms, rusted ice machine, drifting sand, empty courtyard, hints of a drained swimming pool, night dust storm, analog horror mood

    UUID: 0a7ad73a-720c-4259-8963-d6a47c4fc4d0

  Motel Office and Corridor:

    VISUAL: The front office of an abandoned roadside motel blending into an impossible corridor, faux-wood paneling, rotary phone, brass room key wall, faded tourist brochures, dusty check-in ledger, patterned carpet stretching too far into darkness, sickly green fluorescent lighting, year 1982, eerie visual novel background

    UUID: 3f1e0854-6cfa-4750-8c62-d979859e639f

  Room 8:

    VISUAL: A 1982 motel room interior in rural New Mexico, twin bed with floral bedspread, cigarette burns, analog clock radio, buzzing lamp, stained wallpaper shifting between clean and fire-scorched, ominous mirror, cheap wooden dresser, desert moonlight through venetian blinds, intimate supernatural horror atmosphere

    UUID: 179cf9f5-59e6-4458-93a6-13c33d623ccc


INTRO:

  LOCATION: Dry Wells Diner & Gas

  NON-PLAYER  CHARACTERS:
    Deputy Rosa Salazar
    Eli Navarro

  SCENE SYNOPSIS: Near sundown outside Dry Wells, Mara Bell coasts her failing sedan into the only diner and gas station for miles. Eli tells her the car will not be drivable until morning, while Deputy Rosa Salazar warns her not to seek shelter at the abandoned Red Mesa Motor Lodge because travelers connected to that place have a habit of vanishing from local memory as surely as they vanish from the highway. When a dust storm rolls in, the phone lines sputter, and every spare room in town is gone, Mara is forced toward the motel despite the warnings.


ACT I:

  SCENE 1, LOCATION Red Mesa Motor Lodge Exterior

  NON-PLAYER CHARACTERS:
    Danny Pike
    Miriam Voss

  SCENE SYNOPSIS: Mara crosses the storm-lashed road to Red Mesa and finds the supposedly abandoned motel lit by a flickering VACANCY sign, with fresh footprints in the dust and one office lamp burning. A gaunt runaway teen named Danny whispers from the shadows that she must not accept a room, but before he can explain, the front door opens and Miriam Voss greets Mara with the polished courtesy of a clerk who believes the motel is still in business. Drawn by equal parts fear, exhaustion, and professional curiosity, Mara steps inside.

  SCENE 2, LOCATION Motel Office and Corridor

  NON-PLAYER CHARACTERS:
    Danny Pike
    Miriam Voss

  SCENE SYNOPSIS: Inside the office, Miriam checks Mara in using a guest ledger whose most recent normal entries stop in 1971, and the corridor beyond the desk stretches farther than the building's exterior should allow. Danny slips in through a side door and urgently explains that he has been hiding on the property for days, watching the motel replay the same night and trap anyone who accepts a key after midnight. Mara takes the room key anyway, deciding to investigate the ledger's missing names and the motel's impossible geometry before the storm or the ghost can close around her.


ACT II:

  SCENE 1, LOCATION Room 8

  NON-PLAYER CHARACTERS:
    Miriam Voss

  SCENE SYNOPSIS: Room 8 shifts around Mara as she searches it: burnt wallpaper becomes pristine for a heartbeat, the clock radio spits out emergency calls and half-heard pleas, and mirror reflections lag behind her movements. Miriam appears in flashes as both gracious hostess and soot-streaked corpse while Mara witnesses fragments of the motel fire and hears guests pounding at locked doors that no longer exist. Hidden inside the mattress lining, Mara finds a postcard, scorched receipts, and a newspaper clipping that claims only two people died at Red Mesa, contradicting the many voices she heard.

  SCENE 2, LOCATION Red Mesa Motor Lodge Exterior

  NON-PLAYER CHARACTERS:
    Danny Pike
    Deputy Rosa Salazar

  SCENE SYNOPSIS: Guided by Danny, Mara searches the courtyard and drained pool area, uncovering luggage tags, license plates, and personal effects from travelers who should have been reported missing years earlier. Rosa arrives through the storm and admits that her late father, then a county deputy, helped bury evidence after the motel owner illegally chained a rear exit during the fire panic to stop guests from fleeing without paying. The three realize Miriam's spirit is trapped between guilt and denial, and that the motel's guest ledger anchors the haunting by binding every new check-in to the dead already waiting there.


ACT III:

  SCENE 1, LOCATION Motel Office and Corridor

  NON-PLAYER CHARACTERS:
    Danny Pike
    Miriam Voss

  SCENE SYNOPSIS: Mara returns to the office to confront Miriam with the hidden names, the false death count, and the truth of the chained exit. Miriam first pleads with trembling sincerity for Mara to stay until morning, then turns possessive and monstrous when Mara reaches for the ledger and the master keys. As Danny distracts the shifting corridor and the motel begins folding in on itself, Mara learns the final rule of Red Mesa: destroying the ledger before dawn can free the trapped guests, but the last person to sign in risks being taken in their place.

  SCENE 2, LOCATION Red Mesa Motor Lodge Exterior

  NON-PLAYER CHARACTERS:
    Deputy Rosa Salazar
    Danny Pike
    Miriam Voss

  SCENE SYNOPSIS: In the heart of the storm beneath the flickering VACANCY sign, Mara uses her cassette recorder to play back the voices of the victims, forcing Miriam to relive the night she failed to save them. Rosa overloads the sign's failing transformer while Danny hurls the guest ledger into the shower of sparks, igniting decades of paper, dust, and denial. As the motel peels back from welcoming illusion to blackened ruin, Miriam must choose between dragging Mara into the fire as a replacement guest or opening the way for the dead to finally leave Red Mesa behind.


OUTRO:

  LOCATION: Dry Wells Diner & Gas

  NON-PLAYER  CHARACTERS:
    Deputy Rosa Salazar
    Eli Navarro
    Danny Pike

  SCENE SYNOPSIS: At dawn, Red Mesa is nothing but a collapsed shell half-buried in sand, with no sign that its lights ever burned through the night. Rosa quietly commits to reopening the old case, Danny accepts a ride out of Dry Wells and his first real chance to start over, and Eli returns Mara's repaired car keys beside a stack of warped cassette tapes recovered from the wreckage. Mara drives east into the sunrise believing she escaped, until Miriam's velvet voice bleeds through the static of the car radio with one final promise: there are still vacancies.