Cully Hill Boys — Project Brief
Updated 10.08.2026 at 19:36
This is the project brief for THE CULLY HILL BOYS, our feature-length AI film.
Logline: An action-comedy about three underachieving London rappers who, in attempt to make a name for themselves, accidentally get caught in a messy drug war. A fast, funny, beat-driven crime movie about loyalty, friendship, and refusing to stay invisible.
The Cully Hill Boys-Cover_16x9.png
About the project

The film

CAL, HORACE and OLI are three London rappers in their late twenties, going nowhere. They play a killer show to an empty room, get leaned on by the crime boss who owns the venue, and almost break up. Eight pints later Cal has the idea: the ultimate music video, filmed on a hot tub built out of a boat. At the boat shop owned by Horace's uncle they take an old dinghy, drop it down a flight of stairs — and £2M of blood-stained drug money spills out of the hull. Everybody comes for it: the boss's men, a Ukrainian hitman, and the real owner of the money, who takes Cal's daughter as collateral. What follows is one bad day, a gunfight, an exchange that was always going to be an execution, and a train that ends it. Two days later the boys walk out of police custody as national news.
The numbers

Runtime 1 hour 54 minutes. 137 scenes. The premiere was in New York on 5 August 2026. The canvas holds 600 approved assets: 74 cards for the leads and the antagonists, 52 for supporting actors and animals, 90 episodic characters, 159 props and over 200 location plates.
Every frame is generated. The actors are real and signed, but nothing was filmed with them: their likeness lives in the assets, and from that point on only the asset goes into a shot. There are no sets and no camera crews. One exception: a single fight was choreographed by stunt performers and shot on a phone as a motion reference, and that block is further down.
The tools. The entire film was generated in Seedance — every shot, all video and speech. Faces and character sheets: Soul Cinema. Edits, reverse angles and point changes: Seedream and Nano Banana. Prompts: Claude, in two chats — one for image prompts, one for video prompts. We split them because the rules of one job poison the other: the image chat needs flat light and anti-CG wording, the video chat needs field of view in degrees and motivated light.
Still 2026-08-07 163533_1.255.1.jpg
The setting

South-East London, 2011. A council estate, grime on pirate radio, a four-storey club where the losers play the ground floor and the man who owns the borough sits at the top. Autumn, late September: grey-gold light, wet leaves, dark by six.
The year is a rule, not decoration. Nothing in frame is newer than 2011 — no smartphones, no glowing screens in a crowd, no new cars on the street. Left alone, the model drags every shot toward today, so the year goes into every location plate and gets repeated in every prompt. One extra holding a phone and the shot is gone.

The cast

Still 2026-08-07 163533_2.143.1.jpg

The film has signed actors in it. Cal is Matt Kiatipis, the basketball player. Oli is Israel Adesanya, the UFC fighter. Horace is N3on, one of the loudest streamers around. Tobin is Quinton "Rampage" Jackson, the MMA fighter. We digitized their likeness: the character sheets were built from contract photography, so the face on the sheet is the actor's face and not a similar type. After that only the sheet goes into a shot. Likeness and voice rights were closed by contract before the first generation — the platform requires confirmed authorization for assets like these, so the releases go to compliance before the actor ever appears in a frame.
Each character also carries a written manner — written about the character, not about the man who plays him. One paragraph per hero, fixed before the first shot and pasted into every prompt: how he stands, how he talks, what his face does when he loses. Oli's says the fighter's swagger drops the second he is turned down — so in every scene where Oli is refused, the shoulders come down on the same beat. Written once, the manner stops the character from turning into a different person in the next shot.
Accents are written as conditions, never as a label. The boys speak South London street English. Vernon is archaic cockney at a whisper. Tika speaks Indian English. Dmetry, Russian-Ukrainian. Monty, Punjabi English. The accent sits in the voice block of every scene, and where it matters it is spelled out inside the line: th going to f and v, dropped h, glottal t, -ing to -in'. One character, one accent, and it never drifts.

Three skills

A skill is a playbook of rules that Claude loads by itself and then works by. Ours are three, in the order you use them.
LIRA — image prompts. You tell it what you need — this character in this state, this location at this time of day — and it writes the prompt for the sheet or the plate. It holds the weak points of every image model and checks the prompt against them before you send it: the words that summon a photo studio, the light that bakes itself into the sheet, the details a given model always drops.
LIRA SKILL.md
MD


CINEDANCE — video prompts. Three parts inside. The writer builds the whole prompt: it breaks the scene down and sets the blocking, the optics, the physics and the timing. The auditor re-checks every prompt before it goes out — an empty first frame, stale tags, weak geography, two lines that contradict each other. The workbench keeps the prompt as a file and patches only the section that failed, because a fully rewritten prompt loses the parts that already worked.
CINEDANCE HIGGSFIELD SKILL.md
MD


THE ACTING SYSTEM PROMPT — performance. Behavior instead of emotions, the face-and-body hacks, and the master-profile format. Its rules run through this brief; the full version is in the attachments.
ACTING SKILL.md
MD



What we took from the previous film

Four things came straight out of HELL GRIND and stayed. Scene context — every shot opens with what is happening dramatically, who is in it and how long it runs. The first-frame spatial lock — frame one is already occupied, everyone in position, no empty establishing beat. One second of silence after every line — a clean tail inside the clip, so the editor gets a seam and the model has nothing to fill with invented sound. Detailed mimic and acting beats — the face and the body written beat by beat instead of an adjective. The difference is that on the last film we found all of this on the way, and here it was waiting on day one.

The main problem


Consistency is the whole job: keeping every character, place and object the same from shot to shot. A video model has no memory. Describe your hero incompletely, and in the next shot he will have a different appearance, behavior or voice. Add spaces that fall apart when the camera moves, voices that drift between clips, and scenes that lose their geography.
Every shot is born from references plus text. The assets carry the picture; the words carry everything else, including the geometry — who stands where, which side the camera is on, what the light does. No shot is grown out of a still frame. The only exception is the stunt reference below.

Breakdown and the shotlist

A breakdown is not a list of things to create. We turn the script into a preliminary shotlist that already carries the director's script inside it. Every shot gets a card, and the card has four groups.
The material: the location and INT/EXT with the asset that covers it; the time of day, because that is the choice of an asset variant; everyone in frame with their tags and state variants; props and vehicles with tags; the action in one to three sentences; the lines verbatim; the running time in seconds; and the complexity — simple, medium or complex. Each card carries the scene number and a letter for the shot — 50B, 50C — and that same number stays on the card, in the version log and on the prompt file, so two neighboring shots never get mixed up.
Direction: the goal of the shot in one line. The task — what the character does to get what he wants, as a verb: interrogate, expose, shame. The dramaturgy — what changed between the start and the end. The blocking relative to the camera. The acting — what the face and the body do, and what the character hides.
Camera: shot size, movement, lens, angle. Edit: cut type, pace, and how this shot hooks into the next one.
From that card the prompt is written almost mechanically, and the holes show up before you spend a generation: a shot with no goal, a character with no task, a scene with no asset.

Pre-Production: Assets

What an asset is

An asset is a pair: text + image. The text is the descriptor and it goes into every prompt word for word. The image is the reference the model anchors to. Together they keep your hero the same person from shot to shot.
All of ours were generated with LIRA. It holds the sheet rules — background, light, pose, bans — so what comes back is already checked against the habits of the model you are about to use.
The character sheet

b03999a0-5632-487d-9b04-ea2182d07a0b (1).png

A character sheet is three panels in one image: a full body from the front, a full body from the back, and a large close portrait. The prompt states this outright: the same person, consistent across all panels. The portrait is done in three-quarter view — it shows the face from two angles at once, front and side, so the model gets a fuller picture of what the character looks like.
Take the head off the full-body figures. On the wide panels the face is small and soft, and that is exactly the face the model will copy into a wide shot. Remove the head there and only one source of the face is left: the close portrait. It holds far better.
Make two versions of the close-up — with a smile and without. Otherwise the model invents the teeth and the behavior of the jaw the first time the character laughs, and the smile arrives as somebody else's mouth. Worth doing for every speaking character.
The background is solid neutral grey. The light is soft, with no hard shadows and no blown-out highlights. Avoid the word "studio": the model may draw an actual photo studio with stands and lights inside the frame, and it can bake in a studio key light that then repeats in every video generation. Write "no studio, no equipment, no walls" instead. "Overhead key light" draws the lamp itself. Rim light is banned too — a sheet with a beautiful edge glow drags that light into every scene and stops reacting to the real one. Hands on the sheet stay empty: every object is its own asset, because a prop born inside a sheet can never be dropped, thrown or taken away.

States and versions

dd4ce2be-33ec-43e2-bbfc-4d7a015bc805 (1).png
A hero has as many assets as states he goes through in the film. Cal at the start — clean jacket, orange rucksack. Cal after the fall into the Thames — wet. Cal in the third act — split brow, blood on a white tee, dirt in his hair. That is three assets, not one asset with a note.
A new variant is always made the same way: take the original sheet and change only what changed — other clothes, the wound, soaked fabric — and leave the rest untouched. That is how the skin texture survives, because the image never runs through a model twice in full. And a new variant never overwrites the old one: it gets its own name and version. Locations work the same way, so day, night and rain are three assets. So do props: Tobin's gun exists in two states, and a car has separate front and back interiors.
Hence the element naming format, which stays the same when you create the element, when you name it in a Seedance prompt, and when you upload it to the canvas:
@char_CB_Kel_v9                — character, project code, name, version
@loc_CB_warehouse_s6_v2        — location plus the scene it was built for
@loc_CB_kal_street_s5-46_v3    — one plate serving scenes 5 and 46
@prop_CB_gunTobin_s26_v2       — prop, scene, version
@prop_CB_sedan_interior_back   — a car interior is a prop, not a location

All of it lives on one canvas, and it is worth opening before you read on. Six hundred approved assets grouped by zone: character sheets with their states, location plates by time of day, props and vehicles — next to the team's notes and the versions that did not make it. The canvas is the source of truth on the project: if an asset is not there, it is not in a shot either. Open it beside this text and you see what the prep of a feature film actually looks like, card by card.
Canvas preview
Cully Hill Boys

The stress test

The stress test is a video test. A sheet that looks perfect proves nothing; what matters is whether the asset survives motion. Ten generations — different actions, different shot sizes, different locations — recognizable in ten out of ten. We ran them as real prompts: the character runs, raps, talks on the phone, cries, laughs. That is how you find out a face is only stable while the hero is calm.
Test the character and the location together. The two assets pull on each other, so a character tested against nothing tells you nothing — never test a hero before his location is ready. Test him next to the assets he will share the frame with, too: a hero who holds up alone often breaks in a two-shot.
When it falls apart, the asset can be at fault, not only the prompt. Slop and a hero who dissolves halfway through a shot are just as often a weak sheet or a weak plate as they are a weak description. Fix the words first; if the same thing breaks again, rebuild the asset.
Voice and accent

Voice is not an asset. It is a set of precisely written conditions, decided before the dialogues: register, timbre, tempo, accent, manner. Our characters spoke exactly as the block was written — no external cloning, no re-recording. Which is why the block is pasted into the audio section verbatim every time and never changes, not even a synonym: change the wording and you widen what the model samples from, and the voice drifts. The accent is part of the block, named as a category plus one or two phonetic markers:
CAL — voice: "A 25-year-old English man. Smooth, relaxed mid-range baritone;
casual, unscripted, and conversational delivery; South London street accent —
dropped h's, glottal t, -ing to -in'; nostalgic and warmly reflective."

TIKA — voice: "A man in his thirties. High tenor, fast and theatrical; Indian
English — retroflex t and d, full unreduced vowels, syllable-timed rhythm; a
performed politeness that cracks into a screech when he is contradicted."
One clip holds one speaker and one short line. Longer exchanges are written as separate clips, and the answer lives in the next one.

Locations

968e2dc4-2cc8-4e92-913a-5ca1a68ec44d.png

Locations are generated as a wide or medium in three-quarter view. Not frontal: a frontal picture of a room is flat wallpaper, the model cannot read volume from it, and past the frame edges it invents new surroundings every time. Three-quarter gives it depth, so it places the heroes correctly and yields almost a full circle of angles from one plate.
Leave an anchor in every location — a column, a lamp, a sofa, a crooked chair — and tie the staging to it. "The hero at the lamp, facing the door" works; "the hero in the room" is a lottery. Keep one light logic: one source, one direction of shadows, never two suns. No people and no weapons in the plate. Against the render look, use the language of real surfaces: rust, cracks, tape, fingerprints, oil stains, water marks.
A reverse angle can be pulled out of a video. Generate a video of the location without people, with the camera slowly walking through the space: the model draws the other sides of the room consistently with your plate. Take a screenshot of the angle you need, bring it into Seedream or Nano Banana and ask it to improve the texture and the light. A full location kit out of one image. A dialogue location needs that kit — three-quarter, front, reverse and a background plate for each hero in the scene. A pass-through location needs one angle.

Look and color

8f61fb12-2ea7-46fd-a33a-10a8925a32e9.png
The look and the color are decided during asset prep and creation, not in post-production. The film has a visual bible written before the first shot, and every plate was built to it. The film is split into worlds, each with one register: the estate is drowned khaki-green and wet asphalt; the grime scene is concrete and one CRT screen; the mother's house is warm white with honey oak; Vernon's club is oxblood, mahogany and tarnished gold; Tika's world is lacquered crimson and mirror-bright brass; the Thames is black water; the police machine is grey concrete with no warm note at all.
Inside a world the frame is 80–85% base field, 10–15% one or two accents, and about 5% counter-note. The accent is not graded in — it is found as an object with a real source in the frame: a green door, a sodium lamp, an orange tent, the glow of a monitor. One hue is separated by finish and age rather than shade: both bosses live in red and gold, but the old one is patina — dried oxblood, tarnished gold, one aged lamp — and the new one is polish: saturated crimson, mirror-bright brass, many identical lamps in symmetry. Written that way, two rich interiors stop looking like one set.

Pre-Production: Prompts

The fifteen-block skeleton

Every serious shot is written in the same blocks, in the same order: SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · FIRST FRAME AND SPATIAL BLOCKING · FORMAT MODE · OPTICS · CAMERA · ACTION TIMING · PHYSICS · LIGHTING · AUDIO · CHARACTER ACTING · STYLE · QUALITY · POSITIVE CONSTRAINTS.
There is no negative block. A prohibition is written as the desired outcome inside the relevant section, because "does NOT fall on his back" reads to the model as an invitation to think about falling on his back. Write "falls on his stomach".
Two rules about references, because they break generations more often than anything else. Every tag appears exactly once, inside ACTIVE REFERENCES — a duplicated tag at the end of a prompt is the most common reason a generation refuses to launch. And a location reference carries an explicit ban on inheritance: it controls geometry, materials, light and atmosphere, but never framing. Without that line the model hands back a near-copy of your plate. The budget per generation is nine images, three videos and three audio references, and that budget decides how many named heroes can share a shot.

An example prompt: scene 102F, the backstage corridor
Scene 102F, shot p113 — THE COMMONS, backstage corridor, night. Oli is off-screen trying to kick a door open; Cal and Horace watch. This is the whole prompt as it went to the model.
OPTICS: 200mm long telephoto (FOV ≈12°) — heavy compression, SHALLOW depth of field; a tight CLOSE-UP two-shot of the two lads' faces, corridor compressed and soft behind.
CAMERA: ONE continuous shot on a BREATHING HANDHELD — a calm living float (SETTLE feel) on Cal & Horace, who watch OLI off-screen behind the camera; their eyelines sit just BESIDE and slightly ABOVE the lens — NEVER into the lens. When they leave, the CAMERA STAYS PUT — no pan, no follow. No cuts, no slow-motion.
LIGHTING: overhead cool-white FLUORESCENT box-fixtures, cool downward pools; cold cyan-teal field, red-brick + white-painted brick; lone warm note = small dull-RED FIRE-EXIT glow deep behind them. Low-key, deep shadow, true negative fill, never flat front light.
MOVEMENT NOTE: Cal and Horace react on DIFFERENT rhythms and DIFFERENT intonations — Cal the silent weary facepalm, Horace the exasperated deadpan talker; never mirrored.

REFERENCES
@loc_CB_commons_backstage (THE COMMONS — BACKSTAGE CORRIDOR, night): cool-white fluorescent box-fixtures, white-painted brick + red brick walls, a WHITE DOOR (SHUT the entire take) and dark column mid-corridor, dark-GREEN fire-exit doors (SHUT the entire take), flight cases + coiled cable, milk crates, a stage WEDGE MONITOR, dark concrete floor. EVERY door visible in this frame stays CLOSED and MOTIONLESS from first frame to last. Controls geometry, materials, light and atmosphere ONLY — not framing.
@char_CB_Kel (CAL — beaten, frame-LEFT): late-20s, thin/exhausted, messy dark hair, stubble, FACE scrapes + scalp HEAD WOUND, BLOODIED dirty white tee, grey cargo trousers, blue trainers. The TALLER of the two — his head-top clearly the HIGHER head in frame. 100% matches.
@char_CB_Horace (HORACE — frame-RIGHT): younger man, curly black hair, glasses, light beard; GREEN cropped jacket over navy tee, baggy grey jeans, olive trainers; thin and narrow; about 10 CM SHORTER than Cal — his eye-line sits at the level of Cal's MOUTH, his head-top clearly LOWER in frame. 100% matches.
(OLI — OFF-SCREEN ONLY, no reference loaded: he is NEVER visible — not a limb, not a shoulder, not a shadow, not a reflection; the door he kicks is BEHIND the camera and never enters frame; his two failed kicks and the final door-opening happen strictly BEHIND THE CAMERA — UNSEEN and SILENT.)

HORACE VOICE (verbatim): "A 20-year-old English man. High-pitched, nasally tenor; rapid, erratic delivery; South London street accent; natural conversational stutters." — HERE: flat, tired, nasal, deadpan exasperation; he says his ONE line and then stays SILENT for the rest of the take.
CAL VOICE (verbatim, non-verbal): "A 25-year-old English man. Smooth, relaxed mid-range baritone; South London street accent." — HERE: a heavy weary sigh only, no words.

FORMAT — ~12–14 seconds, real-time, ONE continuous shot, no cuts, no fades. NO music score — muffled gig bleed only. NO off-screen kick/door sounds. NO slow-motion.

——— THE SHOT ———
0.0s–3.0s — 200mm tight two-shot, positioned BACK in the corridor by the WHITE DOOR and the dark column: CAL (frame-LEFT, the taller head) and HORACE (frame-RIGHT, head-top lower) watch OLI (OFF-SCREEN behind the camera), eyelines just BESIDE the lens. At ~1.5s the FIRST unseen kick happens — and IN THE SAME SECOND their faces SOUR: a slow unimpressed blink from Cal, Horace's brows knitting in disappointment.
3.0s–6.0s — at ~4.0s the SECOND unseen kick fails — same-second reactions: CAL exhales a heavy weary SIGH, eyes briefly closing, and brings ONE hand up to DRAG SLOWLY DOWN his face. Horace's head tilts, incredulous.
6.0s–8.5s — HORACE, flat and nasal and exasperated, calls out toward Oli off-screen — eyes beside the lens, not into it: "Pull it, Oli." — a tiny eye-roll, a limp gesture toward the unseen door. After this line NOBODY speaks again.
8.5s–11.0s — at ~9.0s, strictly BEHIND THE CAMERA, Oli finally gets his unseen door open (silent, invisible — NOTHING in frame moves) — same-second reads, both SILENT: Cal a tiny relieved-but-unimpressed nod, Horace a small "there you go" eyebrow-raise.
11.0s–13.5s — CAL and HORACE EXCHANGE A LOOK — Horace flicks first with a weary eye-roll, Cal meets it with a tired headshake and the ghost of a fond smirk — then, still SILENT, both walk FORWARD, PAST the camera and OUT of frame: CAL on the LEFT of the lens, HORACE on the RIGHT, never crossing — while the CAMERA STAYS PUT. END on the empty corridor.

CHARACTER ACTING
CAL (left, the taller, silent weary): unimpressed slow blink on the first fail; on the second, the heavy sigh and the ONE slow hand down his face — bone-tired; the tired headshake with a flicker of fondness on the exchange. EYE-LIFE: weary, real blinks, eyes to Oli off-screen then to Horace.
HORACE (right, ~10 cm shorter, exasperated talker): brows up, incredulous head-tilt, a hand half-raised in disbelief; the line lands FLAT and put-upon, with a small eye-roll and a limp point at the unseen door. Completely DIFFERENT rhythm from Cal, never mirrored. EYE-LIFE: lively, darting, real blinks behind the glasses.

POSITIVE LOCKS
HEIGHT RULER: Cal is the TALLER — HORACE about 10 cm shorter, his eye-line at Cal's mouth level, his head-top clearly LOWER in frame. OFF-SCREEN LOCK: Oli is NEVER visible — not a limb, not a shadow, not a reflection; kicks and door-opening are UNSEEN and SILENT, read only in the two faces. IN-FRAME DOORS LOCK: every door VISIBLE in frame stays SHUT and MOTIONLESS the entire take; NOTHING in frame opens or moves at ~9.0s or any other moment. EYELINE LOCK: both eyelines sit just BESIDE the lens — NEVER into it. SPEECH COUNT LOCK: the ENTIRE take contains exactly ONE spoken line — Horace's three words "Pull it, Oli." at ~6.0s; after it his mouth stays CLOSED to the final frame; no ad-libs, no mumbling, no speech in ANY language; Cal speaks ZERO words. EVENT TIMECODES (reactions land IN THE SAME SECOND, never a beat late): kick ~1.5s → faces sour; kick ~4.0s → the sigh and the hand down the face; ~6.0s the line; ~9.0s the unseen door opens; ~11.0s the exchanged look → both walk past the lens, camera stays put. Colour 60:30:10. Nothing modern beyond 2011.
Optics

Optics is written in degrees, not millimeters, off a ladder of ten anchors: 180° · 135° · 107° · 84° · 63° · 47° · 29° · 18° · 12° · 8°. The native zone, 29–84°, comes out reliably; past it the risk starts.
The main law is that content decides the lens. The model does not obey the number — it infers the lens from what is in the frame, which is why detail on 135° collapses and a crowd on 8° collapses. And the lens has to be nailed down per shot, or it slides to a comfortable middle: "one lens per shot — 84°/47°/47°/29°/47°, FOV changes only on the hard cuts". A long lens needs the whole observation pattern or it snaps back to normal:
8° diagonal field of view, super-telephoto observation lens character, camera 20
to 25 meters from subject. Extreme background compression, background flattened
into a soft colour wash, only the subject is sharp, everything else dissolves into
creamy bokeh. Foreground occlusion is mandatory: blurred foreground objects occupy
the lower 30 to 45 percent of frame as oversized dark bokeh shapes.

Geography: the master shot and the spatial map

Still 2026-07-24 172610_2.1.1.jpg

Every scene opens with a master shot. A wide with fixed blocking, about a second long, no lines and no action: the model photographs the arrangement — who stands where, what lies where, where the light comes from — and holds it in every following shot of the scene. Remove that second and the heroes start swapping places. Two hacks: let someone say one short word like "hm" in it and the model treats the wide as a proper shot more readily; and if the scene answers the previous one, feed the tail of the previous clip's line into that first second, so the actor answers the right thing in the right tone and the two clips glue at the seam.
Under the master shot sits the spatial map — a floor plan in a few lines, written once per scene and pasted into every shot of that scene unchanged. It cured the most expensive problem of our early takes: heroes teleporting, swapping places, the camera jumping to the other side of the room.
Compass for this scene: the WINDOW WALL is the camera side (all coverage shoots
from the window side — the 180° line is never crossed); the STAGE is deep
frame-RIGHT; the red EXIT double door sits beside the stage frame-right; the
chair rows fill the middle of the hall facing the stage.
CAL stands at the second chair row, arm's length from the aisle; OLI at the
stage edge, one long stride from the EXIT door; HORACE by the mixing desk.
EXACTLY THREE people, nobody else, the hall otherwise empty.
Positions come from what is visible in the plate, not from distances. Meters mean nothing to the model, and "to the left of the hero" means less than nothing, because it does not know where the hero is. Tie every body to a landmark it can see — the lamp, the second chair row, the stage edge, the door — and use frame-left and frame-right for sides. Say which side the camera is on and which line it never crosses: that one sentence keeps every cut of the scene on one axis. After every cut, name again who is where and where they look. And give a static dialogue a corner of the room rather than the whole room: less space, less choice.
When a generation contradicts the real location, re-read the reference, not the prompt. Our cage-football scene attacked the wrong end of the pitch for several versions because we wrote it from memory.

Acting

Still 2026-08-07 165606_2.474.1.jpg

The acting master profile

Acting is locked the same way as the look and the voice, and it has its own system prompt — the acting skill, in the attachments. Every hero gets one behavior paragraph, written once before shooting. In each scene it is adapted to the posture and the action, but the core never changes. A behavior that is physically impossible in a scene is transferred rather than deleted: a hero who paces the room, sat down on a sofa, does not calm down — the same energy goes into micro-sway, wrist-flicks and paper-tearing.
One default for everyone, in every prompt: eye-life. Micro-saccades, a named gaze target, a realistic blink rate, live catchlights. For controlled characters the blinks are rare and slow — a chosen stillness, never a dead stare.

Behavior, not feelings

A living scene is a hero who wants something, something in his way, and him acting to get it. The emotion is born out of that fight. Give the model a goal and an obstacle, and change the way he fights across the scene: he jokes → it fails → he pushes → it fails → he begs. Every change is a visible event: a pause, a change of posture, a change of tempo. A scene where the hero does one thing all the way through plays flat.
Physics, not adjectives

On "sad", "angry", "shocked" the model improvises and gives a shallow result. For a deep emotion describe the work of the muscles: a tremble, a jaw clenched and flexing, cheekbones drawn tight, a light exhale through the nose. On top of the muscles, intention — one line of inner monologue, marked as unspoken. The model builds micro-expressions from the goal, and the face starts living between the lines.
Add phased blinking: "one lazy blink → a quick DOUBLE-BLINK → one HARD reset-blink". Always write the gaze direction. And against frozen faces in a static shot, one visible micro-event every one or two seconds — stillness written as held tension, because "nobody moves" freezes the frame itself.
Here is how it looks on two heroes in one shot. The words "nostalgic", "jealous" and "sad" appear nowhere in the prompt:
CAL — INNER LINE (unspoken, never voiced, never subtitled): "this room used to be
the whole world." Micro-acting built from it: for once the ADHD engine IDLES — the
fast jittery stride carries him up the aisle, fingers worrying a loose thread — and
then, looking at the stage, he actually STOPS: a rare full stillness, the fidget
dying mid-motion; eyes make one slow pass along the stage edge and settle there; a
small swallow; the half-smile arrives late and soft, not performed.

OLI — INNER LINE (unspoken): "don't let them see it means something." The swagger
walks in first — chin back, shoulders rolling once, the appraising squint of a man
pricing the room — but the eyes betray him: they snag on the stage a half-second
too long, one sharp nostril flare, a jaw clench swallowed down

Three signs of a living shot

The reaction starts before the other line ends. The listener gets the point mid-sentence and his face already answers. After an important event, give the hero a fraction of a second to take it in before he speaks.
Emotion does not switch off instantly. After a heavy moment the breath is uneven and the hands unsteady — that tail carries into the next clip and stitches the cuts.
The hands stay busy. A hero does not have a conversation; he fixes, counts, pours, squares a chair and talks over it. The strongest accent of a scene is the moment that work stops because of what he just heard.

Music scenes: rap and lip-sync

Still 2026-08-07 165606_1.1867.1.jpg

The problem and the pipeline

A video model will not perform your song. Ask it to rap and you get a mouth moving to nothing. Ask it to generate music and you get either a refusal or something the edit will fight. So the music never comes from the model: the track is written and recorded first, and then the model is made to perform it.
The track is finished — full verse, real vocal, final mix — because the mouth gets locked to a specific waveform and a demo you plan to replace will not do. It is cut into blocks of about twelve seconds, the shot length the model handles reliably, with the cuts falling on the vocal's breaths and never mid-word. Each block becomes a video file with a black picture: the video track is a placeholder, the audio track is the block of the song.
The generation's audio is switched off in the settings. The vocal still drives the lip-sync, because the mouth is built from the waveform, but the clip comes back silent — so the copyright check has nothing to catch and cannot block the take. The track is laid back under the silent picture in the edit, which is where it belongs anyway.
The block and its lyrics go to Claude, and a normal prompt is written on them plus two add-ons. Blocks are generated one at a time, and the finished blocks butt together in the edit into the full performance — the seams fall on the breaths.

Two add-ons to the prompt

One: the file is the song, and he is singing it. Not a guide, not a reference, no explaining of the workflow — the model has no interest in the workflow, and meta wording confuses it. What works:
@[Video 1](video_1) — THE TRACK THEY ARE PERFORMING (this file carries the
12-second block of HORACE'S VERSE). The audio of this file IS the live performance.
HORACE SPITS THIS VERSE: his mouth carves EVERY syllable of the Video 1 vocal
exactly as it lands — rap is near-continuous, so his mouth rests ONLY in the file's
own breath-gaps. (The file's own picture is black filler — the image never comes
from Video 1, only the TRACK does.)
Two: the lyrics of the block, plus the lock. Written-out words help the mouth shapes, because the model reads the phonetics and pre-shapes the vowels. But the text and the audio will not match at the edges, and there the file must win:
LYRICS OF THIS BLOCK (as heard in Video 1 — the FILE is the truth: if the block
starts or ends mid-line, the mouth follows the FILE, not this text): "You better
make it clear bruv. 'Cos if you climb that hill you better recognize the skill
blud…"

LIP-SYNC LOCK (HARD) — Horace's mouth belongs to the Video 1 vocal and to NOTHING
else. FRAME-ACCURATE: every syllable shaped exactly as it sounds; no lag, no drift,
no idle mouth — if the mouth misses the timing of a bar, the take is wrong.

MOUTH OWNERSHIP — every audible word belongs to Horace. The other mouths are ALIVE
— open-mouthed laughter, whoops, silent 'heeey's — but they NEVER imitate, echo or
mouth the lyric's words.

Production

Organization and the log

Work runs in scene blocks, in the order of the film, each block in its own shotlist file. Every shot has a number, a timing and a full prompt. Descriptors and the fixed look-and-camera block of each world live as constants, so one edit updates every shot at once.
We generated in batches. Every iteration was surgical: one line changes, the rest stays word for word. Everything goes into the log — version, what changed, verdict — 137 entries in our case, and the log shows which shots fought back: v15, v10, v9. Without it you cannot repeat a good shot, and you cannot tell whether you already tried this fix.

Fixes that saved generations

After fifteen to twenty generations, look for another solution — not a better sentence. The number depends on the complexity of the shot. Split it in two, drop an action, change the angle, or get the physics another way. Every failing shot we saved was saved by changing the shot, never by rewording it.
Complex action never sits in the middle of the timing. The door would not break: the hero shuffled beside it and froze. Now the action opens the prompt — "he is ALREADY mid-swing, the door ALREADY cracking" — and the approach is a separate shot.
A crowd is one asset with a range of heights and clothes, plus one or two lead extras with their own assets for close-ups. Over fifteen people the crowd collapses into three to five figures, so a packed room is written as bodies pressed against the stage edge with arms in the foreground, never as a number. And a crowd is the era: our 2011 gig has no phones and no glowing screens — dark silhouettes, swaying arms, the odd lighter flame.
A car interior is its own asset, separate from the car and from the location — one of the most reusable things we built.
If the model keeps drawing what you never asked for, ban it by name. Our railway plate insisted on arriving as a station: platforms, canopies, floodlight rows, a standing train. A lock listing all of it as absent, plus an exact track count, cured it.

Laws instead of requests

A rule becomes a law when it has a name, a visible proof in the frame and a sentence stating what counts as a broken shot. There are about 150 named locks in our prompt library, and roughly eighty sentences end in "= failed take". Four we used constantly:
Scale is set by three things at once — a real-world measure, a fraction of the frame, and a comparison to an object already in the shot.
Height is set by a direction to fail in: "NOT taller by a single centimeter; if in doubt, render him a touch shorter".
Object count is written frame by frame, because the model duplicates props in motion: a sandwich knocked out of a hand becomes two.
Emotion is clamped from both sides, because a tone written as one word arrives as caricature: "between joy and aggression; a rage-twisted face = failed take; a soft beaming smile = failed take; deadpan = failed take".

The edit in parallel

The edit ran alongside generation. The editor assembled scenes as they arrived and ordered what was missing: "need a cutaway to the hands", "need a wider one". A re-shoot costs minutes, so the edit shaped production instead of waiting for it. Generations almost always feel slow in tempo: cut more aggressively than feels right, and plan to trim the first and last half-second of every clip, because the edges drift.

Post-Production

After picture lock, a separate polish pass. Some shots needed it — text on a sign, a number plate, a small artifact that only shows on a big screen — and those are retouched frame by frame. A shot that is properly broken is regenerated instead, from the saved final prompt with one line changed, which only works because the prompt library is complete and versioned. First priority: close-ups of faces and hands. All of it before color.
Generation supervising is its own job, not a hope. Someone watches the assembled cut for shots that technically exist but do not work — a look that lands a beat late, a hand that reads wrong, a face that drifts on the third second — and sends them back with a named fix. Slop that survives to the screen costs reputation; slop found in the assembly costs one prompt.
Color starts with unification: every generation arrives with its own built-in grade, so the colorist first brings neighboring shots to one look. The look itself was baked into the location assets in pre-production, so the colorist refines rather than invents.
We did not re-record the voices. The lines were cleaned straight from the generations — noise removal, evening out the timbre between clips, placing the voice in the space — with a studio recording only where a clip came out with no usable voice. Sound design and music were built over continuous ambiences: one shared atmosphere glues generated shots into one space even where the picture drifts. Which is why "SFX only. No music." is mandatory in every prompt.

Conclusion

Five rules hold the whole film.
Assets first. Not one shot until every character, location and prop is locked, named, versioned and stress-tested. This rule saves more money than everything else combined.
Describe everything, every time. The model has no memory. The descriptor goes into every prompt word for word and is never shortened.
Change one thing at a time. One line per iteration, everything into the log. Rewrite a prompt fully and you lose the parts that worked.
Give the model less freedom. A corner instead of a room, a landmark instead of open space, a map instead of guesswork, one lens per shot, one action per beat. Laws with visible proof instead of requests.
If it will not come together, simplify the shot, not the wording. Split it in two, remove an action, change the angle.
Every rule here exists because a shot failed without it. Take the attachments and start with one scene: one locked character, one location plate, one prompt skeleton. The pipeline does not need a big team — it needs the rules followed, and it scales down to a team of one.

What's attached

The CINEDANCE skill bundle (writer, auditor, workbench and the pre-send self-check), the LIRA image skill, the acting system prompt with the master-profile format, the visual and color bible, the style prefixes for all five worlds, the optics reference with the ten FOV anchors, the voice system with the accents, the music-scene prompts with their lip-sync locks, and the prompt library with the full text and version history of every shot in the film.
