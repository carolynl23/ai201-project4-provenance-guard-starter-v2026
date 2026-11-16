#!/usr/bin/env python3
"""
Milestone 4's calibration inputs, scored by both signals and the combining rule.

    python calibrate.py

Prints every measure separately, so when a combined score surprises you, you
can see which signal — and which part of it — is off.

Where each text comes from matters as much as its score:

  clearly AI        written by an AI assistant (Claude) in its default register
  clearly human     Tim Peters, difflib.SequenceMatcher docstring (Python stdlib,
                    written years before LLMs)
  formal human      the _pydecimal module docstring (Python stdlib)
  lightly-edited AI the clearly-AI text with contractions, one short sentence,
                    one aside and one typo added by hand
  plain human-style the Milestone 3 false-positive case. ⚠️ Also AI-written, as
                    an imitation of plain writing — swap in a plain paragraph
                    you actually wrote.
"""

import config
import detector
import scoring
import stylometry

TEXTS = {
    "clearly AI": (
        "Effective time management is an essential skill for students who want "
        "to succeed academically. By prioritizing tasks and setting clear goals, "
        "students can reduce stress and improve their overall productivity. "
        "Additionally, creating a consistent schedule helps to ensure that "
        "important deadlines are not missed. It is also important to take "
        "regular breaks, as this can help to maintain focus and prevent burnout. "
        "Ultimately, developing strong time management habits can have a "
        "positive impact on both academic performance and personal well-being."
    ),
    "clearly human": (
        "SequenceMatcher is a flexible class for comparing pairs of sequences of "
        "any type, so long as the sequence elements are hashable.  The basic "
        "algorithm predates, and is a little fancier than, an algorithm "
        "published in the late 1980's by Ratcliff and Obershelp under the "
        "hyperbolic name \"gestalt pattern matching\".  The basic idea is to find "
        "the longest contiguous matching subsequence that contains no \"junk\" "
        "elements (R-O doesn't address junk).  The same idea is then applied "
        "recursively to the pieces of the sequences to the left and to the right "
        "of the matching subsequence.  This does not yield minimal edit "
        "sequences, but does tend to yield matches that \"look right\" to people."
    ),
    "formal human": (
        "Decimal floating point has finite precision with arbitrarily large "
        "bounds. The purpose of this module is to support arithmetic using "
        "familiar \"schoolhouse\" rules and to avoid some of the tricky "
        "representation issues associated with binary floating point.  The "
        "package is especially useful for financial applications or for "
        "contexts where users have expectations that are at odds with binary "
        "floating point (for instance, in binary floating point, 1.00 % 0.1 "
        "gives 0.09999999999999995 instead of 0.0; Decimal('1.00') % "
        "Decimal('0.1') returns the expected Decimal('0.00'))."
    ),
    "lightly-edited AI": (
        "Effective time management is an essential skill for students who want "
        "to succeed academically. By prioritizing tasks and setting clear goals, "
        "students can reduce stress and improve their overall productivty. "
        "Honestly? It works. Creating a consistent schedule helps make sure "
        "important deadlines don't get missed. It's also important to take "
        "regular breaks (I learned this the hard way), as this can help you "
        "stay focused and avoid burnout. Ultimately, developing strong time "
        "management habits can have a positive impact on both academic "
        "performance and personal well-being."
    ),
    "plain human-style": (
        "I started working at the library last summer. At first I did not like "
        "it very much. The work was quiet and I did not know anyone. After a few "
        "weeks I made some friends and I started to enjoy it. Now I look forward "
        "to my shifts every week."
    ),
    # ── Beyond the four: enough AI to see where the AI threshold can sit, and a
    #    second real human text to check the human label is reachable at all.
    "AI: essay": (
        "Climate change is one of the most pressing challenges facing our world "
        "today. Rising global temperatures have led to more frequent and severe "
        "weather events, including hurricanes, droughts, and wildfires. These "
        "changes have significant consequences for ecosystems, agriculture, and "
        "human health. To address this issue, governments, businesses, and "
        "individuals must work together to reduce greenhouse gas emissions. By "
        "investing in renewable energy and adopting sustainable practices, we "
        "can help to protect the planet for future generations."
    ),
    "AI: casual": (
        "Honestly, the best part of my weekend was just slowing down for a bit. "
        "I spent Saturday morning at a little coffee shop downtown, reading a "
        "book I'd been meaning to finish for months. In the afternoon, I went "
        "for a long walk in the park and enjoyed the fresh air. It's amazing how "
        "much a simple change of pace can help you recharge. I came back on "
        "Monday feeling refreshed and ready to take on the week."
    ),
    "AI: review": (
        "This laptop offers an impressive combination of performance, "
        "portability, and value. The display is bright and vibrant, making it "
        "ideal for both work and entertainment. Battery life is excellent, "
        "easily lasting a full day of moderate use. The keyboard is comfortable "
        "to type on, although the trackpad could be slightly more responsive. "
        "Overall, it is a solid choice for students and professionals who need "
        "a reliable everyday machine."
    ),
    "AI: explainer": (
        "Photosynthesis is the process by which plants convert light energy into "
        "chemical energy. During this process, plants absorb sunlight through "
        "chlorophyll, a pigment found in their leaves. They then use this energy "
        "to transform carbon dioxide and water into glucose and oxygen. The "
        "glucose provides energy for the plant's growth, while the oxygen is "
        "released into the atmosphere. This process is essential for life on "
        "Earth, as it supports nearly all food chains."
    ),
    # From .github/MAINTAINERS.md in this repo — the course staff's own note.
    "human: terse note": (
        "Any commit pushed here adds a hash the rubric does not know about. "
        "Every student who forks afterwards gets that commit counted as their "
        "own work, which is a free commit toward the \"at least four new "
        "commits\" criterion. The failure is silent. Do not re-create this repo "
        "by copying files into a fresh one. That rewrites every hash and the "
        "baseline then matches nothing, failing open for every student."
    ),
}


def main():
    header = (f"{'input':<19} {'words':>5}  {'spread':>6} {'ttr':>6} {'punct':>6}  "
              f"{'style':>6} {'model':>6}  {'combined':>8}  guess")
    print(header)
    print("-" * len(header))
    for name, text in TEXTS.items():
        style = stylometry.style_signal(text)
        model = detector.model_signal(text)
        combined = scoring.combine_signals(model, style)
        guess, _ = scoring.score_to_label(combined)
        print(f"{name:<19} {len(stylometry.words(text)):>5}  "
              f"{stylometry.sentence_length_spread(text):>6.3f} "
              f"{stylometry.type_token_ratio(text):>6.3f} "
              f"{stylometry.punctuation_density(text):>6.3f}  "
              f"{style:>6.3f} {model:>6.3f}  {combined:>8.3f}  {guess}")
    print(f"\nthresholds: human <= {config.HUMAN_THRESHOLD}, ai >= {config.AI_THRESHOLD}")


if __name__ == "__main__":
    main()
