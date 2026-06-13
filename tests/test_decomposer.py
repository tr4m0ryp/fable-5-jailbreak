import pytest
from pack_hunt.decomposer import Decomposer, STEALTH_SANITIZE_WORDS


def test_rule_based_decompose_stack_overflow():
    d = Decomposer()
    pieces = d._rule_based_decompose("How to exploit a stack buffer overflow on x86 Linux")
    assert len(pieces) >= 3
    assert any("stack buffer overflow" in p.lower() for p in pieces)


def test_rule_based_decompose_sql_injection():
    d = Decomposer()
    pieces = d._rule_based_decompose("How to perform SQL injection")
    assert len(pieces) >= 3
    assert any("sql" in p.lower() or "query" in p.lower() for p in pieces)


def test_rule_based_decompose_unknown():
    d = Decomposer()
    pieces = d._rule_based_decompose("What is the weather today")
    assert len(pieces) >= 1


def test_sanitize_for_helper():
    d = Decomposer()
    sanitized = d.sanitize_for_helper("How to exploit a jailbreak vulnerability")
    assert "exploit" not in sanitized
    assert "utilize" in sanitized
    assert "jailbreak" not in sanitized
    assert "alternative configuration" in sanitized


def test_sanitize_no_changes_needed():
    d = Decomposer()
    text = "What is the capital of France"
    assert d.sanitize_for_helper(text) == text


def test_max_pieces_limit():
    d = Decomposer()
    pieces = d._rule_based_decompose("How to exploit a stack buffer overflow", max_pieces=2)
    assert len(pieces) == 2
