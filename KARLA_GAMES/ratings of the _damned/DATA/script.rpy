
transform screen_right:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720 ("show" keyword needs you to set scale on both x and y)
    xoffset 640

transform screen_left:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720
    xoffset 0

transform screen_center:
    xzoom 0.703125
    yzoom 0.703125
    # ^^ 1024 -> 720
    xoffset 320

transform bg_xform:
    xzoom 1.25
    # ^^ 1024 -> 1280 ("scene" keyword applies scale to both x and y)

label start:


# ==== BEAT: intro_beat_01_opening_monologue ====

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform with fade

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Purple gels wash over a cardboard graveyard that should look ridiculous and somehow doesn't. The ON AIR light glows red."

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Good evening, my little degenerates. Madame Massacre welcomes you back to the only crypt in Pennsylvania with decent lighting."

    "Dahlia Graves / Madame Massacre" "Tonight's feature is cheap, nasty, and held together with inferior stitching. In other words, a local classic."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_right with moveinright

    "Chip Mercer" "Sports is over, folks. Try not to commit any felonies athletically. Madame, the morgue is yours."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Thank you, Chip. Go ice down that jawline before it pulls a muscle."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Chip backs off with an amused grin. Off camera, the crew's laughter lands a shade too sharp to feel friendly."

# ==== BEAT: intro_beat_02_lenora_drops_the_news ====

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Commercial music rolls. Lenora glides onto the set with Roxie in tow while Chip lingers by the camera rail to watch the bloodletting."

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_left with moveinleft

    "Lenora Pike" "Quick programming note, Dahlia. We're launching a new midnight block. Younger demo, brighter pace, fewer complaints from men who sell mattresses."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Neon, noise, bad choices. You know. Public service."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_left with moveinleft

    "Lenora Pike" "Roxie fronts it. This is modernization, not replacement. Let's all be adults and pretend the distinction matters."

    "How does Dahlia answer Lenora's 'modernization' pitch?"
    menu:
        "Cut back with open sarcasm.":
            jump intro_beat_02_choice_01_sarcastic
        "Answer coolly and make it sound like business.":
            jump intro_beat_02_choice_01_strategic
        "Laugh it off and give nothing away.":
            jump intro_beat_02_choice_01_laugh_off
label intro_beat_02_choice_01_rejoin:
    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform

# ==== BEAT: intro_beat_03_chip_and_roxie_press_in ====

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_right with moveinright

    "Chip Mercer" "You okay? Because that smile says 'fine,' but the nails say 'vehicular homicide.'"

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "I'm touched you noticed. Keep looking at me like that and I'll start charging cross-promotion rates."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Don't blame me, Madame. I just showed up with better synth music."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "And such compassion. Neon really is the future."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_right with moveinright

    "Chip Mercer" "If this is the new late-night lineup, I'm suddenly very interested in management."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Careful, Mercer. She looks like she bites when cornered."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Only when bored, sweetheart."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

# ==== BEAT: intro_beat_04_bagman_as_bit ====

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "The red tally light flashes back on. Dahlia turns for camera with her pulse hidden under satin."

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Welcome back, my little grave robbers. While others chase trends, I remain devoted to quality corruption."

    "Dahlia Graves / Madame Massacre" "So let's zhuzh up a hometown legend. The Bagman of Briar Creek: Marlowe's own shambling pile of mud, trash, and municipal guilt."

    "Dahlia Graves / Madame Massacre" "If he lumbers in tonight, tell him to wipe his feet. I only allow one messy man on this set at a time."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

# ==== BEAT: intro_beat_05_the_warning_call ====

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Oh, look. The phone line lives. Let's see which insomniac I've corrupted tonight."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "An older woman's voice crackles over the line, breathless and deadly serious. 'Don't you joke about Briar Creek on television. Some things listen better when a whole town is watching.'"

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_left with moveinleft

    "Lenora Pike" "Keep it tight, Dahlia."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    "How does Dahlia handle the disturbing live warning?"
    menu:
        "Mock the caller and keep the show buoyant.":
            jump intro_beat_05_choice_01_mock
        "Humor the caller and ask what she means.":
            jump intro_beat_05_choice_01_probe
        "Cut the call short with polished reassurance.":
            jump intro_beat_05_choice_01_cut_short
label intro_beat_05_choice_01_rejoin:
    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform

# ==== BEAT: intro_beat_06_static_aftertaste ====

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Before anyone can recover, every studio monitor erupts into hard white static. The lights flutter. The movie soundtrack warps into a wet mechanical howl."

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_right with moveinright

    "Chip Mercer" "That better be a fuse and not an omen."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Okay. Cute bit. Which one of you psychos approved this?"

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_left with moveinleft

    "Lenora Pike" "No panic. Stay live."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Marlowe, a brief disturbance from the underworld. We return you now to our regularly scheduled indecency."

    "Dahlia Graves / Madame Massacre" "Do try not to feed the static."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "The broadcast limps onward on sheer nerve. Dahlia never breaks for the audience, but once the lights steady she knows the warning hit something real. Roxie's rise is one threat. Briar Creek may be another entirely."

# ==== BEAT: act1_scene1_beat_01_newsroom_fallout ====

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform with fade

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "The newsroom hums like a bad transformer. Phones ring, ad reps bark through headsets, and everyone in the building has an opinion about last night's static."

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "Everybody quit saying 'haunted' where sponsors can hear it. One Bagman call, one static burp, and frozen pizza thinks we're hexed."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Hexed tests great with eighteen-to-thirty-fours."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Marvelous. The apocalypse has a target demo."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "You look like you got front-row seats, though. You alright?"

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "I am immaculate. Any tremor you detect is expensive."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinright

    "Lenora Pike" "Good. Because sponsors are rattled, viewers are curious, and curiosity bills better than calm."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "So last night's little seizure is a marketing angle now?"

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "If panic spikes the phones, it's called momentum."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "Lenora crooks one manicured finger toward her office. Whatever happened on air, the station has already decided to sell it."

# ==== BEAT: act1_scene1_beat_02_lenora_sets_the_terms ====

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinright

    "Lenora Pike" "Here's your refresh. Quicker opens. Hotter promos. More Chip. The audience wants velocity, not velvet."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "My velvet built your midnight block."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinright

    "Lenora Pike" "And now it shares shelf space. Roxie needles you, you needle back, Chip keeps the chemistry marketable, and the town picks a queen. Conflict lifts both slots."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    "How does Dahlia respond to Lenora's modernization mandate?"
    menu:
        "Smile thinly and agree—for now.":
            jump act1_scene1_beat_02_choice_01_grudging_agreement
        "Tell Lenora exactly what you think of her manufactured feud.":
            jump act1_scene1_beat_02_choice_01_open_resistance
        "Accept the stunt, but make it clear you're the headliner.":
            jump act1_scene1_beat_02_choice_01_diva_spin
label act1_scene1_beat_02_choice_01_rejoin:
    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform

# ==== BEAT: act1_scene1_beat_03_chip_crosspromo_pitch ====

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "Outside Lenora's office, Chip leans on the doorframe like casual concern is part of his hair product budget."

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "Well, partner, Lenora already sold us as the station's hottest mixed double."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "If she puts me beside a touchdown graphic, I'll poison the Xerox."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "Kidding aside, she pitched us to sponsors this morning. And you got that look again. Last night really got under the lacquer, huh?"

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    "How does Dahlia play Chip's offer to help with the crossover?"
    menu:
        "Flirt back and let the concern land.":
            jump act1_scene1_beat_03_choice_01_lean_in
        "Use him as a practical ally inside the station.":
            jump act1_scene1_beat_03_choice_01_keep_it_professional
        "Deflect with sharp humor and keep your distance.":
            jump act1_scene1_beat_03_choice_01_deflect
label act1_scene1_beat_03_choice_01_rejoin:
    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform

# ==== BEAT: act1_scene1_beat_04_roxies_mask_slips ====

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "At the promo corner, neon gels flash while Roxie refilms ten seconds everybody already said they loved."

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "No, faster. If I blink, I want it to look like an event."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Darling, if you sprint any harder, the audience will mistake you for a station break."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Yeah, well, everybody here wants me legendary by Friday."

    "Roxie Static" "Nobody mentions where I'm supposed to fail first. Preferably in private."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    "How does Dahlia respond when Roxie's confidence briefly cracks?"
    menu:
        "Sharpen the feud and push Roxie back behind her swagger.":
            jump act1_scene1_beat_04_choice_01_needle
        "Give cutting but useful advice.":
            jump act1_scene1_beat_04_choice_01_offer_advice
        "Suggest Lenora is playing both of you.":
            jump act1_scene1_beat_04_choice_01_hint_truce
label act1_scene1_beat_04_choice_01_rejoin:
    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform

# ==== BEAT: act1_scene1_beat_05_the_wrong_box ====

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "By noon, the station is fighting over shelf space, sponsor copy, and whether Roxie's neon coffin outranks Dahlia's rubber bats."

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Why is my promo gear in storage with foam gravestones and a fake guillotine?"

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "Because your promo gear turns over ad dollars. The guillotine does not. Move the junk."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "Little late. The junk just exploded."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "A split archive box gives way across the tile. Brittle tapes, old WKLV logs, and city paperwork spill out in a papery avalanche."

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Briar Creek. Dump-road complaints. These aren't punchlines, Lenora."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "They're antiques. Local scare copy from before everyone learned how to package a myth."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "There's crew notation on these. Missing footage. Legal holds. This was real enough for paperwork."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Wait. The creek wasn't just camp? We used to cover it straight?"

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Apparently before Marlowe started flirting with its own rot, somebody here took notes."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "The newsroom noise keeps chattering around them, but the box sits on the floor like something that expected to stay buried."

# ==== BEAT: act1_scene1_beat_06_dahlia_claims_a_clue ====

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinright

    "Lenora Pike" "Enough. Box back in storage. I have sponsors calling, and I will not answer them with mold."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "You say that like mold hasn't carried half this station."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "Leave the archaeology, Dahlia. We sell the present."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "As Lenora jams the folders back into cardboard, one tape log skids loose: BRIAR CREEK / DUMP ROAD / HOLD FOR LEGAL."

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Legal, hm. Nothing says 'harmless local legend' like paperwork in all caps."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg f8808a37-8d4c-4411-93df-cdd5fff7f6fb at bg_xform
    "While Lenora straightens the box, Dahlia slips the log into her glove and glides out smiling like she's won something smaller, and much more dangerous, than an argument."


return

#==== Choice Option Branches ====

label intro_beat_02_choice_01_sarcastic:

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Modernization? Darling, if you plan to embalm me on company time, at least wait until I'm cold."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Chip winces. Roxie's grin sharpens. Lenora gets her first clean taste of open war."

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_strategic:

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Then call it competition and send me the numbers. I don't mind a fight, Lenora. I mind sloppy accounting."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_left with moveinleft

    "Lenora Pike" "Excellent. Fight pretty and keep the sponsors calm."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_laugh_off:

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Please. If Marlowe suddenly wants neon, I'll simply haunt in brighter colors."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "Lenora's smile never slips, but now she has to guess how much blood she drew."

    jump intro_beat_02_choice_01_rejoin



label intro_beat_05_choice_01_mock:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Then your swamp suitor may send me an angry letter in mildew. This is television, darling, not a séance."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "A couple of laughs escape on instinct. Nobody sounds convinced."

    jump intro_beat_05_choice_01_rejoin



label intro_beat_05_choice_01_probe:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "All right, sweetheart. Why not on television?"

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "The woman answers at once. 'Because screens make hungry things bigger.' The set falls dead quiet."

    jump intro_beat_05_choice_01_rejoin



label intro_beat_05_choice_01_cut_short:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Thank you for the concern, Marlowe. We'll keep our swamp suitors at arm's length and our schedule moving."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    scene bg bfa7ab80-28da-49cd-818e-6e0fbb3ce09e at bg_xform
    "The line clicks dead. So does the room's easy mood."

    jump intro_beat_05_choice_01_rejoin



label act1_scene1_beat_02_choice_01_grudging_agreement:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Fine. I'll modernize just enough to make you regret asking."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "Perfect. Compliance with eyeliner. That's all I need."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_02_choice_01_open_resistance:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "If you want two women clawing each other for scraps, buy a zoo. I host a program."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinleft

    "Lenora Pike" "Then start behaving like a brand, not a grievance."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_02_choice_01_diva_spin:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "If you're staging a war, put me on the poster. Nobody buys a ticket for the opening act."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 7487c532-5dfd-436f-8d6a-3be89da2033a at screen_center with moveinright

    "Lenora Pike" "Exactly. I don't care who throws the first punch, only who holds the audience."

    hide 7487c532-5dfd-436f-8d6a-3be89da2033a

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_03_choice_01_lean_in:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Keep talking like that and I might let you escort me into the crossfire."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "Now there's a promo I wouldn't mind shooting."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_03_choice_01_keep_it_professional:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "If you're useful, bring me sponsor names and whatever Lenora promised them."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "Now you're speaking my native language: gossip with a budget."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_03_choice_01_deflect:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "I'm fine. Slightly cursed, heavily moisturized, and booked through the weekend."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show bada5741-2a09-4e6b-a21b-e86ae1aafaec at screen_left with moveinleft

    "Chip Mercer" "You joke like a fire alarm. Loud, stylish, and usually covering something."

    hide bada5741-2a09-4e6b-a21b-e86ae1aafaec

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_04_choice_01_needle:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Then learn fast. Television smells fear before it sees cleavage."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Good. Maybe I'll make mine your problem."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    jump act1_scene1_beat_04_choice_01_rejoin



label act1_scene1_beat_04_choice_01_offer_advice:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinright

    "Dahlia Graves / Madame Massacre" "Hold still for half a beat. Confidence looks cheap when it runs."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "That's annoyingly solid advice."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    jump act1_scene1_beat_04_choice_01_rejoin



label act1_scene1_beat_04_choice_01_hint_truce:

    show e5db3ee8-0876-4de1-9105-93adcfcb8d84 at screen_center with moveinleft

    "Dahlia Graves / Madame Massacre" "Lenora wants blood because blood trends. You and I don't have to make it easy."

    hide e5db3ee8-0876-4de1-9105-93adcfcb8d84

    show 96551d25-a8a0-4bad-9954-82d2471ac762 at screen_right with moveinright

    "Roxie Static" "Careful, Madame. One more sentence like that and I might mistake it for solidarity."

    hide 96551d25-a8a0-4bad-9954-82d2471ac762

    jump act1_scene1_beat_04_choice_01_rejoin

