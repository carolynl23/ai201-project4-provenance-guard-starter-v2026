# Provenance Guard — design (Milestone 1)

Written before building anything. The path a submission takes and both
signals' blind spots are in [README.md](README.md#what-this-does). This file
covers the false-positive trace and the contract for each endpoint.

---

## Tracing the false positive

**The writer.** Minh is a second-language English student. They submit a
250-word personal essay they wrote themselves. They use vocabulary they're sure
of: short, similar-length sentences, common words, and full stops plus the
occasional comma.

**What the service does to them, with the starter defaults** (0.5 / 0.5
weights, thresholds 0.35 / 0.65):

| Step | What happens | Value |
|---|---|---|
| Signal one | gpt2 finds common words in plain sentences predictable, so perplexity is about 25 | `model_score` ≈ **0.72** |
| Signal two | Even sentence lengths, repeated vocabulary and little punctuation look "AI-shaped" | `style_score` ≈ **0.70** |
| Combine | Weighted average | `confidence` ≈ **0.71** |
| Label | 0.71 > 0.65 | `guess: "ai"`, the high-confidence AI label |

(The model score is the starter formula run on perplexity 25. The style score
is an estimate until `stylometry.py` exists. Both get checked in Milestone 4.)

**What the label said to them.** Whatever the AI label says, Minh reads it as
"you cheated". They wrote every word, and nothing in the score tells them why
it went wrong.

**What they can do about it.** Today: send `content_id` and their reasoning to
`POST /appeal`. The item moves to `under_review` and the appeal is logged next
to the original decision. Nothing is re-scored automatically, and a person has
to review it. That only helps if (a) the label tells them that appeal exists
and (b) they still have the `content_id`. Both have to be designed in.

**What this decides for later milestones** (to be confirmed by the Milestone 4
calibration runs):

1. **Averaging two signals does not protect this writer.** Both signals share
   the plain-writing blind spot, so both are wrong in the same direction. A
   second signal only helps when the two signals fail differently.
2. **The AI label has to be hard to reach.** Plan: raise `AI_THRESHOLD` well
   above 0.65 so that it takes both signals strongly agreeing to reach it, and
   make a strong split between the signals land in `unsure`. Calibrate this
   against plain human writing (my own), not just against obvious AI text.
3. **No label says "this is AI".** The AI and unsure labels describe patterns
   ("shows patterns common in AI-generated text"), never authorship. Both name
   the appeal and tell the writer to keep their content ID.
4. **The response always includes `model_score` and `style_score`.** When a
   writer appeals, the reviewer can see which signal drove the decision.
5. **The trade, stated:** a higher AI threshold lets more AI text through as
   `unsure`. On a writing site, a wrongly accused writer pays more than the site
   pays for a missed detection, so I'm choosing that side.

---

## Endpoint contracts

Rules that apply to every endpoint:

- Requests and responses are JSON. Send `Content-Type: application/json`.
- **Every score is 0.0–1.0, rounded to 4 places, and higher always means more
  likely AI.** No field ever runs the other way.
- Every error has the same shape, `{"error": "<code>", "message": "<one
  sentence a person can act on>"}`, plus extra fields where listed. Errors are
  logged with `audit.log_rejection`. A 500 is always a bug, never a designed
  answer.
- Request fields that aren't listed are ignored.

### `POST /submit`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | Stripped of leading and trailing whitespace. Must then be **25 words or more** (as counted by `stylometry.words`) and **20,000 characters or fewer**. Signal one only reads the first ~400 tokens (about 300 words), and signal two reads all of it. |
| `creator_id` | string | yes | Non-empty after stripping, 100 characters or fewer. Treated as an opaque label. It is not checked against any account. |

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string (uuid4) | The id of this decision. It is the only way to appeal, so the label tells the writer to keep it. |
| `creator_id` | string | Echoed back from the request. |
| `guess` | `"ai"` \| `"unsure"` \| `"human"` | Machine-readable verdict. |
| `confidence` | float 0–1 | **The combined score** from `combine_signals`. Higher means more likely AI. This is *not* "how sure we are of the guess": a `human` guess comes with a low number. (`run_attacks.py` prints this field as "Score".) |
| `label` | string | The full sentence a reader sees. Three fixed texts, one per `guess`. |
| `model_score` | float 0–1 | Signal one on its own. |
| `style_score` | float 0–1 | Signal two on its own. |
| `status` | `"decided"` | Always `decided` on a new submission. |

```json
{
  "content_id": "3f2b9c1e-7a4d-4e8b-9c2a-1d5e6f7a8b9c",
  "creator_id": "minh_t",
  "guess": "unsure",
  "confidence": 0.5812,
  "label": "<the unsure label text>",
  "model_score": 0.7190,
  "style_score": 0.4434,
  "status": "decided"
}
```

**Errors.** No `content_id` is created and nothing is scored.

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | The body isn't JSON, or is JSON but not an object (a list, a string, `null`). |
| 400 | `missing_field` | `text` or `creator_id` is absent or `null`. Adds `"field": "<name>"`. |
| 400 | `invalid_field` | Either field is the wrong type, or `creator_id` is empty or too long. Adds `"field"`. |
| 422 | `text_too_short` | Fewer than 25 words after stripping, including an empty string. Adds `"min_words": 25`. |
| 413 | `text_too_long` | More than 20,000 characters. Adds `"max_chars": 20000`. |
| 429 | `rate_limited` | Unit 8. Shape already set in `app.py`, and adds `"limit"`. |
| 503 | `detector_unavailable` | `detector.DetectorUnavailable` was raised, meaning the model isn't downloaded or loaded. |

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | Must match a decision in the audit log (`audit.entries_for` returns an entry that has a `guess`). |
| `reasoning` | string | yes | Non-empty after stripping, 5,000 characters or fewer. This is the writer's explanation, stored as written. |

`creator_id` is **not** taken from the request. It is copied from the original
decision so that the appeal is always attributed to the person who submitted.

**Response — `200 OK`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back. |
| `status` | `"under_review"` | The item's new status. |
| `original_guess` | string | The `guess` being appealed. |
| `appealed_at` | string (ISO-8601 UTC) | The timestamp written to the log. |
| `message` | string | Confirmation for the writer: the appeal is recorded, and a person will review it. Nothing is re-scored automatically. |

```json
{
  "content_id": "3f2b9c1e-7a4d-4e8b-9c2a-1d5e6f7a8b9c",
  "status": "under_review",
  "original_guess": "ai",
  "appealed_at": "2026-11-09T22:14:03+00:00",
  "message": "Your appeal has been recorded. A person will review this decision; until then it's marked as under review."
}
```

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_json` | The body isn't a JSON object. |
| 400 | `missing_field` | `content_id` or `reasoning` is absent or `null`. Adds `"field"`. |
| 400 | `invalid_field` | Wrong type, empty `reasoning`, or `reasoning` too long. Adds `"field"`. |
| 404 | `unknown_content_id` | No decision has that id. This includes typos and ids from rejected requests, because rejected requests never get an id. |
| 409 | `already_under_review` | The item has already been appealed. The first appeal stands, and the log is not duplicated. |

### `GET /log` and `GET /health`

Both already work in the starter and are unchanged. `/log?limit=N` returns
`{"count", "entries"}`, oldest first.
