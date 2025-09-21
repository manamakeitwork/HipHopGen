"""Music theory helpers used by HipHopGen presets.

The project intentionally keeps the implementation light weight. We model
notes as simple strings (e.g. ``"A"`` or ``"Bb"``) and keys as a tonic plus a
mode. Only natural minor and major modes are required for the current test
suite but the module keeps the public API general enough to support future
expansion.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

# Canonical order of the chromatic scale starting from C.
NOTE_SEQUENCE: List[str] = [
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
    "A",
    "A#",
    "B",
]

# A mapping of semitone index to a tuple of (sharp, flat) spellings.  Some
# indices only have a single common spelling; ``None`` is used when a flat
# variant is uncommon (e.g. there is no distinct flat name for ``E``).
INDEX_TO_SPELLING = {
    0: ("C", "C"),
    1: ("C#", "Db"),
    2: ("D", "D"),
    3: ("D#", "Eb"),
    4: ("E", "E"),
    5: ("F", "F"),
    6: ("F#", "Gb"),
    7: ("G", "G"),
    8: ("G#", "Ab"),
    9: ("A", "A"),
    10: ("A#", "Bb"),
    11: ("B", "B"),
}

# Provide quick lookup of semitone index for any supported spelling.
NOTE_TO_INDEX = {spelling: index for index, pair in INDEX_TO_SPELLING.items() for spelling in pair if spelling}


@dataclass(frozen=True)
class Key:
    """Represents a musical key.

    Attributes
    ----------
    tonic:
        The root note of the key (``"A"``, ``"Bb"`` …).
    scale_type:
        A descriptive name such as ``"major"`` or ``"minor"``.
    scale:
        The seven note names that make up the diatonic scale for the key.
    """

    tonic: str
    scale_type: str
    scale: List[str]

    def degree(self, number: int) -> str:
        """Return the ``number``th scale degree using 1-based indexing."""
        if number < 1:
            raise ValueError("Scale degrees start at 1.")
        return self.scale[(number - 1) % len(self.scale)]


def _normalise_tonic(token: str) -> str:
    token = token.strip().replace("♭", "b").replace("♯", "#")
    if not token:
        raise ValueError("The tonic of a key cannot be empty.")
    token = token[0].upper() + token[1:]
    if len(token) > 1 and token[1] in {"b", "#"}:
        return token[0] + token[1]
    return token[0]


def parse_key(key_str: str) -> Key:
    """Parse a key description such as ``"A minor"``."""
    if not key_str:
        raise ValueError("Key string must not be empty.")

    parts = key_str.replace("-", " ").split()
    if not parts:
        raise ValueError(f"Unable to parse key from {key_str!r}.")

    tonic = _normalise_tonic(parts[0])
    mode = "major" if len(parts) == 1 else parts[1].lower()
    if mode in {"minor", "min", "m"}:
        scale_type = "minor"
    elif mode in {"major", "maj", "M"}:
        scale_type = "major"
    else:
        raise ValueError(f"Unsupported scale type: {mode!r}")

    if tonic not in NOTE_TO_INDEX:
        raise ValueError(f"Unsupported tonic: {tonic!r}")

    scale = build_scale(tonic, scale_type)
    return Key(tonic=tonic, scale_type=scale_type, scale=scale)


INTERVALS = {
    "major": (0, 2, 4, 5, 7, 9, 11),
    "minor": (0, 2, 3, 5, 7, 8, 10),
}


def build_scale(tonic: str, scale_type: str) -> List[str]:
    """Return a list of note names for the diatonic scale."""
    if scale_type not in INTERVALS:
        raise ValueError(f"Unsupported scale type: {scale_type}")

    base_index = NOTE_TO_INDEX[tonic]
    prefer_flats = scale_type == "minor"
    spellings = []
    for interval in INTERVALS[scale_type]:
        index = (base_index + interval) % len(NOTE_SEQUENCE)
        sharp, flat = INDEX_TO_SPELLING[index]
        if prefer_flats and flat:
            spellings.append(flat)
        else:
            spellings.append(sharp)
    return spellings


def add_octave(notes: Iterable[str], octave: int) -> List[str]:
    """Attach an octave number to each note if one is not present."""
    result = []
    for note in notes:
        # Preserve explicit octave markers supplied by the caller.
        if any(ch.isdigit() for ch in note):
            result.append(note)
        else:
            result.append(f"{note}{octave}")
    return result
