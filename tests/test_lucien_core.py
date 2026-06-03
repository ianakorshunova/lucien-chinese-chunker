import sys
from pathlib import Path

# Allow tests to import lucien_core.py from the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from lucien_core import analyze_sentence

def test_basic_sentence_chunks():
    result = analyze_sentence("我今天很累")
    assert result["syntax"]["subject"] == "我"
    assert result["syntax"]["time"] == "今天"
    assert result["syntax"]["predicate"] == "很累"


def test_emphatic_negation_yidian_ye():
    result = analyze_sentence("我今天一点也不累")
    assert result["syntax"]["predicate"] == "一点也不累"


def test_emphatic_negation_yidianr_ye():
    result = analyze_sentence("我今天一点儿也不累")
    assert result["syntax"]["predicate"] == "一点儿也不累"


def test_negative_state():
    result = analyze_sentence("我今天不累")
    assert result["syntax"]["predicate"] == "不累"


def test_positive_low_intensity():
    result = analyze_sentence("我今天有点累")
    assert result["syntax"]["predicate"] == "有点累"