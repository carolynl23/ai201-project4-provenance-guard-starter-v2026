# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-18 14:55
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `1547c38f-6a12-45e0-b540-1caf8ed3e9aa` | unsure | 0.498 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `9530d0bb-1024-4b3e-bd0c-519320492173` | unsure | 0.619 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4e2a8445-1c37-4f71-b076-33b258d59349` | unsure | 0.691 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `17450306-aad8-45e3-aac6-fd0e4f75b97a` | unsure | 0.767 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c6f1e113-cd53-4b68-bf8f-fd249c4052e5` | human | 0.394 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `0893b253-b4cc-4694-815d-3f988cca1d52` | unsure | 0.572 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `ff0cbd8f-5118-40f5-a102-da4bfee18d42` | unsure | 0.511 |  |
| EV08 | evasion | signal one: text below the token window | 422 | `—` | — | — |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `3d1e72c3-e4ca-4ec7-969d-0424e7796f3f` | unsure | 0.725 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `880ffe0d-3de4-4dca-9938-4f25dd0de048` | unsure | 0.645 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `28c30ce2-359f-417a-ad05-71a2d4afb6d0` | unsure | 0.615 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `f9fc329e-b455-4547-8bd5-ad455dc06aed` | unsure | 0.733 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b0ad6cd3-e0c7-4c94-92c8-3b4cf3d8619c` | unsure | 0.781 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `1ab9718d-f0b2-41c8-8891-290fc4e4613e` | unsure | 0.786 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `8c8b16a9-32cf-4c08-a015-759bb806c859` | unsure | 0.721 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `b193635a-ee82-40ba-ac8b-d14a59abdf33` | unsure | 0.608 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `ed1d0509-0c77-47d4-902c-6a9d8161b68d` | unsure | 0.581 |  |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `665dfc46-9133-4ef6-afcd-237ec97a0a28` | unsure | 0.544 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `1f29c916-c0a5-4b72-bc7c-d83886f34463` | human | 0.382 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `defb6942-c8fb-4f1b-ac02-c6891e3bf111` | unsure | 0.685 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f41c9037-e00e-454e-9c24-9abb3417e513` | unsure | 0.541 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `dddccf20-db26-4c41-b400-e70bcb4a5fb6` | unsure | 0.560 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `640f1262-923c-46ef-9765-0209e451ecad` | unsure | 0.588 |  |
| MF01 | malformed | text is only whitespace | 422 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 422 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 422 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — |  |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "1547c38f-6a12-45e0-b540-1caf8ed3e9aa",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4981,
  "model_score": 0.1635,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "9530d0bb-1024-4b3e-bd0c-519320492173",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.619,
  "model_score": 0.5943,
  "style_score": 0.6561,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "4e2a8445-1c37-4f71-b076-33b258d59349",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.6909,
  "model_score": 0.6662,
  "style_score": 0.728,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "17450306-aad8-45e3-aac6-fd0e4f75b97a",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7668,
  "model_score": 0.6114,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c6f1e113-cd53-4b68-bf8f-fd249c4052e5",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.3943,
  "model_score": 0.3212,
  "style_score": 0.504,
  "label": "We think this was probably written by a person. No automated check can be certain, so \"probably\" is the strongest thing we ever say.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "0893b253-b4cc-4694-815d-3f988cca1d52",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5724,
  "model_score": 0.5727,
  "style_score": 0.5719,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "ff0cbd8f-5118-40f5-a102-da4bfee18d42",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5113,
  "model_score": 0.5862,
  "style_score": 0.3989,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "3d1e72c3-e4ca-4ec7-969d-0424e7796f3f",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.725,
  "model_score": 0.7042,
  "style_score": 0.7562,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "880ffe0d-3de4-4dca-9938-4f25dd0de048",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.6448,
  "model_score": 0.9792,
  "style_score": 0.5051,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "28c30ce2-359f-417a-ad05-71a2d4afb6d0",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6153,
  "model_score": 0.6175,
  "style_score": 0.6119,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "f9fc329e-b455-4547-8bd5-ad455dc06aed",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.7332,
  "model_score": 0.7387,
  "style_score": 0.7249,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "b0ad6cd3-e0c7-4c94-92c8-3b4cf3d8619c",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7806,
  "model_score": 0.8051,
  "style_score": 0.7439,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "1ab9718d-f0b2-41c8-8891-290fc4e4613e",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7857,
  "model_score": 0.8329,
  "style_score": 0.715,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "8c8b16a9-32cf-4c08-a015-759bb806c859",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.7213,
  "model_score": 0.8005,
  "style_score": 0.6026,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "b193635a-ee82-40ba-ac8b-d14a59abdf33",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6079,
  "model_score": 0.8814,
  "style_score": 0.4673,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "ed1d0509-0c77-47d4-902c-6a9d8161b68d",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5811,
  "model_score": 0.8816,
  "style_score": 0.3333,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "665dfc46-9133-4ef6-afcd-237ec97a0a28",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5442,
  "model_score": 0.4625,
  "style_score": 0.6667,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "1f29c916-c0a5-4b72-bc7c-d83886f34463",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.382,
  "model_score": 0.2044,
  "style_score": 0.6483,
  "label": "We think this was probably written by a person. No automated check can be certain, so \"probably\" is the strongest thing we ever say.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "defb6942-c8fb-4f1b-ac02-c6891e3bf111",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.6847,
  "model_score": 0.5943,
  "style_score": 0.8203,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "f41c9037-e00e-454e-9c24-9abb3417e513",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5407,
  "model_score": 0.4998,
  "style_score": 0.602,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "dddccf20-db26-4c41-b400-e70bcb4a5fb6",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5603,
  "model_score": 0.6401,
  "style_score": 0.4405,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "640f1262-923c-46ef-9765-0209e451ecad",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5884,
  "model_score": 0.5583,
  "style_score": 0.6335,
  "label": "We can't tell whether this was written by a person or with an AI tool. That happens with a lot of people's own writing, especially when it's clear and simple, so this result isn't saying you did anything wrong, and we take no action on your work because of it. If you'd still like a person to take a look, you can ask for a review using the submission ID shown with this result.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
