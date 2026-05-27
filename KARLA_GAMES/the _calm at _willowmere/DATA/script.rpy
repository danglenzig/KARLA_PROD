
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


# ==== BEAT: intro_beat_01_evening_routine ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform with fade

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "The common room drifted through its nightly routine: local news a notch too loud, a jigsaw on the side table, lamps doing their best against institutional beige."

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Willowmere's idea of variety is switching from weather panic to municipal graft by eight-thirty."

    "Dr. Miriam Vale" "Routine I can forgive. It's the cheerful supervision that offends me."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Ruby sat with her scarf half-unwound, Walter guarded his chair like a foreman finishing shift, Nila kept one finger in a book, and Mara moved at the edges of the room with blankets, reminders, and polite corrections."

# ==== BEAT: intro_beat_02_common_room_banter ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "The news finally wandered from zoning disputes to the night's main attraction: grainy telescope footage and excited captions about a comet due over town."

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "They've pushed this thing back three times. Either the comet can't read a clock, or the station can't."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_left with moveinleft

    "Ruby Alvarez" "If it misses us entirely, the town council will take credit."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_left with moveinleft

    "Nila Banerjee" "They've already used the phrase 'historic event' twice. It usually means nothing happens on schedule."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinleft

    "Dr. Miriam Vale" "Good. I was afraid we'd face celestial spectacle without expert commentary."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    "Whom does Miriam engage most directly as the room's chatter turns to the comet story?"
    menu:
        "Trade barbs with Ruby.":
            jump intro_beat_02_choice_01_ruby
        "Compare notes with Walter on timing and routine.":
            jump intro_beat_02_choice_01_walter
        "Encourage Nila's careful scrutiny.":
            jump intro_beat_02_choice_01_nila
label intro_beat_02_choice_01_rejoin:
    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform

# ==== BEAT: intro_beat_03_mara_on_rounds ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Mara made her evening circuit with a cart of tea, tissues, and reminders, restoring order whenever the room started sounding too much like itself."

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "Blankets, tea, and last-call requests. Let's get everyone comfortable."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinleft

    "Dr. Miriam Vale" "You herd us so gently it almost counts as free will."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "I'd settle for comfortable, Dr. Vale."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_left with moveinleft

    "Ruby Alvarez" "Comfortable's nice. Bourbon would be civic-minded."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "Tea is what passed inspection tonight."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "My chair's fine. It's the television that's crooked."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "Then I'll straighten the world one degree at a time, Mr. Finch."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "It was practiced, mildly patronizing, and familiar enough to pass for care—which, most nights, it probably was."

# ==== BEAT: intro_beat_04_the_comet_segment ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "The broadcast finally gave the comet the full screen."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "A shaky live shot filled the television: dark trees, a small crowd, and a bright digital countdown ticking above them."

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "They've got a countdown clock for a rock. That's optimism."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_left with moveinleft

    "Ruby Alvarez" "Small town gets one celestial event and suddenly everybody needs folding chairs."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_left with moveinleft

    "Nila Banerjee" "They've already called it rare, historic, and family-friendly. Only one of those can be measured."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Let them have their pageant. Even institutions deserve a little sky."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Even Mara paused with a folded blanket over one arm. Around the room, heads lifted from cards, books, and grievances alike."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "The countdown began. For one strange, suspended moment, Willowmere felt connected to a world beyond its windows."

# ==== BEAT: intro_beat_05_too_smooth_after ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "A pale streak crossed the television sky and was gone."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "A few soft sounds rose, then the common room settled into a hush too complete to be ordinary."

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "You're all quite safe. Let's keep the evening calm."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "From the corridor, the same reassurance arrived again, word for word, in the same even cadence."

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinleft

    "Dr. Miriam Vale" "No."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Mara had always been composed. This was different—smoother, emptier, as if calm itself had started speaking through her."

# ==== BEAT: intro_beat_06_miriam_marks_the_difference ====

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Miriam kept her face arranged in polite boredom and watched Mara resume her round with that new, frictionless ease."

    "How does Miriam respond to the staff's sudden, unnatural calm?"
    menu:
        "Ask Mara a dry, pointed question.":
            jump intro_beat_06_choice_01_pointed_question
        "Make a joke and watch how it lands.":
            jump intro_beat_06_choice_01_joke_test
        "Say nothing and study the pattern.":
            jump intro_beat_06_choice_01_silent_observe
label intro_beat_06_choice_01_rejoin:
    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform

# ==== BEAT: act1_scene1_beat_01 ====

    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform with fade

    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform
    "Morning light washes the Cedar Dining Room in harmless beige. Coffee steams, eggs cool on plates, and silverware taps softly against china."

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Nothing says cheerful dawn like synchronized tray delivery."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinright

    "Mara Keene" "Good morning. Breakfast is on time, everyone is comfortable, and everything is in hand."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform
    "A chair is straightened, then another, then another, each correction landing on the same invisible count. The smiles arriving with them look pre-fitted."

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "No. That's not efficiency. Efficiency has rough edges."

# ==== BEAT: act1_scene1_beat_02 ====

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "What line of inquiry does Miriam use to test the breakfast staff?"
    menu:
        "Ask about the comet.":
            jump act1_scene1_beat_02_choice_01_ask_about_comet
        "Ask about schedules, calls, and access.":
            jump act1_scene1_beat_02_choice_01_ask_about_schedule
        "Comment on the staff's strange cheer.":
            jump act1_scene1_beat_02_choice_01_comment_on_cheer
label act1_scene1_beat_02_choice_01_rejoin:
    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform

# ==== BEAT: act1_scene1_beat_03 ====

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform
    "Miriam stops watching Mara and watches the table instead. From elsewhere in the room, the same reassurance drifts past again, word for word."

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "I had a joke about the eggs, but repetition got there first."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "Routine's one thing. This is timing."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinleft

    "Nila Banerjee" "She said 'everything is in hand' yesterday at 8:12. I wrote it down."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Good. Then I am not being eccentric alone."

# ==== BEAT: act1_scene1_beat_04 ====

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "How does Miriam pressure Mara without fully exposing herself?"
    menu:
        "Use dry sarcasm to call out the repeated reassurances.":
            jump act1_scene1_beat_04_choice_01_dry_sarcasm
        "Ask factual questions about timing and routine.":
            jump act1_scene1_beat_04_choice_01_factual_questions
        "Feign confusion and make Mara over-explain.":
            jump act1_scene1_beat_04_choice_01_feign_confusion
label act1_scene1_beat_04_choice_01_rejoin:
    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform

# ==== BEAT: act1_scene1_beat_05 ====

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "How openly does Miriam share her suspicion with Ruby, Walter, and Nila?"
    menu:
        "Speak bluntly about something being wrong.":
            jump act1_scene1_beat_05_choice_01_speak_bluntly
        "Frame it as pattern-checking.":
            jump act1_scene1_beat_05_choice_01_frame_as_pattern_checking
        "Keep it understated and elliptical.":
            jump act1_scene1_beat_05_choice_01_keep_it_understated
label act1_scene1_beat_05_choice_01_rejoin:
    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform

# ==== BEAT: act1_scene1_beat_06 ====

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    scene bg 3d37b634-9158-4f6b-b142-8cd2b4c8daa8 at bg_xform
    "Breakfast thins. For one brief minute, no staff stand close enough to hear the table."

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Let's say it plainly. Since the comet, something is wrong at Willowmere."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "Yes. And that nurse smile is meant to put a lid on us."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "Yes. It's timing, wording, the whole works."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinleft

    "Nila Banerjee" "Yes. I'm frightened, but I'm not mistaken."

    "Nila Banerjee" "Wait with me at the nurse station later. People linger there all the time. We can compare details and look ordinary doing it."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Then later, at the nurse station. Quietly. We wait for pills and mail, and in the meantime we pay attention."


return

#==== Choice Option Branches ====

label intro_beat_02_choice_01_ruby:

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Ms. Alvarez, you sound disappointed. Were you hoping for a better class of apocalypse?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_left with moveinleft

    "Ruby Alvarez" "Honey, if the heavens are going to put on a show, I expect effort."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "At last, a woman with standards."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_walter:

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Still betting on 8:41, Mr. Finch?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "I'm betting on bad broadcasting and a perfectly innocent rock."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "A rigorous distinction. I approve."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_nila:

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Mrs. Banerjee, should we fact-check the universe?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_left with moveinleft

    "Nila Banerjee" "Only the people narrating it. The universe manages without copy editors."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinleft

    "Dr. Miriam Vale" "A loss to every newsroom."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    jump intro_beat_02_choice_01_rejoin



label intro_beat_06_choice_01_pointed_question:

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "Tell me, Mara, did the comet improve the service, or are you all suddenly auditioning for sainthood?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "There's nothing to worry about, Dr. Vale. Everyone is settled, and everything is as it should be."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "The answer was immaculate and hollow, like a sentence copied rather than spoken."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Miriam tucked the certainty away and decided to keep watch."

    jump intro_beat_06_choice_01_rejoin



label intro_beat_06_choice_01_joke_test:

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_center with moveinright

    "Dr. Miriam Vale" "If this serenity spreads to the kitchen, I'll know we're under supernatural assault."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_right with moveinright

    "Mara Keene" "There's no need for upset. Everything is peaceful tonight."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "No smile. No puzzled delay. Just the same polished reassurance, dropped into place without a seam."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "That absence of ordinary timing told Miriam more than an argument would have."

    jump intro_beat_06_choice_01_rejoin



label intro_beat_06_choice_01_silent_observe:

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Miriam said nothing."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "Mara adjusted a blanket, turned a cup exactly a quarter turn, and moved on. A moment later, from the hall, the same soft phrase came again in the same rhythm."

    scene bg f3d398db-f927-46aa-b1eb-5c20f3c8aec8 at bg_xform
    "She lowered her eyes before anyone could notice she had stopped treating any of it as normal."

    jump intro_beat_06_choice_01_rejoin



label act1_scene1_beat_02_choice_01_ask_about_comet:

    "Dr. Miriam Vale" "Did the comet trouble anyone else, or are we pretending the sky didn't perform last night?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinleft

    "Mara Keene" "There's nothing to worry about, Dr. Vale. Everyone is safe, and everything is proceeding normally. I'll check back with you shortly."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Mm. A human answer would have been messier."

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_02_choice_01_ask_about_schedule:

    "Dr. Miriam Vale" "Who revised today's schedule, and why is every phone suddenly on a pilgrimage?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinleft

    "Mara Keene" "Your calls and daily arrangements are already being handled. There's no need to concern yourself with logistics this morning. I'll check back with you shortly."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Handled is not a synonym for explained."

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_02_choice_01_comment_on_cheer:

    "Dr. Miriam Vale" "You all seem remarkably delighted for people serving powdered eggs."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinright

    "Mara Keene" "We're simply keeping things pleasant. Let's not disturb breakfast with upsetting ideas. I'll check back with you shortly."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Polish before particulars. Noted."

    jump act1_scene1_beat_02_choice_01_rejoin



label act1_scene1_beat_04_choice_01_dry_sarcasm:

    "Dr. Miriam Vale" "Mara, do those reassurances come printed on cards, or do you memorize them in batches?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinright

    "Mara Keene" "I know change can feel distressing, Dr. Vale. I'll make sure someone checks on you, but let's keep the table calm and pleasant for everyone."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "Management smile. Knew it."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Thank you, Ruby. Peer review helps."

    jump act1_scene1_beat_04_choice_01_rejoin



label act1_scene1_beat_04_choice_01_factual_questions:

    "Dr. Miriam Vale" "Then help me with a fact. Why did breakfast arrive early, and why were those chairs straightened in sequence?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinleft

    "Mara Keene" "Everything is exactly on schedule. There's no need to monitor the routine so closely, but I'll note your concern."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "That's not routine. That's timing."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Mr. Finch continues to save us from imprecise nouns."

    jump act1_scene1_beat_04_choice_01_rejoin



label act1_scene1_beat_04_choice_01_feign_confusion:

    "Dr. Miriam Vale" "Forgive me, Mara. When you say 'everything is in hand,' whose hand is holding what, precisely?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 305fbefb-e004-42cc-b1da-d8f01d0302eb at screen_center with moveinright

    "Mara Keene" "Your meals, medication, and daily schedule are all in hand. Everything is in hand. You don't need to trouble yourself with the details."

    hide 305fbefb-e004-42cc-b1da-d8f01d0302eb

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinleft

    "Nila Banerjee" "Same phrase. Same cadence."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Lovely. Even the footnotes repeat."

    jump act1_scene1_beat_04_choice_01_rejoin



label act1_scene1_beat_05_choice_01_speak_bluntly:

    "Dr. Miriam Vale" "Something is wrong here. Since the comet, every smile in this place has teeth."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "All right, professor. Now you're talking straight."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "You're not the only one hearing it."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinright

    "Nila Banerjee" "Nor the only one writing it down."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Good. Then we may dispense with polite denial."

    jump act1_scene1_beat_05_choice_01_rejoin



label act1_scene1_beat_05_choice_01_frame_as_pattern_checking:

    "Dr. Miriam Vale" "Let's keep adjectives out of it for one minute. What have you each noticed, exactly?"

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "Serving rhythm. Too exact."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinleft

    "Nila Banerjee" "Repeated sentences. Exact repeats."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "And that smile means shut up and cooperate."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Excellent. Three symptoms, one illness."

    jump act1_scene1_beat_05_choice_01_rejoin



label act1_scene1_beat_05_choice_01_keep_it_understated:

    "Dr. Miriam Vale" "If anyone else thinks breakfast has acquired a second script, now would be the elegant time to blink."

    hide 32164687-7d8d-45b2-b5d8-217846ab434b

    show ab2ac8cb-7b89-411a-9a91-091ce58474eb at screen_right with moveinright

    "Ruby Alvarez" "I'm blinking, honey."

    hide ab2ac8cb-7b89-411a-9a91-091ce58474eb

    show 5980d332-bfc3-4816-bb92-f97e05149da2 at screen_right with moveinright

    "Walter Finch" "I've heard the knock in the engine."

    hide 5980d332-bfc3-4816-bb92-f97e05149da2

    show c51ddbc2-0eec-418e-8d1a-152311eb2bdd at screen_center with moveinleft

    "Nila Banerjee" "I have notes in my pocket."

    hide c51ddbc2-0eec-418e-8d1a-152311eb2bdd

    show 32164687-7d8d-45b2-b5d8-217846ab434b at screen_left with moveinleft

    "Dr. Miriam Vale" "Subtlety may yet save us."

    jump act1_scene1_beat_05_choice_01_rejoin

