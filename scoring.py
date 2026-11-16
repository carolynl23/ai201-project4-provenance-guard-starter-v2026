"""
Turning two numbers into one, and one number into something a person can read.
← YOU BUILD THIS IN MILESTONES 4 AND 5

Two functions live here, and both are stubs.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Combine two 0–1 signals into one 0–1 score. ← TODO (Milestone 4)

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    ⚠️ **Write the rule down before you code it, and put the numbers in your
    README.** A weighted average is the obvious choice and it is not the only
    one. Things worth thinking about:

      - **What happens when they disagree?** One signal at 0.9 and the other at
        0.1 averages to 0.5 — "unsure". Is that what you want? It might be
        exactly right: two methods disagreeing IS uncertainty. Or you might
        decide one signal is more trustworthy when they split.

      - **Which way do you want to be wrong?** Weighting toward the signal that
        reads more human means fewer false accusations and more AI text
        getting through. There's no weighting that avoids the trade.

      - Milestone 4 asks you to find a case where your two signals split and
        write it down. That case is what this rule exists to handle.

    The weights in config.py are placeholders. Change them, or ignore them and
    write a different rule.

    Mine, in words:

      1. Weighted average — model 0.6, style 0.4.
      2. If the two signals differ by more than DISAGREEMENT_GAP (0.4) AND the
         average leans AI, it's pulled DISAGREEMENT_PULL (halfway) back toward
         0.5. One signal alone can't accuse anyone.

    Why only on the AI side: the expensive mistake is one-sided. A first
    version pulled both ways, and it made the human label unreachable — the
    course staff's own note (model 0.14, style 0.59) got dragged from 0.32 to
    0.41. Gaming the style signal down to earn "human" is already blocked by
    the 0.6 model weight: AI text with model ≈ 0.88 averages above 0.5 even
    with style at 0.
    """
    average = (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
    )
    if average > 0.5 and abs(model_score - style_score) > config.DISAGREEMENT_GAP:
        average = 0.5 + (average - 0.5) * (1 - config.DISAGREEMENT_PULL)
    return round(min(max(average, 0.0), 1.0), 4)


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.
    ← TODO (Milestone 5)

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    ⚠️ Write the label text for someone who has never heard the word
    "threshold".

        ✗ "human, 0.81 confidence"
        ✓ "We think this was probably written by a person."

    All three labels have to be **reachable**. If no score can produce one of
    them, your ranges have a gap — and Milestone 5 asks you to submit text that
    produces each one, which is how you'd find out.

    The hardest one to write is "unsure". It has to admit uncertainty without
    sounding like an accusation, because the person reading it may well have
    written every word themselves. Your breakout asks your group what they'd
    think if they got it on their own work. That question is the whole
    milestone.
    """
    if score >= config.AI_THRESHOLD:
        return "ai", LABELS["ai"]
    if score <= config.HUMAN_THRESHOLD:
        return "human", LABELS["human"]
    return "unsure", LABELS["unsure"]


# The exact text a reader sees. The README's Label Variants table quotes these
# word for word — change one here, change it there.
#
# The AI and unsure labels both say how to ask for a review, and both say
# that plain writing is the kind this check gets wrong — because it is
# (DESIGN.md, "Tracing the false positive").
LABELS = {
    "human": (
        "We think this was probably written by a person. No automated check can "
        "be certain, so \"probably\" is the strongest thing we ever say."
    ),
    "unsure": (
        "We can't tell whether this was written by a person or with an AI tool. "
        "That happens with a lot of people's own writing, especially when it's "
        "clear and simple, so this result isn't saying you did anything wrong, "
        "and we take no action on your work because of it. If you'd still like "
        "a person to take a look, you can ask for a review using the submission "
        "ID shown with this result."
    ),
    "ai": (
        "This writing has a lot in common with text produced by AI tools, so we "
        "think it may have been written with one. Automated checks like ours "
        "can be wrong, especially on plain, straightforward writing. If you "
        "wrote this yourself, ask for a review using the submission ID shown "
        "with this result, and a person will look at it. Nothing is removed "
        "while you wait. In your request, tell us how you wrote it; mentioning "
        "drafts or notes you could share helps."
    ),
}


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f}"),
        ("unsure", f"{config.HUMAN_THRESHOLD:.2f} – {config.AI_THRESHOLD:.2f}"),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00"),
    ]
