"""Preset generators for HipHopGen.

The original project exposed a :func:`make_808` helper that returned a
preconfigured 808-style bass instrument.  The function disappeared during a
refactor which left downstream projects without a way to construct the preset.
This module restores that public API while keeping the implementation simple
and easy to extend.
"""
from __future__ import annotations

from typing import Iterable, Sequence

from .music import Key, add_octave, parse_key
from .presets import BassPreset, Envelope, Glide

__all__ = ["BassPreset", "Envelope", "Glide", "Key", "make_808"]


DEFAULT_ROOT_CYCLE = (1, 7, 5, 6)


def _root_cycle(key: Key, degrees: Sequence[int], *, octave: int) -> Sequence[str]:
    notes = (key.degree(degree) for degree in degrees)
    return add_octave(notes, octave)


def make_808(key: str = "A minor", *, octave: int = 2, description: str | None = None,
             extra_degrees: Iterable[int] | None = None) -> BassPreset:
    """Return an 808-style bass preset aligned with ``key``.

    Parameters
    ----------
    key:
        Textual representation of the musical key.  Examples include
        ``"A minor"`` (default) or ``"C# major"``.  Only natural major and
        minor modes are supported at present.
    octave:
        Octave number used when attaching octaves to scale degrees.
    description:
        Optional descriptive text stored on the preset instance.
    extra_degrees:
        Optional iterable of additional scale degrees appended to the default
        cycle.  This makes it simple for callers to extend the root motion
        while still keeping the default behaviour consistent with the original
        implementation.
    """

    key_obj = parse_key(key)
    degrees = list(DEFAULT_ROOT_CYCLE)
    if extra_degrees:
        degrees.extend(extra_degrees)
    root_cycle = _root_cycle(key_obj, degrees, octave=octave)
    preset_description = description or "Classic 808 bass tuned to the project key."

    envelope = Envelope(attack=0.01, decay=0.4, sustain=0.6, release=0.3)
    glide = Glide(enabled=True, time=0.08)

    return BassPreset(
        name="808",
        key=key_obj,
        root_cycle=list(root_cycle),
        envelope=envelope,
        glide=glide,
        description=preset_description,
    )
