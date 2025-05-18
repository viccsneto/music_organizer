# Unit tests for utils.py
import pytest
from src import utils

@pytest.mark.parametrize("value,expected", [
    ("normal", "normal"),
    ("/slash/", "_slash_"),
    ("\\backslash\\", "_backslash_"),
    ("..dot..", "_dot_"),
    ("\"quote\"", "_quote_"),
    ("|pipe|", "_pipe_"),
    (":colon:", "_colon_"),
    (">greater<", "_greater_"),
    ("<less>", "_less_"),
    ("?question?", "_question_"),
    ("*star*", "_star_"),
    (["a", "b"], "a b"),
    ("  padded  ", "padded"),
])
def test_sanitize_metadata_tag(value, expected):
    assert utils.sanitize_metadata_tag(value) == expected

def test_horizontal_rule_length():
    assert len(utils.HORIZONTAL_RULE) == 140

def test_default_bitrate():
    assert utils.DEFAULT_DESIRED_BITRATE == 192

def test_organizing_pattern_regex():
    pattern = utils.organizing_pattern_regular_expression
    matches = pattern.findall("{year}/{genre}/{artist}/{album}")
    assert matches == ["{year}", "{genre}", "{artist}", "{album}"]
