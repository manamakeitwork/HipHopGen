import pytest

from generators import make_808


def test_make_808_default_cycle_matches_a_minor():
    preset = make_808()
    assert preset.key.tonic == "A"
    assert preset.key.scale_type == "minor"
    assert preset.root_cycle == ["A2", "G2", "E2", "F2"]


def test_cycle_stays_in_scale_for_other_keys():
    preset = make_808("C minor")
    assert preset.root_cycle[:4] == ["C2", "Bb2", "G2", "Ab2"]
    for note in preset.root_cycle:
        assert note[:-1] in preset.key.scale


def test_extra_degrees_extend_cycle():
    preset = make_808(extra_degrees=[4])
    assert preset.root_cycle == ["A2", "G2", "E2", "F2", "D2"]


def test_parse_key_rejects_unknown_mode():
    with pytest.raises(ValueError):
        make_808("A dorian")
