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

**The rule:**

**The numbers:**

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

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
