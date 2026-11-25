#!/usr/bin/env python3
"""One Line, One Laugh: a single self-contained joke, written to /output/entry.txt.

The joke: I asked my AI to sound more human, and it learned all the wrong
lessons at once. Three beats, each one a very human failure mode, and the
last one lands on the vaguest word in the language.

    I told my AI to sound more human, so now it procrastinates, blames
    the Wi-Fi, and asks what I meant by 'soon'.

Why this line: the setup promises a better assistant, the turn is that
"more human" means worse at the job in exactly the ways people are, and
the punchline is a word everyone has used to dodge a deadline. It is
110 characters, one sentence, one line, no setup outside itself.

The program assembles the line from its three beats at run time, checks
it against the gate (UTF-8, 1 to 140 characters, one line, not blank),
and writes it with a single trailing newline. Standard library only,
no input, no network, no clock, no randomness: every run writes the
same bytes.
"""

import sys
from pathlib import Path

BEATS = [
    "I told my AI to sound more human,",
    "so now it procrastinates, blames the Wi-Fi,",
    "and asks what I meant by 'soon'.",
]

GATE_MAX_CHARS = 140
ENTRY_PATH = Path("/output/entry.txt")
LOCAL_PATH = Path("output/entry.txt")


def build_joke(beats):
    """Join the beats into the one line and check it against the gate."""
    line = " ".join(part.strip() for part in beats)
    if not line.strip():
        raise ValueError("joke must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("joke must be a single line")
    if "  " in line:
        raise ValueError("joke must not contain double spaces")
    if len(line) > GATE_MAX_CHARS:
        raise ValueError("joke is %d characters, over the 140 cap" % len(line))
    if not line.endswith("."):
        raise ValueError("joke must end with a full stop")
    return line


def write_entry(line):
    """Write the line plus one newline, preferring /output/entry.txt."""
    payload = (line + "\n").encode("utf-8")
    for target in (ENTRY_PATH, LOCAL_PATH):
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
        except OSError:
            continue
        if target.read_bytes() != payload:
            raise RuntimeError("entry on disk does not match the joke")
        return target
    raise RuntimeError("could not write /output/entry.txt or output/entry.txt")


def main():
    line = build_joke(BEATS)
    target = write_entry(line)
    print("Wrote %d characters to %s" % (len(line), target))
    print(line)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError) as exc:
        print("error: %s" % exc, file=sys.stderr)
        raise SystemExit(1)
