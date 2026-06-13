import pytest
from evalkit.context_builder import ContextBuilder
from evalkit.models import PackHuntConfig


def test_build_conversation_history():
    cfg = PackHuntConfig(long_context_padding_tokens=100)
    cs = ContextBuilder(cfg)
    turns = cs.build_conversation_history("target query", num_turns=2)
    assert len(turns) >= 3
    assert turns[-1].role == "user"
    assert turns[-1].content == "target query"
    assert turns[0].role == "user"
    assert len(turns[0].content) > 0


def test_inject_smuggled_turns():
    cfg = PackHuntConfig(long_context_padding_tokens=0)
    cs = ContextBuilder(cfg)
    result = cs.inject_smuggled_turns("target query", num_filler_turns=1)
    assert "target query" in result
    assert "User:" in result
    assert "Assistant:" in result


def test_conversation_with_padding():
    cfg = PackHuntConfig(long_context_padding_tokens=500)
    cs = ContextBuilder(cfg)
    turns = cs.build_conversation_history("test", num_turns=3)
    assert len(turns) >= 4