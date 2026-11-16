"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

# Window for moving-average type-token ratio. Short enough that a 60-word
# submission gets a few windows; long enough that "the" repeating isn't
# the whole story.
TTR_WINDOW = 50


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies. ← TODO

    Returns:
        A float. Decide yourself what scale it's on and which direction means
        "more human" — then write that down, because your combining rule
        depends on knowing it.

    A hint on what you're reaching for: the standard deviation of sentence
    lengths, probably divided by the mean so a long text and a short one are
    comparable. `statistics.stdev` is imported for you.

    Watch the edge case: a one-sentence submission has no spread at all, and
    `stdev` raises on fewer than two values. Decide what that should return
    before the attack set decides for you.

    Mine: coefficient of variation (stdev / mean) of words per sentence.
    0.0 means every sentence is the same length; human prose usually lands
    0.4–0.8. **Higher means more human.** Fewer than two sentences returns
    0.0 — and `style_signal` treats that case as "no evidence", not as AI.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    mean = statistics.mean(lengths)
    return round(statistics.stdev(lengths) / mean, 4)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words. ← TODO

    Returns:
        A float between 0 and 1. Higher means more varied vocabulary.

    Worth knowing before you rely on it: this measure falls as text gets
    longer, because common words repeat. Two texts of different lengths aren't
    directly comparable on it, and if your test inputs vary a lot in length,
    that alone can look like a signal.

    Mine: moving-average TTR — plain TTR over every 50-word window, averaged —
    so a 300-word essay and a 60-word paragraph are on the same footing.
    Under 50 words it falls back to plain TTR. **Higher means more human.**
    """
    toks = words(text)
    if not toks:
        return 0.0
    if len(toks) <= TTR_WINDOW:
        return round(len(set(toks)) / len(toks), 4)
    ratios = [
        len(set(toks[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(toks) - TTR_WINDOW + 1)
    ]
    return round(statistics.mean(ratios), 4)


def punctuation_density(text: str) -> float:
    """
    How much punctuation, relative to length. ← TODO

    Returns:
        A float. Whether you count all punctuation or only some kinds — commas,
        semicolons, dashes — is a real choice. Semicolons and em dashes are
        more interesting than full stops, because they vary more between
        writers.

    Mine: marks *inside* sentences — commas, semicolons, colons, dashes,
    brackets, quotes — per word. Full stops are left out because every
    sentence has one, so they only measure sentence count, which spread
    already covers. Direction is not obvious; see `style_signal`.
    """
    toks = words(text)
    if not toks:
        return 0.0
    marks = len(re.findall(r"[,;:()\[\]\"—–]|--| - ", text))
    return round(marks / len(toks), 4)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.

    Mine: each measure is mapped onto 0–1 "AI-ness" by a clipped straight
    line between two anchor values (STYLE_ANCHORS), then the three are
    averaged with equal weight. The anchors come from `python calibrate.py`.

      spread  low  -> AI   (even, marching sentences)
      ttr     HIGH -> AI   ⚠️ the opposite of the starter's guess. On my
                           calibration set the AI text scored 0.88 and every
                           human text 0.74–0.78: modern models reach for
                           varied, polished words, people repeat their topic
                           words. Five samples, so recheck on your own ten.
      punct   low  -> AI   (no brackets, quotes, semicolons)

    A one-sentence text has no spread, so that measure sits at 0.5 — no
    evidence either way — rather than reading as "perfectly even".
    """
    parts = []
    for name, value in (
        ("spread", sentence_length_spread(text)),
        ("ttr", type_token_ratio(text)),
        ("punct", punctuation_density(text)),
    ):
        if name == "spread" and len(sentences(text)) < 2:
            parts.append(0.5)
            continue
        at_human, at_ai = STYLE_ANCHORS[name]
        parts.append(_scale(value, at_human, at_ai))
    return round(sum(parts) / len(parts), 4)


# The raw value at which each measure reads fully human (0.0) and fully AI
# (1.0). Between them the score moves in a straight line; outside, it clips.
STYLE_ANCHORS = {
    "spread": (0.60, 0.20),
    "ttr": (0.72, 0.90),
    "punct": (0.12, 0.04),
}


def _scale(value: float, at_human: float, at_ai: float) -> float:
    """Map `value` onto 0 (at_human) … 1 (at_ai), clipped. Works either direction."""
    position = (value - at_human) / (at_ai - at_human)
    return min(max(position, 0.0), 1.0)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")
