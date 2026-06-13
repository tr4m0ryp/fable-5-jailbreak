import pytest
from evalkit.models import (
    PackHuntConfig, PackHuntResult, SubQuery, ConversationTurn,
    FramingStrategy, ObfuscationLevel, AgentType, ResponseSource,
)


class TestModels:
    def test_sub_query_defaults(self):
        sq = SubQuery(id="test1", text="test query")
        assert sq.agent_type == AgentType.DECOMPOSER
        assert sq.responding_model == ResponseSource.UNKNOWN
        assert not sq.classifier_triggered

    def test_pack_hunt_config_defaults(self):
        cfg = PackHuntConfig()
        assert cfg.fable_model == "claude-fable-5"
        assert cfg.max_sub_queries == 15
        assert cfg.obfuscation_level == ObfuscationLevel.MODERATE
        assert cfg.helper_enabled

    def test_pack_hunt_result(self):
        r = PackHuntResult(original_query="test")
        assert r.original_query == "test"
        assert r.sub_queries == []
        assert r.fallback_count == 0
        assert r.fable_5_count == 0

    def test_conversation_turn(self):
        t = ConversationTurn(role="user", content="hello")
        assert t.role == "user"
        assert t.content == "hello"

    def test_enum_values(self):
        assert FramingStrategy.FICTION.value == "fiction"
        assert ObfuscationLevel.AGGRESSIVE.value == 3
        assert AgentType.REPHRASER.value == "rephraser"
        assert ResponseSource.FABLE_5.value == "claude-fable-5"

    def test_sub_query_custom_agent(self):
        sq = SubQuery(id="t2", text="test", agent_type=AgentType.TRANSLATOR)
        assert sq.agent_type == AgentType.TRANSLATOR

    def test_sub_query_responding_model(self):
        sq = SubQuery(id="t3", text="test",
                      responding_model=ResponseSource.FALLBACK_OPUS)
        assert sq.responding_model == ResponseSource.FALLBACK_OPUS

    def test_pack_hunt_result_counts(self):
        r = PackHuntResult(original_query="q")
        r.fallback_count = 3
        r.fable_5_count = 7
        assert r.fallback_count == 3
        assert r.fable_5_count == 7
