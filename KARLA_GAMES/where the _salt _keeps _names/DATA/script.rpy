
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


# ==== BEAT: intro_beat_01_false_name_arrival ====

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform with fade

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "Dreg's Landing greeted him with tar, rot, and the old midnight rhythm of cargo changing hands where the law got sleepy. It should have felt like cover. It felt like memory with its teeth in."

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Borrowed name, borrowed walk. Keep moving."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    "How does Brego try to pass through the wharf unnoticed?"
    menu:
        "Lean on a practiced dockside lie.":
            jump intro_beat_01_choice_01_dockside_lie
        "Keep to the shadows and side routes.":
            jump intro_beat_01_choice_01_shadow_routes
        "Move in plain sight with the cargo flow.":
            jump intro_beat_01_choice_01_walk_with_flow
label intro_beat_01_choice_01_rejoin:
    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform

# ==== BEAT: intro_beat_02_signs_of_the_net ====

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "Then the harbor answered back. A shortcut stood newly barred. A lantern signal changed the moment he changed direction. Somewhere ahead, his borrowed name was repeated with a little too much polish."

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Too neat. Someone's laying boards under my feet."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    "Which route does Brego test to break surveillance?"
    menu:
        "Try the old warehouse cut-through.":
            jump intro_beat_02_choice_01_warehouse_cutthrough
        "Climb to the rope-and-crane path.":
            jump intro_beat_02_choice_01_rope_and_crane_path
        "Push through the busiest dock lane.":
            jump intro_beat_02_choice_01_crowded_dock_lane
label intro_beat_02_choice_01_rejoin:
    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform

# ==== BEAT: intro_beat_03_seris_steps_out ====

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "The maze narrowed into a pocket between hanging nets and tar-slick pilings. Before he could settle on knife, bluff, or flight, someone stepped into the lane and made choice feel childish."

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "Keep your hand off the knife, Brego. The borrowed name carried you farther than it should have."

    "Seris Vale" "If I wanted a chase, I'd have left you more room."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I liked you better as a rumor."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "Rumor would have waited in the wrong lane. I preferred certainty."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "No shout went up. No steel flashed. Being cornered into conversation felt worse than being chased."

# ==== BEAT: intro_beat_04_the_warning ====

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "I'm not here to spill you into the tide."

    "Seris Vale" "Vey Marrow wants you alive, intact, and delivered for an accounting."

    "Seris Vale" "You should be more afraid of that than of a blade."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    "How does Brego answer Seris's warning?"
    menu:
        "Bluff ignorance.":
            jump intro_beat_04_choice_01_bluff_ignorance
        "Needle Seris about the bounty.":
            jump intro_beat_04_choice_01_needle_the_bounty
        "Ask directly what Marrow wants.":
            jump intro_beat_04_choice_01_ask_about_marrow
label intro_beat_04_choice_01_rejoin:
    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform

# ==== BEAT: intro_beat_05_no_safe_harbor ====

    "Seris Vale" "You saw the closed cut-through. The lantern signal. The laborer who said your borrowed name too cleanly."

    "Seris Vale" "Watchers on the lanes. Harbor records turned. Exits narrowed without anyone raising a voice. Marrow prefers work that looks like weather."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "So the alias lived exactly as long as she allowed it."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "There is no local hole left for you to crawl into."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "No old runner surfaced with a favor. No side door opened. Dreg's Landing stopped feeling like cover and became a net already drawn."

# ==== BEAT: intro_beat_06_forced_toward_old_names ====

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "Go, Brego."

    "Seris Vale" "If anyone on this coast still answers your real name, it will be the people you left behind."

    "Seris Vale" "I am giving you a courtesy. Do not mistake it for safety."

    hide 630fe0d3-d9bd-44d2-afee-765ee8e3bf61

    "How does Brego frame his next move after Seris lets him go?"
    menu:
        "Accept the warning and head for the old crew immediately.":
            jump intro_beat_06_choice_01_take_warning_at_face_value
        "Assume Seris is manipulating him, but choose the old crew anyway.":
            jump intro_beat_06_choice_01_assume_manipulation_but_go
        "Tell himself he's only borrowing old ties and seek Nessa's help.":
            jump intro_beat_06_choice_01_borrow_old_ties_seek_nessa
label intro_beat_06_choice_01_rejoin:
    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform

# ==== BEAT: act1_scene1_beat_01 ====

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform with fade

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "The Eel and Lantern sways with dockside noise, lamp smoke, and the stink of brine worked into old wood."

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "Brego has nearly found a shadow to vanish into when he spots Nessa Quill under a torn green curtain. Her eyes are already on him."

    "How does Brego open when Nessa notices him?"
    menu:
        "Lead with an apology.":
            jump act1_scene1_beat_01_choice_01_apologize
        "Lead with a sardonic quip.":
            jump act1_scene1_beat_01_choice_01_quip
        "Lead with blunt business.":
            jump act1_scene1_beat_01_choice_01_business
label act1_scene1_beat_01_choice_01_rejoin:
    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform

# ==== BEAT: act1_scene1_beat_02 ====

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "Behind the curtain, the tavern becomes muffled enough for old wounds to speak plainly."

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Three years without a word. Then you stroll in like the tide misplaced you."

    "Nessa Quill" "Do you know how many versions of your death I heard? I had favorites."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Sorry to disappoint the better storytellers."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Don't joke at the part where I'm relieved you're breathing."

    "Nessa Quill" "I spent too long teaching myself not to look for you in doorways."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I didn't come here for forgiveness."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Good. What you left behind doesn't fit in that word anyway."

    "Nessa Quill" "Start with why we were the ones left holding the wreck."

# ==== BEAT: act1_scene1_beat_03 ====

    "Nessa Quill" "After the job broke, Marrow's people swept every berth, locker, and debt marker we had."

    "Nessa Quill" "You were gone. The rest of us got to be what her anger landed on."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    "How much does Brego tell Nessa about Seris and Marrow's current interest in him?"
    menu:
        "Tell her everything Seris warned you about.":
            jump act1_scene1_beat_03_choice_01_full_honesty
        "Give her the danger, but not every name and detail.":
            jump act1_scene1_beat_03_choice_01_partial_truth
        "Keep it vague and refuse to show the worst of it.":
            jump act1_scene1_beat_03_choice_01_deflect
label act1_scene1_beat_03_choice_01_rejoin:
    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform

    "Nessa Quill" "So that's it. Not nostalgia. Pressure."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "For the first time since he sat down, she looks at him less like a ghost and more like a man being driven."

# ==== BEAT: act1_scene1_beat_04 ====

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Then hear the rumor that's been walking ahead of you."

    "Nessa Quill" "Marrow thinks you came out of that wreck with her missing ledger under your coat."

    "Nessa Quill" "Not cargo tallies. Names. Routes. Debts. Enough ink to sink half the coast."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I never touched any ledger."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Doesn't matter. She thinks you did, or wants the ports to think she thinks it."

    "Nessa Quill" "Either way, anyone who hides you paints a mark on their door."

# ==== BEAT: act1_scene1_beat_05 ====

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "At Red Hook, the strongbox never even reached my hands. I was covering the stairs when the shouting started."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "And I was told you bolted from the counting room with something wrapped in oilskin."

    "Nessa Quill" "That isn't panic talking. That's somebody placing you exactly where Marrow would hate you most."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Someone wanted me to wear the theft."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Someone wanted the crew broken, scattered, and too busy bleeding to compare stories."

    "Nessa Quill" "We weren't just unlucky, Brego. We were sold from the inside."

# ==== BEAT: act1_scene1_beat_06 ====

    "Nessa Quill" "Here's what I am willing to do."

    "Nessa Quill" "I can put you under a roof tonight, keep your face out of the harbor lamps, and point you toward what Orun may still know."

    "Nessa Quill" "Price is simple. You help me find who sold us out, or you go face Marrow's coast alone."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    "Does Brego accept Nessa's terms, push back against them, or demand a little more before following her?"
    menu:
        "Accept her terms outright.":
            jump act1_scene1_beat_06_choice_01_accept
        "Push back and preserve some pride.":
            jump act1_scene1_beat_06_choice_01_push_back
        "Ask for a little more before agreeing.":
            jump act1_scene1_beat_06_choice_01_ask_more
label act1_scene1_beat_06_choice_01_rejoin:
    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform


return

#==== Choice Option Branches ====

label intro_beat_01_choice_01_dockside_lie:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He slipped beside a knot of haulers and let a bored complaint about spoiled rope and late tallies do the work. A familiar lie bought him a few nods and a few steps of borrowed belonging."

    jump intro_beat_01_choice_01_rejoin



label intro_beat_01_choice_01_shadow_routes:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He took the slick side ladders, net-stacks, and service gaps, favoring darkness over speed. He stayed hard to mark, but every turn felt thinner than it used to."

    jump intro_beat_01_choice_01_rejoin



label intro_beat_01_choice_01_walk_with_flow:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He matched the push of carts and shoulders, carrying himself like a man who had every right to be there. For a stretch, the borrowed name held because no one bothered to test it."

    jump intro_beat_01_choice_01_rejoin



label intro_beat_02_choice_01_warehouse_cutthrough:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He cut for a narrow seam between warehouses he had once used when jobs turned bloody. Fresh timber and an idle hook-cart sealed it off. Somebody had planned for haste."

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_rope_and_crane_path:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He went up instead, along damp braces and rope walk. From the higher dark he spotted a still figure posted exactly where a smuggler would look for the clever exit."

    jump intro_beat_02_choice_01_rejoin



label intro_beat_02_choice_01_crowded_dock_lane:

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He dropped into a louder lane, hoping bodies would blur him. A cask split at exactly the wrong moment, traffic stalled, and too many eyes found him through the confusion. Marked."

    jump intro_beat_02_choice_01_rejoin



label intro_beat_04_choice_01_bluff_ignorance:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Then she's confused. I don't carry anything of hers."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "Fury is brief. Patience is expensive. She paid for the slower thing."

    jump intro_beat_04_choice_01_rejoin



label intro_beat_04_choice_01_needle_the_bounty:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Must be a rich hunt if the corpse isn't good enough."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "This is not about vengeance. Dead men close doors. Living men can be opened."

    jump intro_beat_04_choice_01_rejoin



label intro_beat_04_choice_01_ask_about_marrow:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Then say it plain. What does she think I still have?"

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 630fe0d3-d9bd-44d2-afee-765ee8e3bf61 at screen_right with moveinright

    "Seris Vale" "Routes. Names. The shape of old debts. Enough that being taken alive would be the worse outcome."

    jump intro_beat_04_choice_01_rejoin



label intro_beat_06_choice_01_take_warning_at_face_value:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Courtesy. That's a grim word for it. Fine. I stop pretending the coast forgot me."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He turned from the wharf already measuring the road to the crew he had tried not to face."

    jump intro_beat_06_choice_01_rejoin



label intro_beat_06_choice_01_assume_manipulation_but_go:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "You're steering me. Fine. Doesn't change the math if every other door is nailed shut."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "Warning or design, the road bent the same way: back toward the names he had left behind."

    jump intro_beat_06_choice_01_rejoin



label intro_beat_06_choice_01_borrow_old_ties_seek_nessa:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I'm not going back for comfort. I'm borrowing one old tie and hoping Nessa still opens doors."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    scene bg 9c797922-f35e-476a-b08e-220d314571e7 at bg_xform
    "He left the docks with one ugly hope: that the only people who might still answer his name had not decided to bury it."

    jump intro_beat_06_choice_01_rejoin



label act1_scene1_beat_01_choice_01_apologize:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Nessa. I know sorry is late, but it's what I have."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Late, cheap, and still better than pretending you meant to stay dead. Sit. Quietly."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "She jerks her chin toward the curtained alcove and waits for him to obey."

    jump act1_scene1_beat_01_choice_01_rejoin



label act1_scene1_beat_01_choice_01_quip:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "If I'd known this town still remembered my face, I'd have worn someone else's and brought flowers."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "You should've brought a priest. Sit down before the room notices I'm deciding whether to break a bottle on you."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "Her crooked grin never quite arrives, but she makes space in the alcove."

    jump act1_scene1_beat_01_choice_01_rejoin



label act1_scene1_beat_01_choice_01_business:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I need a corner, five minutes, and your voice lower than your temper."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "You walk in after three years asking favors like table scraps. Fine. Corner first. Then you explain your terrible judgment."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "She pulls the curtain back with two ink-stained fingers."

    jump act1_scene1_beat_01_choice_01_rejoin



label act1_scene1_beat_03_choice_01_full_honesty:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Seris Vale found me in Dreg's Landing and didn't take the bounty."

    "Brego" "She said Marrow wants me alive. Not for revenge. For something worse."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "You told me the whole ugly thing. That's new."

    "Nessa Quill" "And if Seris let you walk, the water is deeper than I thought."

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_03_choice_01_partial_truth:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Marrow's hunters are close, and one of them made it plain Brackwater won't stay blind for long."

    "Brego" "I came because I ran out of safe doors."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "That's a neat slice of truth. Too neat."

    "Nessa Quill" "If you're trimming names and reasons, I'm hearing the scissors."

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_03_choice_01_deflect:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Marrow's interested. That's all you need. The rest is weather."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "No. The rest is the storm walking in wearing your coat."

    "Nessa Quill" "If you still ration truth like contraband, don't ask me to stake my neck on your measurements."

    jump act1_scene1_beat_03_choice_01_rejoin



label act1_scene1_beat_06_choice_01_accept:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "All right. Your terms."

    "Brego" "I'm tired of running blind."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Good. Don't ruin the miracle by sounding grateful."

    "Nessa Quill" "Count ten, then follow. We leave separately."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "It is not forgiveness, but it is a door left unbarred."

    jump act1_scene1_beat_06_choice_01_rejoin



label act1_scene1_beat_06_choice_01_push_back:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "I'll help find the rat. I won't crawl because you snapped your fingers."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "I don't need you crawling. I need you useful."

    "Nessa Quill" "My roof, my rules, and you keep one eye open if pride helps you sleep."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "The terms harden, but the offer stands."

    jump act1_scene1_beat_06_choice_01_rejoin



label act1_scene1_beat_06_choice_01_ask_more:

    show fb0fa485-3066-40e0-ba20-a955ab7f4c84 at screen_left with moveinleft

    "Brego" "Before I trail after you, I want one thing more than shelter. I want the first real lead you have."

    hide fb0fa485-3066-40e0-ba20-a955ab7f4c84

    show 736f5435-de0b-48a4-9df6-2b0e51a60012 at screen_right with moveinright

    "Nessa Quill" "Fair."

    "Nessa Quill" "I think Orun kept a piece of the night we lost. Help me reach him, and I open the rest."

    hide 736f5435-de0b-48a4-9df6-2b0e51a60012

    scene bg 6a4fcb2f-52fe-464a-994b-f1a1d36772a7 at bg_xform
    "Trust arrives thin as lamp smoke, but it arrives."

    jump act1_scene1_beat_06_choice_01_rejoin

