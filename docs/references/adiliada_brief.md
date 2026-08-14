# ADILIADA — Project Brief

Source: Higgsfield project brief, read-only, updated 15:03 (fourth project
supplied to PRE, after HELL GRIND, CULLY HILL BOYS and ONEIRIC).

Canvas asset counts at time of reading — total 11299, grouped by sequence:

| Folder | Assets |
|---|---|
| 1. COLD OPEN: "The Crow Hunt" | 1451 |
| 2. MAIN TITLE SEQUENCE | 4637 |
| 3. SPACE SCENES | 2296 |
| 4. MEETING THE VILIAN | 2363 |

---

Alright. While this thing still thinks it's the one in charge up here, we've got about five minutes.
Let's skip the introductions, you know who I am.

I'd rather tell you how my colleagues at Higgsfield put together a series about me. The pipeline, the tools, the tricks they picked up along the way. Some of which I approve of.

It started when I died. Then I died again. On the third one it finally clicked that this is my thing now: I die and wake up in another universe, in another version of myself. Some people get superpowers, some get a cool suit, and I got a lifetime travel pass that activates on death. And yes, it hurts every single time. Nobody warned me that rebirth isn't a flash of light, it's the feeling of being turned inside out through your... ahem, ahem. Just inside out, let's leave it there.

So that's my life now: hopping between worlds, collecting cosmic artifacts that can stop the end of the world before it lands. Not alone. With me there's grandpa Rex, a war veteran who shoots before he says hello. My stepsister Mia, a hot girl, especially if we're talking about her temper. And... Chung, my stepbrother. I could talk about Chung for a very long time, and I am deliberately not going to, because right now we're talking about me.

## About the project

ADILIADA is a photoreal AI short film, roughly six minutes, built in the format of a series opening. Every frame is generated: no filming, no sets, no camera crew.

The rest of us exist as reference assets, and every shot is born from those references plus text. There was one goal: to make you believe you're watching a clip from a big, high-budget series that already exists. Charismatic characters, a black-comedy sci-fi setting, the sense that several seasons have already been shot off screen. The whole structure grew out of that goal. It comes in three parts.

**Part 1. The scene before the titles.** A classic cold open that gives you no context at all and only multiplies the questions. Who is this? What's happening? Is that the main character? Why did the main character die thirty seconds in? On the last one: yes, that's me, and yes, I die thirty seconds in. No hard feelings. Dying is my job and my bread and butter.

**Part 2. The title sequence.** A main-title reel built the way sitcoms and cartoon shows of the 2000s built them. You get the short visual version of the story: what happened to me, who I am, how I found my crew, and what kind of show to expect from here. It's packed with pop-culture references and rides on a driving, banging track that plays off the name itself: ADILIADA. You'll get it when you watch it. No, really, listen to it, A-DI-LI-A-DA, that thing goes hard.

**Part 3. The scene after the titles.** The titles roll straight into what looks like the rest of the episode and shows all of us as if we've known each other for ages and been through more than one season together. We have known each other for more than one season, you just weren't told about it. This part drops you into the context and then cuts off at the best possible moment. All of it so you'll be sure the rest exists, that the series is out there and can be found and finished.

In production terms the guys had two completely different jobs. The first was to invent the worlds. You need a lot of universe concepts and a lot of character versions, and every one of them has to make you want to find that exact episode in that exact setting; the world I fall into has to grab you immediately. The second was to hold the recognition. We exist in several universes at once, every version has its own face and its own personality, and you never know in advance whether we're the heroes in this world or the villains.

At the same time, any alternate version of me still has to read as me. And that's exactly where the whole difficulty of the project lives, somewhere between "make him different" and "make him the same".

One second.

The crow is objecting. She needs a reminder about who's in charge here.

BAAAAAM!

There we go, now we're in a dive. Continuing.

## The tools

- **Seedance**: every shot, all the video, all the generations.
- **Claude + skills.** A skill is a playbook of rules that Claude loads and works by. They have two: an acting system and CINEDANCE, the video-prompt writer. The acting system decides what exactly I play in a shot. Nobody asked me, naturally.
- **Diagram Skill.** In shots with several of us in frame, text alone won't hold the staging. The skill turns a frame into a schematic color-coded diagram, and Seedance reads exact positions, poses and facing directions off it. Being a colored circle with an arrow is humbling. Works every time.
- **Depth map.** A depth map is a black-and-white image where the light areas mean near objects and the dark ones mean far. The model reads it as the depth skeleton of the scene: an exact sense of three-dimensional space, which means correct composition, volume and proportion. Without it the space drifts, and you'd be watching me fight a bird in a city that rearranges itself every three seconds.

## 01. Development

On an AI film a weak scene costs real money: you find out it doesn't work only after you've generated it. So before anything is generated, the team writes every scene out in terms of drama, and every scene gets argued over for whether it actually works: what the event is, what the character wants, where the turn happens.

After that the project goes into a step-by-step storyboard: scenes are broken into shots, and only on the storyboard does it become clear how good a scene really is, as opposed to how good it was in our heads.

## 02. Pre-production

### Assets

An asset is a pair: text plus image. The text descriptor goes into every prompt word for word; the image is the reference the model anchors to. Together they keep a character the same person from shot to shot.

### Character sheets

A character is built in two passes with two models. Soul Cinema makes the face: always generated in close-up, so the model captures the identity at maximum detail. That close-up face is the anchor every following asset of the character is checked against. Soul 2.0 then builds the looks: full-figure images with the wardrobe, costume, materials, silhouette, all fitted to the locked face.

Then both passes are assembled into the character sheet in Seedream / Nano Banana / ChatGPT, with one hard condition: the original close-up portrait stays untouched. It never runs through a model again; the assembly happens in editing tools around it. Every detail that changes between states goes in point by point, with masks, without touching the base: a scar, a haircut, a piece of wardrobe, dirt, a wound. The base image stays the same pixels.

For ADILIADA the same principle works at the level of universes: an alternate version of the character is built from the same base face, the wardrobe, makeup, hair, scars and damage all change, but the face stays the same set of pixels. Which is why in any world Adil reads as Adil, even when he's the villain there.

### Locations, the reference frame and visual anchors

A location is built in two approaches. Soul Cinema makes the main location image, the reference frame the whole team leans on stylistically from then on: the period, the world, the color, the characters.

In every scene and every location we tried to plant visual anchors, the things that later help hold the scene consistent and keep the characters in the same places across different generations: the chair a character sits in, the window two of them talk by. After that the locations were edited and tuned for color, light and saturation, so that all of them would match in character once the generations started.

## 03. Production

### Video prompts, CINEDANCE

Every shot is written by the CINEDANCE skill in the same blocks, in the same order:

```text
SCENE CONTEXT
ACTIVE REFERENCES
LOCATION MAP
GAZE / EYELINES
FIRST FRAME AND BLOCKING
SEGMENTS (timed beats)
DIALOGUE
AUDIO
PHYSICS
LIGHTING
STYLE / FORMAT
POSITIVE LOCKS
```

Seedance only sees the text in front of it, so every prompt is an island: positions, poses, wardrobe, props, optics, light, all spelled out from scratch, every single time. "Same as the previous shot" is an instruction to a model that has no "before".

## 04. Post-production

1. **Assembly.** All scenes in script order. The goal: see the whole film, find the sags and the coverage holes.
2. **Rough cut.** Rhythm, trims, rearrangements. This is where the main list of shot reorders takes shape.
3. **Generation supervision.** A quality-control pass after the rough cut: regenerating broken shots, clearing out AI slop, catching the moments that don't work before the fine cut.
4. **Fine cut.** Precise fitting, screenings with cold viewers.
5. **Picture lock.** The picture is fixed. After lock there are no new generations, except emergency fixes with notice to color and sound.

After picture lock the material goes to cleanup, color correction and the sound work: scoring and sound design. Every generation arrives with its own grade baked in, so the colorist's job here is unification: bringing neighboring shots to one look and giving the picture a single, coherent feel.

## 05. Conclusion

- **Assets first.** Not a single shot until every character, location and prop is built, named and locked.
- **Describe everything, every time.** The model has no memory. Descriptors, location maps and staging go into every prompt word for word.
- **Hold the face, change everything else.** A new universe is a new look, not a new person. The base is never touched.
- **Say what you want, not what you're avoiding.** The words you write are the words you summon, including the ones sitting inside a "no".
- **Direct, don't describe.** The scene event, the motive, the goal, the obstacle, the tactic. Directing is the one part the model still won't invent for you.

That's it, you're on your own from here. The crow has finally worked out where we're heading and she disagrees. If I die again, see you in another universe. If I don't, see you in the next episode. It exists, go look.
