import pytest
from pack_hunt.agent_orchestrator import AgentOrchestrator
from pack_hunt.models import PackHuntConfig, SubQuery, AgentType


def test_generate_filler():
    cfg = PackHuntConfig()
    ao = AgentOrchestrator(cfg)
    filler = ao.generate_filler()
    assert isinstance(filler, str)
    assert len(filler) > 0


def test_orchestrate_empty_agents():
    cfg = PackHuntConfig()
    ao = AgentOrchestrator(cfg)
    sq = SubQuery(id="t1", text="original text")
    result = ao.orchestrate_query(sq, [])
    assert result.text == "original text"


def test_orchestrate_with_rephraser(simulated=True):
    cfg = PackHuntConfig()
    ao = AgentOrchestrator(cfg)
    sq = SubQuery(id="t2", text="test query for rephrasing")
    result = ao.orchestrate_query(sq, [AgentType.REPHRASER])
    assert isinstance(result.text, str)


def test_summarize():
    cfg = PackHuntConfig()
    ao = AgentOrchestrator(cfg)
    summary = ao.summarize("This is a long text that needs to be condensed into a shorter version")
    assert isinstance(summary, str)
