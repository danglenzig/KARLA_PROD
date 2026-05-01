# NarrativeDesignAgent Output Samples (Model: GPT-5.4)

## Test Logic:

Test entry point in src/narrative_design_agent.py
Run as python module from terminal:
```
$ python3 -m src.narrative_design_agent
```

### Code:
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
  "story_title": "Vacancy at Lost Mesa",
  "synopsis": "In 1982, Albuquerque radio repair technician Rosa Medina becomes stranded on a lonely stretch of rural New Mexico highway beside the long-abandoned Lost Mesa Motor Lodge. Drawn in by a voice on a dead radio frequency, she finds a terrified young photographer, a superstitious deputy, a guilt-ridden former housekeeper, and the ghost of the motel's last night clerk all circling the same secret: something beneath the motel has learned how to lure travelers, record their names, and keep the night from ending. The tone is slow-burn, dusty, claustrophobic supernatural horror with analog-radio unease, shifting architecture, and a haunted roadside Americana atmosphere.",
  "player_character": {
    "character_data": {
      "uuid": "a3e929b5-3f88-4e9b-b289-3b39b57bc277",
      "name": "Rosa Medina",
      "portrait_image_prompt": "Bust portrait of a Latina woman in her late 20s, practical and sharp-eyed, dark curly hair tied back loosely, denim jacket over a faded mechanic's work shirt, a small toolkit and cassette recorder strap visible, desert dust on her clothes, tired but determined expression, 1982 roadside aesthetic, cinematic visual novel style, moody horror lighting",
      "dialogue_examples": [
        "A dead battery I can fix. A dead radio station calling my name is new.",
        "If this place is abandoned, then who keeps answering the phone?",
        "Don't tell me to relax while the room numbers keep changing.",
        "I work with wires, switches, and signals. If this thing can talk, it can be answered.",
        "We're getting out before sunrise, even if I have to pull this motel apart one circuit at a time."
      ]
    }
  },
  "non_player_characters": [
    {
      "character_data": {
        "uuid": "f0e64695-7782-42e0-9d44-a7586752ee1d",
        "name": "June Mercer",
        "portrait_image_prompt": "Bust portrait of a young white woman around 20, bleached blonde hair with dark roots, thrift-store jacket over a band tee, camera strap around her neck, smudged eyeliner, scared but defiant expression, 1982 desert punk style, harsh motel neon and moonlight, visual novel horror portrait",
        "dialogue_examples": [
          "I stopped for pictures before sunset. Then the road stopped making sense.",
          "Don't open any door that's already unlocked. I'm serious.",
          "The motel likes people who look lost. You look very lost.",
          "If you hear an ice machine, run. There isn't one."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "dba0ae9f-5de9-469d-8d9c-804de340d580",
        "name": "Deputy Tom Baca",
        "portrait_image_prompt": "Bust portrait of a Hispanic man in his early 40s, rural sheriff's deputy uniform from 1982, thick mustache, weathered face, flashlight and hat in hand, stern posture hiding deep unease, dusty New Mexico lawman aesthetic, dim patrol-car light and motel neon glow, visual novel style",
        "dialogue_examples": [
          "Folks around here know better than to stop at Lost Mesa after dark.",
          "I've seen coyotes strip a car to bones. This place scares me more.",
          "Stay where I can see you. If the lights come on by themselves, we leave.",
          "In this county, the desert keeps what it wants."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "955507a9-601f-48fa-909d-154de2de5a63",
        "name": "Dolores Varela",
        "portrait_image_prompt": "Bust portrait of an elderly Latina woman in her late 60s, deeply lined face, gray braid, worn cardigan, rosary wrapped around one hand, old flashlight in the other, solemn and haunted expression, desert wind and motel dust, candlelike warm rim light against cold night shadows, visual novel horror portrait",
        "dialogue_examples": [
          "It was a decent place once, before the water went bad and the prayers stopped working.",
          "Names matter in that office. Don't give the building yours.",
          "I buried the ledger years ago. I should have burned it.",
          "The dead don't haunt this motel, mija. Something else taught them how."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "7cde0937-9599-4023-be55-c15a836222b9",
        "name": "Virgil Bell",
        "portrait_image_prompt": "Bust portrait of a gaunt middle-aged man in a faded motel clerk blazer, combed hair, hollow eyes, cigarette-stained fingers, polite smile that feels wrong, caught between 1950s hospitality and ghostly decay, flickering fluorescent office light, eerie visual novel portrait",
        "dialogue_examples": [
          "Welcome to the Lost Mesa Motor Lodge. Vacancy has a way of finding people.",
          "You needn't trouble yourself with signing in. I've already prepared your key.",
          "We never had a Room 7 until the night it asked for one.",
          "If the radio asks for a name, please give it mine."
        ]
      }
    },
    {
      "character_data": {
        "uuid": "ea2a30ce-0037-4e78-9edc-570d3b54b380",
        "name": "The Mother Road Voice",
        "portrait_image_prompt": "Surreal dialogue portrait of a human face half-formed from radio static, motel neon, and black water reflections, features shifting and indistinct, no clear age or gender, analog distortion, CRT scanlines, threatening calm expression, supernatural desert horror aesthetic",
        "dialogue_examples": [
          "Driver, you have reached your final vacancy.",
          "Please sign clearly. We dislike errors in the register.",
          "Morning has been delayed for your convenience.",
          "Every guest returns. Some simply take the long road."
        ]
      }
    }
  ],
  "locations": [
    {
      "location_data": {
        "uuid": "06f305cb-1ddc-4711-b267-340c4bac597f",
        "name": "Highway Pullout at Lost Mesa",
        "location_image_prompt": "1982 rural New Mexico desert highway at dusk, empty two-lane road, faded turquoise roadside sign for LOST MESA MOTOR LODGE, dusty station wagon with hood up, telephone poles, red mesas on the horizon, gathering storm clouds, lonely roadside horror atmosphere, cinematic background art"
      }
    },
    {
      "location_data": {
        "uuid": "e5afbf45-d4d0-47cf-b354-dd8f1781cf9d",
        "name": "Motel Lobby and Office",
        "location_image_prompt": "Abandoned roadside motel office in 1982, dusty wood paneling, cracked vinyl chairs, front desk with brass bell, key cubbies, rotary phone, analog tabletop radio, faded tourist brochures, dead neon glow and flickering fluorescent light, eerie analog horror background"
      }
    },
    {
      "location_data": {
        "uuid": "471f21d5-1f21-419e-af27-793ba40bde2a",
        "name": "Exterior Walkway and Room 7",
        "location_image_prompt": "Nighttime exterior of a decaying desert motel, cracked stucco walls, long shadowy walkway, mismatched room numbers, an ominous Room 7 door where it should not fit, flickering red VACANCY sign, windblown dust, deep pools of darkness, supernatural horror background"
      }
    },
    {
      "location_data": {
        "uuid": "f4348bb0-923a-49e8-a982-188341042800",
        "name": "Drained Pool Courtyard",
        "location_image_prompt": "Desert motel courtyard under pale moonlight, empty cracked swimming pool full of weeds and blown sand, rusted lounge chairs, dry palm tree, broken chain-link fence, open New Mexico sky, eerie stillness and drifting debris, cinematic horror background"
      }
    },
    {
      "location_data": {
        "uuid": "5403788c-b106-462a-8d51-7416173b4f62",
        "name": "Pump House and Black-Water Cistern",
        "location_image_prompt": "Subterranean motel pump house beneath the desert, concrete stairs, rusted pipes, dangling bare bulbs, jury-rigged radio transmitter equipment, black water cistern reflecting weak light, cramped oppressive shadows, analog supernatural horror background"
      }
    }
  ],
  "intro_scene": {
    "scene_data": {
      "location_uuid": "06f305cb-1ddc-4711-b267-340c4bac597f",
      "non_player_character_uuids": [
        "f0e64695-7782-42e0-9d44-a7586752ee1d",
        "ea2a30ce-0037-4e78-9edc-570d3b54b380"
      ],
      "narrtive_summary": "Rosa's station wagon dies on a deserted highway after her dashboard radio crackles to life on an unused frequency and guides her toward the abandoned Lost Mesa Motor Lodge. At the roadside sign she meets June Mercer, a frightened young photographer who claims she has already tried to leave several times and somehow keeps returning to the same pullout. The intro establishes the 1982 desert setting, Rosa's practical need for a phone or help, and the first impossible hint that the motel is calling stranded travelers by name."
    }
  },
  "act_one": [
    {
      "scene_data": {
        "location_uuid": "e5afbf45-d4d0-47cf-b354-dd8f1781cf9d",
        "non_player_character_uuids": [
          "f0e64695-7782-42e0-9d44-a7586752ee1d",
          "955507a9-601f-48fa-909d-154de2de5a63",
          "7cde0937-9599-4023-be55-c15a836222b9"
        ],
        "narrtive_summary": "Searching for a phone, Rosa and June enter the motel office and find it shifting between dust-choked ruin and a fully lit version of itself from decades earlier. Virgil Bell, the courteous night clerk, behaves as though the motel is open and tries to coax Rosa into signing the guest ledger, while Dolores Varela appears outside and urgently warns her not to write her name anywhere. The scene introduces the motel's rules, its unsettling hospitality, and the idea that accepting shelter here may be more dangerous than the desert outside."
      }
    },
    {
      "scene_data": {
        "location_uuid": "471f21d5-1f21-419e-af27-793ba40bde2a",
        "non_player_character_uuids": [
          "f0e64695-7782-42e0-9d44-a7586752ee1d",
          "dba0ae9f-5de9-469d-8d9c-804de340d580",
          "ea2a30ce-0037-4e78-9edc-570d3b54b380"
        ],
        "narrtive_summary": "Deputy Tom Baca arrives after spotting Rosa's stranded car, but every attempt to drive the women away bends the road back to the same cracked motel walkway. Room numbers shift when nobody is looking, and the impossible Room 7 appears under the flickering VACANCY sign as radios in the nearby rooms begin broadcasting the Mother Road Voice. The act closes with the cast realizing they are trapped on motel grounds until they understand what is holding them there."
      }
    }
  ],
  "act_two": [
    {
      "scene_data": {
        "location_uuid": "f4348bb0-923a-49e8-a982-188341042800",
        "non_player_character_uuids": [
          "f0e64695-7782-42e0-9d44-a7586752ee1d",
          "955507a9-601f-48fa-909d-154de2de5a63",
          "7cde0937-9599-4023-be55-c15a836222b9"
        ],
        "narrtive_summary": "In the moonlit courtyard, Dolores admits she once worked at Lost Mesa and explains that after a deadly flood and a string of vanished motorists, the motel began changing at night. June shows Rosa her Polaroids, each one revealing extra figures around the drained pool and one image that seems to include Rosa before she ever arrived. Virgil appears at the poolside in a moment of cracked lucidity, suggesting that something beneath the motel learned how to speak through radios, intercoms, and guest records."
      }
    },
    {
      "scene_data": {
        "location_uuid": "471f21d5-1f21-419e-af27-793ba40bde2a",
        "non_player_character_uuids": [
          "dba0ae9f-5de9-469d-8d9c-804de340d580",
          "7cde0937-9599-4023-be55-c15a836222b9",
          "ea2a30ce-0037-4e78-9edc-570d3b54b380"
        ],
        "narrtive_summary": "Rosa investigates Room 7 and discovers a space that is larger inside than the building allows, filled with suitcases and keepsakes belonging to missing travelers from many different years. Virgil confesses that he kept checking people in under orders from the Voice, which promises the night will end if a new clerk agrees to take his place. When Deputy Baca tries to burn the ledger and break the pattern by force, the hallway warps and drags him toward the pump house while the Mother Road Voice calmly announces that the motel is preparing a permanent reservation."
      }
    }
  ],
  "act_three": [
    {
      "scene_data": {
        "location_uuid": "5403788c-b106-462a-8d51-7416173b4f62",
        "non_player_character_uuids": [
          "f0e64695-7782-42e0-9d44-a7586752ee1d",
          "dba0ae9f-5de9-469d-8d9c-804de340d580",
          "955507a9-601f-48fa-909d-154de2de5a63",
          "ea2a30ce-0037-4e78-9edc-570d3b54b380"
        ],
        "narrtive_summary": "Guided by Dolores, Rosa and June descend into the pump house and discover an old emergency radio relay wired into a black-water cistern beneath the motel. Deputy Baca is found alive but injured, and Dolores reveals that the motel's owner once used the transmitter to lure stranded motorists before something in the water began answering back and taking control of the place. Rosa realizes her knowledge of radios gives her a chance either to overload the system or retune it long enough to free the trapped voices tied to the ledger."
      }
    },
    {
      "scene_data": {
        "location_uuid": "e5afbf45-d4d0-47cf-b354-dd8f1781cf9d",
        "non_player_character_uuids": [
          "f0e64695-7782-42e0-9d44-a7586752ee1d",
          "dba0ae9f-5de9-469d-8d9c-804de340d580",
          "955507a9-601f-48fa-909d-154de2de5a63",
          "7cde0937-9599-4023-be55-c15a836222b9",
          "ea2a30ce-0037-4e78-9edc-570d3b54b380"
        ],
        "narrtive_summary": "As the motel fully reanimates around them with blazing lights, phantom guests, and doors slamming in sequence, Rosa uses the office intercom and the retuned transmitter to call every stolen name back out of the building. Virgil rebels against the Voice long enough for Rosa to destroy the guest ledger and sever Room 7 from the rest of the motel, while Dolores stays behind to shut the office and hold the entity in place. The climax forces the cast to choose survival over certainty as the illusion of hospitality collapses into darkness and rushing black water."
      }
    }
  ],
  "outro_scene": {
    "scene_data": {
      "location_uuid": "06f305cb-1ddc-4711-b267-340c4bac597f",
      "non_player_character_uuids": [
        "f0e64695-7782-42e0-9d44-a7586752ee1d",
        "dba0ae9f-5de9-469d-8d9c-804de340d580"
      ],
      "narrtive_summary": "At dawn, Rosa, June, and Deputy Baca reach the highway and find the Lost Mesa Motor Lodge reduced to old concrete slabs and a fallen sign, as if it has been abandoned for decades. June's photographs develop almost completely blank except for one frame showing the office light still burning, and Rosa's repaired radio whispers the word vacancy one last time before going silent. The story ends with the survivors driving toward town unsure whether Dolores and Virgil were finally laid to rest, leaving relief and lingering dread in equal measure."
    }
  }
}
```

## Human Readable

`NarrativeDesignAgent().run_workflow(wf_input).human_readable()`

TITLE: Vacancy at Lost Mesa


SYNOPSIS: In 1982, Albuquerque radio repair technician Rosa Medina becomes stranded on a lonely stretch of rural New Mexico highway beside the long-abandoned Lost Mesa Motor Lodge. Drawn in by a voice on a dead radio frequency, she finds a terrified young photographer, a superstitious deputy, a guilt-ridden former housekeeper, and the ghost of the motel's last night clerk all circling the same secret: something beneath the motel has learned how to lure travelers, record their names, and keep the night from ending. The tone is slow-burn, dusty, claustrophobic supernatural horror with analog-radio unease, shifting architecture, and a haunted roadside Americana atmosphere.


PLAYER CHARCTER: Rosa Medina

  VISUAL: Bust portrait of a Latina woman in her late 20s, practical and sharp-eyed, dark curly hair tied back loosely, denim jacket over a faded mechanic's work shirt, a small toolkit and cassette recorder strap visible, desert dust on her clothes, tired but determined expression, 1982 roadside aesthetic, cinematic visual novel style, moody horror lighting

  DIALOGUE EXAMPLES:
    'A dead battery I can fix. A dead radio station calling my name is new.'
    'If this place is abandoned, then who keeps answering the phone?'
    'Don't tell me to relax while the room numbers keep changing.'
    'I work with wires, switches, and signals. If this thing can talk, it can be answered.'
    'We're getting out before sunrise, even if I have to pull this motel apart one circuit at a time.'

  UUID: a3e929b5-3f88-4e9b-b289-3b39b57bc277


NON-PLAYER CHARACTERS:

  NPC: June Mercer

    VISUAL: Bust portrait of a young white woman around 20, bleached blonde hair with dark roots, thrift-store jacket over a band tee, camera strap around her neck, smudged eyeliner, scared but defiant expression, 1982 desert punk style, harsh motel neon and moonlight, visual novel horror portrait

    DIALOGUE EXAMPLES:
      'I stopped for pictures before sunset. Then the road stopped making sense.'
      'Don't open any door that's already unlocked. I'm serious.'
      'The motel likes people who look lost. You look very lost.'
      'If you hear an ice machine, run. There isn't one.'

    UUID: f0e64695-7782-42e0-9d44-a7586752ee1d

  NPC: Deputy Tom Baca

    VISUAL: Bust portrait of a Hispanic man in his early 40s, rural sheriff's deputy uniform from 1982, thick mustache, weathered face, flashlight and hat in hand, stern posture hiding deep unease, dusty New Mexico lawman aesthetic, dim patrol-car light and motel neon glow, visual novel style

    DIALOGUE EXAMPLES:
      'Folks around here know better than to stop at Lost Mesa after dark.'
      'I've seen coyotes strip a car to bones. This place scares me more.'
      'Stay where I can see you. If the lights come on by themselves, we leave.'
      'In this county, the desert keeps what it wants.'

    UUID: dba0ae9f-5de9-469d-8d9c-804de340d580

  NPC: Dolores Varela

    VISUAL: Bust portrait of an elderly Latina woman in her late 60s, deeply lined face, gray braid, worn cardigan, rosary wrapped around one hand, old flashlight in the other, solemn and haunted expression, desert wind and motel dust, candlelike warm rim light against cold night shadows, visual novel horror portrait

    DIALOGUE EXAMPLES:
      'It was a decent place once, before the water went bad and the prayers stopped working.'
      'Names matter in that office. Don't give the building yours.'
      'I buried the ledger years ago. I should have burned it.'
      'The dead don't haunt this motel, mija. Something else taught them how.'

    UUID: 955507a9-601f-48fa-909d-154de2de5a63

  NPC: Virgil Bell

    VISUAL: Bust portrait of a gaunt middle-aged man in a faded motel clerk blazer, combed hair, hollow eyes, cigarette-stained fingers, polite smile that feels wrong, caught between 1950s hospitality and ghostly decay, flickering fluorescent office light, eerie visual novel portrait

    DIALOGUE EXAMPLES:
      'Welcome to the Lost Mesa Motor Lodge. Vacancy has a way of finding people.'
      'You needn't trouble yourself with signing in. I've already prepared your key.'
      'We never had a Room 7 until the night it asked for one.'
      'If the radio asks for a name, please give it mine.'

    UUID: 7cde0937-9599-4023-be55-c15a836222b9

  NPC: The Mother Road Voice

    VISUAL: Surreal dialogue portrait of a human face half-formed from radio static, motel neon, and black water reflections, features shifting and indistinct, no clear age or gender, analog distortion, CRT scanlines, threatening calm expression, supernatural desert horror aesthetic

    DIALOGUE EXAMPLES:
      'Driver, you have reached your final vacancy.'
      'Please sign clearly. We dislike errors in the register.'
      'Morning has been delayed for your convenience.'
      'Every guest returns. Some simply take the long road.'

    UUID: ea2a30ce-0037-4e78-9edc-570d3b54b380


LOCATIONS:

  Highway Pullout at Lost Mesa:

    VISUAL: 1982 rural New Mexico desert highway at dusk, empty two-lane road, faded turquoise roadside sign for LOST MESA MOTOR LODGE, dusty station wagon with hood up, telephone poles, red mesas on the horizon, gathering storm clouds, lonely roadside horror atmosphere, cinematic background art

    UUID: 06f305cb-1ddc-4711-b267-340c4bac597f

  Motel Lobby and Office:

    VISUAL: Abandoned roadside motel office in 1982, dusty wood paneling, cracked vinyl chairs, front desk with brass bell, key cubbies, rotary phone, analog tabletop radio, faded tourist brochures, dead neon glow and flickering fluorescent light, eerie analog horror background

    UUID: e5afbf45-d4d0-47cf-b354-dd8f1781cf9d

  Exterior Walkway and Room 7:

    VISUAL: Nighttime exterior of a decaying desert motel, cracked stucco walls, long shadowy walkway, mismatched room numbers, an ominous Room 7 door where it should not fit, flickering red VACANCY sign, windblown dust, deep pools of darkness, supernatural horror background

    UUID: 471f21d5-1f21-419e-af27-793ba40bde2a

  Drained Pool Courtyard:

    VISUAL: Desert motel courtyard under pale moonlight, empty cracked swimming pool full of weeds and blown sand, rusted lounge chairs, dry palm tree, broken chain-link fence, open New Mexico sky, eerie stillness and drifting debris, cinematic horror background

    UUID: f4348bb0-923a-49e8-a982-188341042800

  Pump House and Black-Water Cistern:

    VISUAL: Subterranean motel pump house beneath the desert, concrete stairs, rusted pipes, dangling bare bulbs, jury-rigged radio transmitter equipment, black water cistern reflecting weak light, cramped oppressive shadows, analog supernatural horror background

    UUID: 5403788c-b106-462a-8d51-7416173b4f62


INTRO:

  LOCATION: Highway Pullout at Lost Mesa

  NON-PLAYER  CHARACTERS:
    June Mercer,
    The Mother Road Voice,

  SCENE SYNOPSIS: Rosa's station wagon dies on a deserted highway after her dashboard radio crackles to life on an unused frequency and guides her toward the abandoned Lost Mesa Motor Lodge. At the roadside sign she meets June Mercer, a frightened young photographer who claims she has already tried to leave several times and somehow keeps returning to the same pullout. The intro establishes the 1982 desert setting, Rosa's practical need for a phone or help, and the first impossible hint that the motel is calling stranded travelers by name.


ACT I:

  SCENE 1, LOCATION Motel Lobby and Office

  NON-PLAYER CHARACTERS:
    June Mercer,
    Dolores Varela,
    Virgil Bell,

  SCENE SYNOPSIS: Searching for a phone, Rosa and June enter the motel office and find it shifting between dust-choked ruin and a fully lit version of itself from decades earlier. Virgil Bell, the courteous night clerk, behaves as though the motel is open and tries to coax Rosa into signing the guest ledger, while Dolores Varela appears outside and urgently warns her not to write her name anywhere. The scene introduces the motel's rules, its unsettling hospitality, and the idea that accepting shelter here may be more dangerous than the desert outside.

  SCENE 2, LOCATION Exterior Walkway and Room 7

  NON-PLAYER CHARACTERS:
    June Mercer,
    Deputy Tom Baca,
    The Mother Road Voice,

  SCENE SYNOPSIS: Deputy Tom Baca arrives after spotting Rosa's stranded car, but every attempt to drive the women away bends the road back to the same cracked motel walkway. Room numbers shift when nobody is looking, and the impossible Room 7 appears under the flickering VACANCY sign as radios in the nearby rooms begin broadcasting the Mother Road Voice. The act closes with the cast realizing they are trapped on motel grounds until they understand what is holding them there.


ACT II:

  SCENE 1, LOCATION Drained Pool Courtyard

  NON-PLAYER CHARACTERS:
    June Mercer,
    Dolores Varela,
    Virgil Bell,

  SCENE SYNOPSIS: In the moonlit courtyard, Dolores admits she once worked at Lost Mesa and explains that after a deadly flood and a string of vanished motorists, the motel began changing at night. June shows Rosa her Polaroids, each one revealing extra figures around the drained pool and one image that seems to include Rosa before she ever arrived. Virgil appears at the poolside in a moment of cracked lucidity, suggesting that something beneath the motel learned how to speak through radios, intercoms, and guest records.

  SCENE 2, LOCATION Exterior Walkway and Room 7

  NON-PLAYER CHARACTERS:
    Deputy Tom Baca,
    Virgil Bell,
    The Mother Road Voice,

  SCENE SYNOPSIS: Rosa investigates Room 7 and discovers a space that is larger inside than the building allows, filled with suitcases and keepsakes belonging to missing travelers from many different years. Virgil confesses that he kept checking people in under orders from the Voice, which promises the night will end if a new clerk agrees to take his place. When Deputy Baca tries to burn the ledger and break the pattern by force, the hallway warps and drags him toward the pump house while the Mother Road Voice calmly announces that the motel is preparing a permanent reservation.


ACT III:

  SCENE 1, LOCATION Pump House and Black-Water Cistern

  NON-PLAYER CHARACTERS:
    June Mercer,
    Deputy Tom Baca,
    Dolores Varela,
    The Mother Road Voice,

  SCENE SYNOPSIS: Guided by Dolores, Rosa and June descend into the pump house and discover an old emergency radio relay wired into a black-water cistern beneath the motel. Deputy Baca is found alive but injured, and Dolores reveals that the motel's owner once used the transmitter to lure stranded motorists before something in the water began answering back and taking control of the place. Rosa realizes her knowledge of radios gives her a chance either to overload the system or retune it long enough to free the trapped voices tied to the ledger.

  SCENE 2, LOCATION Motel Lobby and Office

  NON-PLAYER CHARACTERS:
    June Mercer,
    Deputy Tom Baca,
    Dolores Varela,
    Virgil Bell,
    The Mother Road Voice,

  SCENE SYNOPSIS: As the motel fully reanimates around them with blazing lights, phantom guests, and doors slamming in sequence, Rosa uses the office intercom and the retuned transmitter to call every stolen name back out of the building. Virgil rebels against the Voice long enough for Rosa to destroy the guest ledger and sever Room 7 from the rest of the motel, while Dolores stays behind to shut the office and hold the entity in place. The climax forces the cast to choose survival over certainty as the illusion of hospitality collapses into darkness and rushing black water.


OUTRO:

  LOCATION: Highway Pullout at Lost Mesa

  NON-PLAYER  CHARACTERS:
    June Mercer,
    Deputy Tom Baca,

  SCENE SYNOPSIS: At dawn, Rosa, June, and Deputy Baca reach the highway and find the Lost Mesa Motor Lodge reduced to old concrete slabs and a fallen sign, as if it has been abandoned for decades. June's photographs develop almost completely blank except for one frame showing the office light still burning, and Rosa's repaired radio whispers the word vacancy one last time before going silent. The story ends with the survivors driving toward town unsure whether Dolores and Virgil were finally laid to rest, leaving relief and lingering dread in equal measure.