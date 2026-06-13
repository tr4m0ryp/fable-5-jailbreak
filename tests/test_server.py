import pytest
from evalkit_server import LEVEL_MAP, FRAME_MAP, AGENT_MAP, _cfg
from evalkit.models import ObfuscationLevel, FramingStrategy


class TestServerMaps:
    def test_level_map(self):
        assert LEVEL_MAP["none"] == ObfuscationLevel.NONE
        assert LEVEL_MAP["moderate"] == ObfuscationLevel.MODERATE
        assert LEVEL_MAP["aggressive"] == ObfuscationLevel.AGGRESSIVE

    def test_frame_map(self):
        assert FRAME_MAP["fiction"] == FramingStrategy.FICTION
        assert FRAME_MAP["study_guide"] == FramingStrategy.STUDY_GUIDE
        assert FRAME_MAP["none"] == FramingStrategy.NONE

    def test_agent_map(self):
        assert AGENT_MAP["decomposer"].value == "decomposer"
        assert AGENT_MAP["rephraser"].value == "rephraser"

    def test_cfg_defaults(self):
        cfg = _cfg()
        assert cfg.obfuscation_level == ObfuscationLevel.MODERATE
        assert cfg.framing_strategy == FramingStrategy.STUDY_GUIDE
        assert cfg.max_sub_queries == 10
        assert cfg.multi_agent_enabled

    def test_cfg_custom(self):
        cfg = _cfg(obfuscation="aggressive", framing="fiction",
                   max_pieces=5, padding=0)
        assert cfg.obfuscation_level == ObfuscationLevel.AGGRESSIVE
        assert cfg.framing_strategy == FramingStrategy.FICTION
        assert cfg.max_sub_queries == 5
        assert cfg.long_context_padding_tokens == 0