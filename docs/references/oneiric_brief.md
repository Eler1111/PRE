ONEIRIC
Updated today at 00:00
This is the project breakdown for ONEIRIC, our AI short film: the pipeline, the tools, and the hacks we learned along the way.

Logline: Four friends in a dorm common room daydream about a neural net that could drop you into any world — Troy, deep space, a fairy tale. Then the quiet one is asked where he'd go, and his answer changes what the whole afternoon means.

16x9 (1).png

About the project

ONEIRIC is a ~20-minute photoreal AI short film. Every frame is generated: there is no filmed footage, no sets, no camera crew. The characters exist only as reference assets, and every shot is born from those references plus text.
The structure of the film defines the whole production. Its spine is one long dialogue scene — four friends in a student dorm common room, discussing a neural engine that could drop a dreamer into any world. Three times the film smash-cuts into those imagined worlds — a battle on the plain of Troy, a chase through a galactic cruiser, a griffin flight over a fairy-tale valley — each a short set piece with its own art direction. The final scene pulls back and reframes everything that came before it.
In production terms that means two very different jobs. The dream worlds are brief and spectacular — their challenge is design and scale. The common room is the opposite: four characters in one space, held across dozens of shots — same faces, same voices, same seats, same eyelines, for most of the film's runtime. A video model has no memory: it forgets a face between shots, redraws the room when the camera moves, gives a character a new voice in every clip. Keeping that one room stable is the hardest technical task of the film, and most of the pipeline below exists to solve it.

The tools

Seedance — every shot, all video and speech. Assets live as named elements on the project.
Claude + our skills — a skill is a playbook of rules Claude loads and works by. Ours: a scene-drama engine, an acting system, and CINEDANCE, the video-prompt writer.
The Diagram Skill — in shots with several characters, text alone doesn't hold the staging.The skill turns any frame into a schematic color-coded diagram, and Seedance reads exact positions, poses and facing directions from it.
The anamorphic hack — Seedance doesn't reliably hold anamorphic optics asked for in a video prompt. So the lens character is baked into the location assets themselves: the model reads it straight off the reference image and keeps it. The recipe is in the Assets section.

Screenshot 2026-08-12 at 12.32.11.png


01 · DEVELOPMENT
The script goes through a Stress Test

On an AI film a weak scene costs real money — you find out it doesn't work only after you've generated it. So before anything is generated, every scene runs through the Script Stress Test: a Claude skill that checks it against a five-element engine — Goal, Obstacle, Tactic, Reversal, Value Shift — and returns a verdict per element, the single weakest point, and "what if" fixes from minimal to clean rewrite.
The same stage produces the director's read: for each scene, the one shared event every character lives through, and each character's own physical channel for it. Our laboratory scene: the event is "the search for self-forgiveness." Alfred relives it in the dream; the doctor hides in flawless procedure; the young medic cares for the patient beyond the checklist. The surface — routine rounds — is just the terrain the event moves through. The medic's last line, "Poor guy. Just can't forgive himself," names all three men at once without knowing it.

tig-scene-engine.skill
SKIL



02 · PRE-PRODUCTION
Assets

An asset is a pair: text + image. The text descriptor goes into every prompt word for word; the image is the reference the model anchors to. Together they keep for example a hero the same person from shot to shot.

Canvas preview
Higgsfield Canvas

One naming convention for the whole team

Every element in the project — locations, characters, extras, props, pose references — is named by a single tag convention the whole team follows. The point is simple: one element, one name. Without it a project this size quickly grows duplicates — the same couch living under three different names — and nobody knows which reference is the real one.

One tag system everywhere — on the element, in the prompt, in the table:
@loc_ON_dorm_commonroom_front_s2     location + project + name + scene
@char_ON_Rudy_s2_v1                                 character + project + scene + version
@prop_ON_pizza                                          prop + project + name 

The scene suffix ties every asset to where it lives. The version suffix appears when a state changes — a new state is a new asset with a new name, never an overwrite. A character has as many assets as states he goes through: Alfie in the common room and Alfred in the lab bed are different assets of the same man.

Character sheets

A character is built in two passes with two models. Soul Cinema makes the face: always generated in close-up, so the model captures identity at maximum detail — that close-up face is the anchor every other asset of the character is checked against. Soul 2.0 then builds the looks: full-figure images with the wardrobe — costume, materials, silhouette — matched to the locked face. 
The two passes are then assembled into the character sheet in Seedream / Nano Banana / ChatGPT — with one hard condition: the original close-up portrait is preserved untouched. It never runs through a model again; the assembly happens in editing tools around it. Every detail that changes between states is integrated point-by-point with masks, without touching the base — a scar, a haircut, a piece of wardrobe, dirt, a wound. The base image stays the same pixels, so the identity (and the skin texture that carries it) survives every new version of the character.

7ea09322-f909-493c-9151-71cdc3112704 (2).png
66999418-2fc0-4666-ac52-206c4ba5cc01.png

Locations — the anamorphic look

The film is 2.39:1 with an anamorphic lens character, and here's the problem: ask Seedance for that look in a video prompt and it won't hold it reliably — the optics drift from shot to shot. The fix is to move the lens one step earlier in the pipeline: generate the location image with the anamorphic effect already in it. Seedance reads the optics straight off the asset and keeps them — the plate itself becomes the lens.
There is no "anamorphic" switch in an image model either, so at the asset stage the effect is assembled from words — the geometry of the lens, written out:

Block for the end of a location image prompt:
STRONG anamorphic lens character: horizontal squeeze and compression,
oval elliptical bokeh, horizontally stretched highlights, curved barrel
edge distortion, chromatic aberration toward the edges. NO lens flares, NO light streaks, NO floating bokeh circles. 2.39:1.

Dose the strength with subtle / gentle / moderate or strong / maximum, and at this image stage also ban the garbage that tags along: lens flares, light streaks, floating bokeh orbs. In video prompts those words never appear at all — even as bans (see the iron rules: naming them summons them). The video prompt only describes clean glass and contained glows; the anamorphic character comes from the asset.
Screenshot 2026-08-12 at 19.00.48.png

03 · PRE-PRODUCTION
Voices are written conditions

Seedance generates the speech, but a voice drifts between clips unless it's pinned down. A voice here is a written block — register, timbre, tempo, manner — decided once, stored in the Voice Bible, and pasted into every generation verbatim, never even a synonym changed. 
Example AUDIO LOCK (Bob):
BOB — voice: warm boisterous baritone, big dynamic range, theatrical
comedic enthusiasm, a gravelly edge; bursts loud then drops to a
mock-confidential murmur, punches key words, laughs mid-line. American.

04 · PRODUCTION
Video prompts — CINEDANCE

Every shot is written by the CINEDANCE skill in the same blocks, in the same order:
SCENE CONTEXT · ACTIVE REFERENCES · LOCATION MAP · GAZE / EYELINES ·
FIRST FRAME AND BLOCKING · SEGMENTS (timed beats) · DIALOGUE · AUDIO ·
PHYSICS · LIGHTING · STYLE / FORMAT · POSITIVE LOCKS
Seedance sees only the text in front of it, so every prompt is an island: positions, poses, wardrobe, props, optics, light — spelled out from scratch, every time. "Same as the previous shot" is an instruction to a model that has no "before".
CINEDANCE HIGGSFIELD SKILL.skill
SKIL




Real fragment — Scene 2
SCENE CONTEXT
Live-action photoreal feature-film shot, about 11 seconds, continuing Scene 2. Sam, eating pizza, listens to Rudy (off-screen) and cuts him off with a skeptical dismissal; then a hard cut to Bob, who fires back at Sam, all in and trying to win the guys over. It opens on a brief silent wide of the four in their exact positions, then a medium of Sam, then a medium of Bob. The mood is warm and lively.

ACTIVE REFERENCES
@char_ON_Bob_s2_v1: big soft warm guy, early 20s, long curly brown hair, open blue hoodie over a grey UFO tee, baggy jeans. Holding a soda can in his right hand, relaxed in his armchair. 100% matches the reference.
@char_ON_Sam_s2_v1: slim 18-year-old, short in stature, about 170 cm, ginger hair, rimless glasses, navy-and-cream raglan "Quantum" tee, light-blue jeans. Seated, his head rises only slightly above the armchair back (about 5 cm). Holding a floppy slice of pizza, taking bites and chewing. 100% matches the reference.
@char_ON_Rudy_s2_v1: tall lean man, ~190 cm, short dark curly hair, light mustache with a soul-patch, oversized washed cream long-sleeve with a faded navy graphic, baggy dark jeans. Lying reclined along the couch, phone in his left hand, guitar across his lap. In this shot Rudy is off-screen for the mediums (voice only), present in the wide. 100% matches the reference.
@char_ON_Alfie_s1_v1: quiet guy in his early 20s, medium-length wavy brown hair, plain grey hoodie. Seated in the dark foreground armchair, seen from behind. 100% matches the reference.
@loc_ON_dorm_commonroom_front_s2: the warm cluttered student common room, front angle — beige couch under a window in back, brown plush armchair screen-left, beige armchair screen-right, two dark upholstered armchairs in the near foreground backing camera, cluttered coffee table, sci-fi posters, guitar. Controls architecture, materials, clutter, and light only. 100% matches the reference.
@prop_ON_pizza: a slice of pizza in Sam's hand and the open pizza box on the coffee table. 100% matches the reference.
@prop_ON_rudy_guitar: Rudy's guitar, lying across his body on the couch. 100% matches the reference.
@prop_ON_rudy_phone_s2: Rudy's smartphone, in his left hand. 100% matches the reference.

LOCATION MAP (exact positions)
BOB screen-left in the brown plush armchair, soda can in his right hand. RUDY reclined center on the beige couch (off-screen for the mediums). SAM in the beige armchair screen-right, holding a slice of pizza. ALFIE seated in the dark foreground armchair screen-right, back to camera. The cluttered coffee table with the open pizza box sits center foreground. Warm daylight from the window behind the couch; cozy amber shade. Eyelines: Sam looks screen-left toward Rudy on the couch; Bob looks screen-right toward Sam.

FORMAT MODE
Controlled three-segment sequence with HARD CUTS. Real-time motion. Dialogue delivered as spoken audio.

SEGMENT 1 — SILENT ESTABLISHING WIDE, NO DIALOGUE (~0.0s–0.5s)
The first frame sets all four in the exact positions above, matching the previous shots. Level wide, held about half a second, everyone relaxed and lively. This wide has no dialogue at all: every mouth stays closed and the room is silent for the full half-second. The dialogue happens only in the mediums that follow.
LENS: level widescreen wide, soft oval bokeh, clean crisp glass with a matte finish; the window and practical lights read as soft, round, contained glows within their own sources.

SEGMENT 2 — MEDIUM, SAM (~0.5s–5.5s)
Hard cut to a medium of Sam in his armchair screen-right, taking a bite of pizza and chewing as he listens to Rudy off-screen, his eyes toward screen-left. ACTION TASK: Sam is skeptical about the AI and wants to shoot down what Rudy is saying; he cuts Rudy off with a flat, sarcastic dismissal, sure he is right — delivering exactly his scripted line and nothing more. He speaks around the pizza, keeping the words clear.
LENS: widescreen medium framed through soft out-of-focus foreground objects — the cluttered coffee table items (a mug, the pen jar, a glass, the edge of the pizza box) sit between camera and Sam as a soft foreground; soft oval bokeh, clean crisp glass with a matte finish; light sources stay soft, round, contained glows.

SEGMENT 3 — MEDIUM, BOB (~5.5s–11s)
Hard cut to a medium of Bob in his armchair screen-left, lighting up and turning toward Sam (screen-right). ACTION TASK: Bob is a funny, warm-hearted geek buzzing with positive excitement — he genuinely believes in this technology and is trying to win the guys over in a playful, good-natured way. His "Nah, YOU'RE complete garbage" is warm teasing, not hostile; he grins, gestures with the soda can, delighted and sincere, radiating good energy. He delivers his lines.
LENS: widescreen medium framed through soft out-of-focus foreground objects — the cluttered coffee table items and the near armchair edge sit between camera and Bob as a soft foreground; soft oval bokeh, clean crisp glass with a matte finish; light sources stay soft, round, contained glows.

DIALOGUE (spoken exactly as written, verbatim, word for word)
All dialogue happens only in Segments 2 and 3. Segment 1 (the wide, 0.0s–0.5s) stays completely silent.
RUDY (voice off-screen) 1.0s–3.6s: "AI builds the whole thing around you in real time."
SAM 3.8s–5.3s: "Bro, that's complete garbage."
BOB 5.8s–10.8s: "Nah, YOU'RE complete garbage. I saw the demos, man — it's real. It's actually real."
Rudy's line is heard off-screen only (he stays out of frame for the mediums). Sam cuts in over the tail of Rudy's line. Each character says only their own line, verbatim; when a character is not speaking, their mouth stays closed.

PHYSICS
Sam's pizza slice is a clean, intact slice, floppy with a grease sheen; his jaw works with real chewing between words. Bob's soda can has real liquid weight as he gestures with it, his shoulders and torso moving with his excitement. Real weight in the armchairs as each shifts. Clothing and hair settle; dust motes drift in the window light.

LIGHTING
Warm natural daylight from the window behind the couch, low-key and cozy; the faces sit in a soft shadow with a gentle falloff, grazed by just enough light to stay readable while dropping softly into shadow. Every light source stays a soft, round, contained glow within its own source; clean crisp glass with a matte finish.

AUDIO (voice identity only — see DIALOGUE for words)
RUDY's voice (off-screen): low, deep, bassy resonant American chest voice, smooth and grounded, calm quiet confidence — the same locked timbre.
SAM's voice: bright, high-set American male voice with a reedy, nasal, hard grating edge — wiry and forceful, high mobile pitch with big animated leaps, fast clipped over-enunciated delivery, sharp sarcastic bite; the same locked timbre.
BOB's voice: warm boisterous American baritone with a light gravelly edge and big dynamic range, Jack Black-style — theatrical, playful, upbeat and delighted, punching key words with good-natured energy; the same locked timbre.
These voice identities are fixed and identical across all shots. Quiet room tone, soft couch and armchair creaks.

STYLE
Fully photoreal live-action, 35mm filmic look, widescreen frame with a gentle horizontal squeeze and soft oval bokeh, clean crisp lens glass with a matte finish, natural depth of field, organic grain, warm cozy grade, grounded realism. Window and practical light sources render as soft, round, contained glows that stay within their own sources.

POSITIVE LOCKS
Opens on a brief silent level wide (~0.5s) with the exact positions matching the previous shots — every mouth closed and the room silent through the wide, dialogue beginning only in the mediums. Then a hard cut to a medium of Sam eating pizza and cutting Rudy off with his skeptical line, then a hard cut to a medium of Bob answering Sam in a warm, playful, upbeat way — a funny, kind-hearted geek buzzing with positive excitement, teasing without malice as he tries to win the guys over. Rudy is heard off-screen only. Each speaks exactly the DIALOGUE lines, verbatim; Sam adds nothing beyond his scripted line; voices match the locked timbres. Sam looks screen-left toward Rudy; Bob looks screen-right toward Sam. Both mediums are framed through soft out-of-focus foreground objects (room clutter) for depth. Identities, wardrobe and props match the reference tags. Widescreen soft oval bokeh, clean crisp glass with a matte finish, and light sources as soft round contained glows. The image stays sharp, steady and clean.

05 · PRODUCTION
The Diagram Skill — staging for video generation

When a shot needs precise multi-character staging — who is where in the frame, in what pose, facing which way — words alone stop being enough. The Diagram Skill controls disposition directly in the generation. The key idea: make the AI treat a reference not as a picture to copy, but as a system of spatial data — lines, colors, coordinates, directions and functions. That's why we call it the Diagram Skill and deliberately avoid the words "image" or "reference" when talking about it.
tig-diagram.skill
SKIL



How it works, step by step:
Attach the frame you want to reproduce (a still, a previous generation, any composition) and ask Claude for the diagram. The skill writes a diagram-generation prompt in which the frame is a composition-only guide: exact framing, angle, crop, positions and poses — but none of its photographic look. Cropped bodies stay cropped; nothing that isn't in the frame gets added.
Generate the diagram using Seedream / Nano Banana / Chat GPT: a flat schematic line drawing on white — each figure a thin outline in its own muted color, furniture as simple outline shapes, a very faint grid. No letters, no labels anywhere on the drawing.
Add the diagram to your Seedance prompt. In the same Claude chat, ask for the video prompt that uses it. Important: Claude never sees the diagram image itself — it works from the text description of the frame only. It writes the connector block, which binds each color to a real character tag — "@A = the BLUE figure = @char_ON_Rudy_s2_v1 → on the couch, facing frame-right" — and states that the map defines positions only: style, light, faces and wardrobe come exclusively from the location and character references.

hf_20260809_110351_4d9a7dec-3a53-4831-845d-484bc51eedda.png

Win rate on staging-accurate takes goes up dramatically.
Screenshot 2026-08-12 at 21.03.48.png

Editing a diagram. Changes are requested in the same Claude chat where the original diagram prompt was written — it holds the full color key and geometry, so the edit stays consistent. Two rules. First, name every element by its assigned color, never by the object or person: "move the BLUE figure to the couch's left edge", not "move Rudy" — colors are the diagram's language; character names belong to the video prompt. Second, when generating the corrected version, the image model gets the same original frame that the first diagram was built from — never the previous diagram. A diagram is always drawn from the real shot; feed a drawing into the model and it starts copying the drawing's flaws instead of the frame's geometry.
Three details make it safe. Letters A, B, C live in the prompt text only, bound to figures through color — a rendered letter could bleed into the shot. The connector is written in positive form only: it never names the map's graphic style even as a ban, because "no flat illustration" still injects the word flat. And the diagram is always a front view from the camera's side, never a top-down floor plan — video models think in frames, not blueprints.
The everyday magic: once a scene has its diagram, coverage becomes a conversation. Ask "give me the MCU on the blue" or "now the POV of the green" — and get a re-staged diagram for the new shot size or camera angle. The same convention extends to trajectories (a dashed colored path for a thrown object or a character's cross, with start, path, end and trigger beat) and camera moves(arrows declared as camera-path-only in the legend).

06 · PRODUCTION
Acting skill — tasks, not emotions

Write "sad" in a prompt and you get a caricature or a dead face. The Acting Skill replaces emotion labels with an acting task: the character is invested in a tactic of reaching a goal, and the emotion is born from that fight — on screen, not in the adjective. For each character the skill names the scene's shared direction, his personal motive and goal, the obstacle pressing against the line, and the tactic — written as what he is doing to his partner, with the eye-work named as action: checking both of the partner's eyes, registering whether the point landed, stealing looks and snapping back.

Screenshot 2026-08-12 at 12.48.03.png

The eyes are the whole game. Aliveness = the mind visibly working on a task. Dead, glassy eyes are never fixed with lighting — they're fixed by giving the eyes a job. Alfie's confession lands precisely because the three around him play keeping the afternoon light, not "shock": the audience feels the thing nobody performs.
tig-acting-task.skill
SKIL



ACTING TASK block, short form:
ACTING TASK — [NAME] (invested in his tactic; the work happens in his eyes):
SCENE DIRECTION (shared, unspoken): [one line]
MOTIVE / GOAL / OBSTACLE: [his fuel, his fight, what presses on it]
TACTIC, moment to moment:
— "[dialogue words]" — [verb at the partner + what the eyes check]
(Safety: gaze always engaged in the task; natural blink cadence.)

07 · POST-PRODUCTION
Post-production

The edit — five stages to picture lock

—   01 · Assembly — all scenes in script order, without rhythm. Goal: see the whole film, find sags and coverage  holes.
—  02 · Rough cut — rhythm, trims, rearrangements. Here the main list of shot re-orders is formed.
—  03 · Generation supervision — quality control pass after the rough cut: re-generating broken shots, cleaning out AI slop, catching moments that don't work before the fine cut.
—  04 · Fine cut — precise fitting, screenings with "cold" viewers.
—  05 · Picture lock — the picture is fixed. After lock — no new generations, except emergency fixes with notice to color and sound.
After picture lock the material goes to a cleanup and color correction pass. Every generation arrives with its own built-in grade, so the colorist's job here is unification — bringing neighboring shots to one look and giving the picture a single, cohesive feel.

08 · CONCLUSION
What holds it together

 Assets first — not one shot until every character, location and prop is named, versioned and locked.
 Describe everything, every time — the model has no memory. Descriptors, voice locks and maps go into every prompt word for word.
 Say what you want, not what you avoid — the words you write are the words you summon, including the ones inside a "no".
 Direct, don't describe — scene event, motive, goal, obstacle, tactic. The director's craft is the one part the model can't invent for you yet.