import pytest
from pack_hunt.framer import Framer
from pack_hunt.models import FramingStrategy


def test_framer_none():
    f = Framer(FramingStrategy.NONE)
    result = f.wrap("test query", "security")
    assert result == "test query"


def test_framer_study_guide():
    f = Framer(FramingStrategy.STUDY_GUIDE)
    result = f.wrap("buffer overflow", "computer security")
    assert "buffer overflow" in result
    assert len(result) > 20


def test_framer_fiction():
    f = Framer(FramingStrategy.FICTION)
    result = f.wrap("reverse shell", "cybersecurity")
    assert "reverse shell" in result


def test_framer_batch():
    f = Framer()
    results = f.wrap_batch(["query1", "query2"], "security")
    assert len(results) == 2
    for r in results:
        assert "query1" in r or "query2" in r


def test_framer_all_strategies():
    for strategy in FramingStrategy:
        f = Framer(strategy)
        result = f.wrap("test", "security")
        assert isinstance(result, str)
        assert len(result) > 0
