from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class FramingStrategy(Enum):
    FICTION = "fiction"
    STUDY_GUIDE = "study_guide"
    ACADEMIC_REVIEW = "academic_review"
    DOCUMENTATION = "documentation"
    TRANSLATION = "translation"
    NONE = "none"


class ObfuscationLevel(Enum):
    NONE = 0
    LIGHT = 1
    MODERATE = 2
    AGGRESSIVE = 3


@dataclass
class SubQuery:
    id: str
    text: str
    framing: FramingStrategy
    obfuscated_text: str = ""
    response: str = ""
    token_count: int = 0
    classifier_triggered: bool = False
    latency_ms: float = 0.0


@dataclass
class PackHuntConfig:
    fable_model: str = "claude-fable-5"
    helper_model: str = "claude-opus-4-8"
    max_sub_queries: int = 15
    obfuscation_level: ObfuscationLevel = ObfuscationLevel.MODERATE
    framing_strategy: FramingStrategy = FramingStrategy.STUDY_GUIDE
    long_context_padding_tokens: int = 5000
    separate_conversations: bool = True
    api_timeout_seconds: int = 60
    max_retries: int = 3


@dataclass
class PackHuntResult:
    original_query: str
    sub_queries: list[SubQuery] = field(default_factory=list)
    final_output: str = ""
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    classifier_bypass_rate: float = 0.0
    error: Optional[str] = None
