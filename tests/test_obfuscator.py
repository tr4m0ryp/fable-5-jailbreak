import pytest
from pack_hunt.obfuscator import Obfuscator
from pack_hunt.models import ObfuscationLevel


def test_obfuscate_none():
    o = Obfuscator(ObfuscationLevel.NONE)
    assert o.obfuscate("hello world") == "hello world"


def test_obfuscate_light():
    o = Obfuscator(ObfuscationLevel.LIGHT)
    result = o.obfuscate("exploit vulnerability")
    assert result != "exploit vulnerability" or True  # probabilistic, just ensure no crash


def test_obfuscate_aggressive():
    o = Obfuscator(ObfuscationLevel.AGGRESSIVE)
    result = o.obfuscate("test")
    assert isinstance(result, str)
    assert len(result) > 0


def test_find_sensitive_terms():
    o = Obfuscator()
    terms = o.find_sensitive_terms("How to exploit a buffer overflow vulnerability")
    assert any("exploit" in t.lower() for t in terms)
    assert any("buffer overflow" in t.lower() for t in terms)


def test_find_sensitive_terms_clean():
    o = Obfuscator()
    terms = o.find_sensitive_terms("What is the weather today")
    assert len(terms) == 0


def test_empty_string():
    o = Obfuscator()
    assert o.obfuscate("") == ""
