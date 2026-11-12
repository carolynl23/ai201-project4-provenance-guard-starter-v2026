# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is not called AI, and is mostly called human

Of 10 pieces I wrote myself, at least 3 of them deliberately plain (short
sentences and everyday words, the writer from my false-positive trace in
`DESIGN.md`), **at most 1 is labelled high-confidence AI** and **at least 6
are labelled high-confidence human**. Both parts have to hold in every one of
the three trials.

**Why this target:** On a writing site, a wrong accusation costs the writer far
more than a missed detection costs the site, so I allow at most 1 in 10. The
"at least 6 human" half stops me cheating my way to that number. If I widened
the unsure band until nothing was ever called AI, the first half would pass
easily, but real writers would get a shrug instead of an answer. The plain
pieces are there because both of my signals share that blind spot. A test set
of only my fancier writing would hide the failure I'm most worried about.

---

## 2. Clearly-AI and clearly-human text are far apart

Across 5 clearly AI-generated texts (unedited model output) and 5 clearly
human texts (my own writing, not the plain pieces), the **mean `confidence` of
the AI set is at least 0.30 higher than the mean of the human set**. Also, **at
most 1 human text scores higher than the lowest-scoring AI text**. Both hold in
every trial.

**Why this target:** My unsure band is roughly 0.35 to 0.65+, which is about
0.30 wide. If the easy cases aren't at least that far apart, they can't land
on opposite sides of it, and every threshold I choose is guesswork. The overlap
limit is there because two averages can be 0.30 apart while a single bad text
still crosses over.

---

## 3. All three labels are reachable, and the AI label still catches AI

Running 9 inputs (3 I expect to be AI, 3 I expect to be human, 3 borderline),
**each of the three labels is produced at least once** in every trial. Also,
of the 5 clearly AI-generated texts from criterion 2, **at least 3 are labelled
high-confidence AI** in every trial.

**Why this target:** A label no score can reach means there's a gap in my
ranges. The starter even warns that a 0.5 stub makes the human label nearly
impossible to reach. The second half is criterion 1's counterweight. My plan
is to make the AI label hard to reach, and this puts a floor under that plan:
if I raise the threshold so far that real AI output stops being caught, I want
to see it fail here rather than call it a success. I chose 3 of 5 rather than
5 of 5 deliberately, because I'm accepting some missed AI text to protect
human writers.

---

## 4. Every appeal is recorded, and every bad appeal is refused

Tested by hand against the running service:

- 5 appeals against real `content_id`s from `/submit`: **5 of 5 return 200**
  with `status: "under_review"`, and `GET /log` shows **5 appeal entries**,
  each with the matching `content_id`, the reasoning as written, and the
  original `creator_id`.
- 3 appeals against ids that don't exist (one typo of a real id, one made-up
  id, one empty string): **3 of 3 return 404 or 400**, and **0 appeal entries**
  are written for them.
- A second appeal on an id that is already under review **returns 409** and
  writes no second entry.

**Why this target:** This is ordinary code with no model in it, so anything
short of 100% is a bug and not a trade-off. The appeal is the only thing that
stands between a wrongly accused writer and nothing at all. An appeal that
returns 200 but never reaches the log is worse than one that fails loudly,
because the writer thinks they've been heard.

---

## 5. Malformed input never crashes the service

Sending these 8 request bodies to `/submit` (empty `text`, whitespace-only
`text`, `text` missing, `text: null`, `text` as a number, a 24-word `text`, a
50,000-word `text`, and a JSON list instead of an object), **0 of 8 return a
5xx**, **8 of 8 return the 4xx status and `error` code listed in
`DESIGN.md`**, and **8 of 8 leave a rejection entry in the audit log**. The
service still answers `/ping` afterwards. Holds in every trial.

**Why this target:** Unit 8's attack set will send exactly this kind of input,
and a 500 tells the caller nothing while also hiding the attack. The
rejection-log requirement is there because an attack that shows up only as an
absence is one I'd never find. These are deterministic checks, so the target is
all of them.


---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
