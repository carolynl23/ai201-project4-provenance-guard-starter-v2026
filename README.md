# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. **The request arrives at `POST /submit`** (`app.py`) as JSON:
   `{"text": ..., "creator_id": ...}`. *Adds:* nothing yet. (Unit 8: the rate
   limiter checks the caller here first. A 429 is logged with
   `audit.log_rejection`.)
2. **The route checks the input.** `text` must be a string with at least 25
   words and at most 20,000 characters. `creator_id` must be a non-empty
   string. Anything else gets a 4xx with `{error, message}`, is logged as a
   rejection, and stops here. *Adds:* a `content_id` (uuid4), which is created
   only once the input passes.
3. **Signal one, `detector.model_signal(text)`.** gpt2 reads the first 400
   tokens and measures how predictable they are (perplexity). That number is
   squashed onto 0–1. *Adds:* `model_score` (higher = more likely AI).
4. **Signal two, `stylometry.style_signal(text)`.** Measures the shape of the
   whole text: sentence-length spread, vocabulary variety and punctuation.
   *Adds:* `style_score` (higher = more likely AI).
5. **The combining rule, `scoring.combine_signals(model, style)`.** Turns the
   two scores into one. *Adds:* `confidence`, the combined 0–1 score.
6. **The label mapping, `scoring.score_to_label(confidence)`.** Compares the
   score with the thresholds in `config.py`. *Adds:* `guess`
   (`ai` / `unsure` / `human`) and `label`, the sentence a reader sees.
7. **Log, then answer.** `audit.log_decision(...)` writes all nine fields with
   `status: "decided"`, and the route returns the response JSON. The reader
   sees the `label`. If they disagree with it, they send the `content_id` to
   `POST /appeal`, which checks that the id exists, writes
   `audit.log_appeal(...)` and moves the item to `under_review`.

Full field-by-field contracts for both endpoints are in [DESIGN.md](DESIGN.md).


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable the text is to a small language model
(gpt2). This is perplexity over the first 400 tokens, mapped onto 0–1 by a
logistic curve centred at perplexity 45. Low perplexity gives a high score,
which means more likely AI.

**Why that might differ between human and AI writing:** A language model
generates text by picking likely next words, so its output is text a model
finds easy to predict. People make odder, more specific choices that a model
doesn't expect.

**What it can't see:** Who actually wrote the words. It measures how ordinary
the wording is, and that is not the same as authorship:
- **Plain human writing scores as AI.** Short sentences and common words are
  typical of second-language writers, younger writers, people writing plainly on
  purpose and formulaic genres such as lab reports. All of these look
  "predictable". So do famous or boilerplate passages, such as quotations or
  standard legal text.
- **Unusual AI writing scores as human.** AI text with rare words, ornate
  phrasing, high-temperature sampling or a paraphrase pass looks "surprising"
  to gpt2.
- **It only reads the first 400 tokens.** If a human writes the opening and AI
  writes the rest, the AI part is never scored.
- **gpt2 is small and old.** What gpt2 finds predictable is not necessarily
  what a modern model writes. Technical vocabulary also raises perplexity
  whoever wrote the text.

### Signal two — the style signal

**What it measures:** The shape of the text without its meaning. It combines
three measures: how much sentence length varies (standard deviation over
mean), how much vocabulary repeats (type-token ratio), and how much and what
kind of punctuation is used. The result is a 0–1 score where higher means more
likely AI.

**Why that might differ between human and AI writing:** Generated prose tends
towards even, mid-length sentences and a narrower vocabulary. Human writing is
lumpier, with a three-word sentence next to a forty-word one.

**What it can't see:** Anything about content. It cannot read:
- **Cheap surface edits move it.** Adding typos raises vocabulary variety,
  chopping or merging sentences changes the spread, and pasting in a quotation
  or some dashes changes the punctuation. None of these change who wrote the
  text.
- **Length distorts it.** Type-token ratio falls as text gets longer, so a long
  human essay can look "repetitive". A one- or two-sentence submission has no
  spread to measure at all.
- **Its assumptions can be backwards.** Modern AI uses em dashes and
  semicolons heavily, so punctuation variety may point the wrong way. Poetry,
  lists, dialogue and code break the sentence splitter.
- **It shares signal one's worst blind spot.** A plain human writer with even
  sentences and a small vocabulary scores as AI here too. The two signals are
  *not* independent on the case that matters most: the false positive (see
  [DESIGN.md](DESIGN.md#tracing-the-false-positive)). When both are wrong,
  combining them does not cancel the error.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take a weighted average that counts the model signal more than
the style signal. Then, if the two signals disagree strongly *and* the average
leans AI, pull the score halfway back toward 0.5. One signal alone can't
accuse anyone. On the human side the score is left alone, because a wrong
"human" is the cheap mistake. Gaming the style signal down can't earn a
"human" label either, because the model's 0.6 weight keeps AI text above 0.5.

**The numbers:** (all in `config.py`)
- Weights: model **0.6**, style **0.4**. Style is weighted lower because it's
  the cheapest signal to game. In calibration, adding one three-word sentence
  to AI text moved its sentence-spread measure from fully AI to fully human.
- Disagreement: a gap of more than **0.4** between the signals, with an
  average above 0.5, gets a pull of **0.5** (halfway) toward 0.5.
- Thresholds: **≤ 0.40 human**, **≥ 0.80 AI**, and unsure in between.

How the style signal is built (`stylometry.py`): three measures, each mapped
onto 0–1 between two anchor values and averaged equally.
- **Sentence-length spread** (standard deviation over mean): low means AI.
- **Type-token ratio** (moving average over 50-word windows): *high* means AI.
  That is the opposite of the starter's guess, because AI text scored 0.77–0.88
  and human text 0.74–0.87. It's weak and based on few samples.
- **Within-sentence punctuation per word:** low means AI.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**The calibration run** (`python calibrate.py`, where every text's source is
listed):

```
input               words  spread    ttr  punct   style  model  combined  guess
-------------------------------------------------------------------------------
clearly AI             81   0.141  0.879  0.049   0.922  0.883     0.898  ai
clearly human         112   0.169  0.754  0.107   0.451  0.583     0.530  unsure
formal human           89   0.712  0.782  0.146   0.115  0.557     0.380  human
lightly-edited AI      87   0.665  0.920  0.058   0.594  0.800     0.718  unsure
plain human-style      50   0.234  0.740  0.000   0.675  0.836     0.771  unsure
AI: essay              76   0.210  0.881  0.118   0.631  0.957     0.826  ai
AI: casual             78   0.185  0.822  0.038   0.856  0.851     0.853  ai
AI: review             68   0.152  0.831  0.088   0.670  0.877     0.795  unsure
AI: explainer          73   0.078  0.765  0.055   0.688  0.920     0.827  ai
human: terse note      71   0.553  0.873  0.056   0.587  0.141     0.320  human

thresholds: human <= 0.4, ai >= 0.8
```

Where they **agree**: on clear AI text both are high (0.88 / 0.92). On the
plain human-style paragraph both are *also* high (0.84 / 0.68). That is the
shared blind spot, and no combining rule can fix agreement. The high AI
threshold is what keeps that paragraph at unsure (0.771), and the margin is
only 0.03.

**A case where my two signals split, and what my rule does with it:**
The *formal human* text (the Python `decimal` module docs). Signal one says
0.56, close to a coin flip: technical vocabulary and an ordinary register. The
style signal says 0.11, clearly human: long and short sentences mixed, with
parentheses, quotes and a semicolon. The gap is 0.44, which counts as strong
disagreement. The average (0.38) leans human, so the rule leaves it alone and
it's labelled human. If the split ran the other way, with the model high and
the style low on a text averaging above 0.5, the rule would pull it toward 0.5
and it would land on unsure.

The opposite split showed me the first version of the rule was wrong. The
course staff's terse note scored model 0.14 and style 0.59. Pulling *both*
directions dragged it from 0.32 to 0.41, and no text could reach the human
label. That's why the pull is now one-sided.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.40 | We think this was probably written by a person. No automated check can be certain, so "probably" is the strongest thing we ever say. |
| unsure | 0.40 – 0.80 | We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result. |
| high-confidence AI | 0.80 – 1.00 | This writing has a lot in common with text produced by AI tools, so we think it may have been written with one. Automated checks like ours can be wrong, especially on plain, straightforward writing. If you wrote this yourself, ask for a review using the submission ID shown with this result, and a person will look at it. Nothing is removed while you wait. In your request, tell us how you wrote it; mentioning drafts or notes you could share helps. |

The ranges come from `scoring.label_ranges()`, and the text lives in
`scoring.py::LABELS`. All three were reached through `/submit`: the course
staff's terse note scored 0.32 (human), the plain paragraph 0.77 (unsure) and
the clearly-AI paragraph 0.90 (AI).

**Why I worded the "unsure" one this way:**
On a text this service can't call, the most likely reader is the plain writer
from my false-positive trace. The plain paragraph lands in exactly this band,
at 0.77. So the label does three things:
- It names the reason *their kind of writing* lands here, so it doesn't feel
  like a verdict on them personally.
- It says outright that nothing happens because of the result.
- It gives them a way to ask for a review anyway.

**How I tested the wording:** I gave all three labels, with no explanation of
how the system works, to a fresh Claude session. I asked it to answer as the
writer: what each label is saying about them, and what they'd do next. What it
heard, and what I changed:
- **Human label:** "probably" made it uneasy ("why only fairly sure?"). I added
  that "probably" is the strongest thing we ever say, so it doesn't read as
  doubt about them.
- **Unsure label:** it believed it wasn't being accused. It still wondered
  whether the result counts against it, and said it would appeal "just to
  clear it up". I added "we take no action on your work because of it".
- **AI label:** "my stomach would drop". It wanted to know what happens to its
  work meanwhile, and whether drafts would help. I added "Nothing is removed
  while you wait" and the advice about drafts. I left out a review timeline,
  because this service has none and I won't promise one.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

This is the plain, human-style paragraph from my false-positive trace. Signal
one alone scores it 0.84, almost as AI-like as obvious AI text. The combined
score of 0.77 keeps it just under the AI line, so it lands on unsure.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I started working at the library last summer. At first I did not like it very much. The work was quiet and I did not know anyone. After a few weeks I made some friends and I started to enjoy it. Now I look forward to my shifts every week.", "creator_id": "carol"}'
```

```json
{
    "confidence": 0.7714,
    "content_id": "987f7ffe-ddd3-46ff-afb7-3820ca6ad2ca",
    "creator_id": "carol",
    "guess": "unsure",
    "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
    "model_score": 0.8357,
    "status": "decided",
    "style_score": 0.675
}
```

**A rejected submission** (too short), which is still logged:

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "", "creator_id": "eval"}'
```

```json
{"error":"text_too_short","message":"That's too short to judge fairly. Send at least 25 words.","min_words":25}
```
HTTP 422.

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "987f7ffe-ddd3-46ff-afb7-3820ca6ad2ca", "reasoning": "I wrote this myself for my English class. I keep my sentences simple on purpose because English is my second language. I have my first draft in Google Docs with the edit history."}'
```

```json
{
    "appealed_at": "2026-11-16T00:11:46+00:00",
    "content_id": "987f7ffe-ddd3-46ff-afb7-3820ca6ad2ca",
    "message": "Your appeal has been recorded. A person will review this decision; until then it's marked as under review.",
    "original_guess": "unsure",
    "status": "under_review"
}
```

**What the log shows afterwards**

The original decision is untouched, and the appeal sits right after it with
the new status. The `creator_id` on the appeal is copied from the decision,
not taken from the request.

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
    "count": 2,
    "entries": [
        {
            "combined_score": 0.7714,
            "content_id": "987f7ffe-ddd3-46ff-afb7-3820ca6ad2ca",
            "creator_id": "carol",
            "guess": "unsure",
            "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
            "model_score": 0.8357,
            "status": "decided",
            "style_score": 0.675,
            "timestamp": "2026-11-16T00:11:38+00:00"
        },
        {
            "content_id": "987f7ffe-ddd3-46ff-afb7-3820ca6ad2ca",
            "creator_id": "carol",
            "event": "appeal",
            "reasoning": "I wrote this myself for my English class. I keep my sentences simple on purpose because English is my second language. I have my first draft in Google Docs with the edit history.",
            "status": "under_review",
            "timestamp": "2026-11-16T00:11:46+00:00"
        }
    ]
}
```

**Appeals that are refused** (none of them writes an appeal entry):

| Request | Status | `error` |
|---|---|---|
| A second appeal on the same id | 409 | `already_under_review` |
| The real id with its last character changed | 404 | `unknown_content_id` |
| `"content_id": "not-a-real-id"` | 404 | `unknown_content_id` |
| `"content_id": ""` | 400 | `invalid_field` |
| No `reasoning` | 400 | `missing_field` |
| `[1,2]` as the body | 400 | `invalid_json` |

Afterwards, `audit.entries_for(id)` returned exactly 2 entries: the decision
and the appeal.

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
