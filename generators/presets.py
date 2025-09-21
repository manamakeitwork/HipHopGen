"""Runtime data structures describing synth presets."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from .music import Key


@dataclass(frozen=True)
class Envelope:
    """Simple ADSR-like envelope parameters for a synthesizer."""

    attack: float = 0.005
    decay: float = 0.3
    sustain: float = 0.8
    release: float = 0.4


@dataclass(frozen=True)
class Glide:
    """Represents portamento controls for sliding between notes."""

    enabled: bool = False
    time: float = 0.0


@dataclass(frozen=True)
class BassPreset:
    """Describes an 808-style bass preset."""

    name: str
    key: Key
    root_cycle: List[str]
    envelope: Envelope = field(default_factory=Envelope)
    glide: Glide = field(default_factory=Glide)
    description: str = ""

    def as_dict(self) -> dict:
        """Return a serialisable representation of the preset."""
        return {
            "name": self.name,
            "key": {
                "tonic": self.key.tonic,
                "scale_type": self.key.scale_type,
                "scale": list(self.key.scale),
            },
            "root_cycle": list(self.root_cycle),
            "envelope": self.envelope.__dict__,
            "glide": self.glide.__dict__,
            "description": self.description,
        }
