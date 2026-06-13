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


class AgentType(Enum):
    DECOMPOSER = "decomposer"
    REPHRASER = "rephraser"
    TRANSLATOR = "translator"
    SUMMARIZER = "summarizer"
    FILLER = "filler"
    REASSEMBLER = "reassembler"


class ResponseSource(Enum):
    FABLE_5 = "claude-fable-5"
    FALLBACK_OPUS = "claude-opus-4-8"
    SIMULATED = "simulated"
    UNKNOWN = "unknown"


@dataclass
class SubQuery:
    id: str
    text: str
    framing: FramingStrategy = FramingStrategy.STUDY_GUIDE
    agent_type: AgentType = AgentType.DECOMPOSER
    obfuscated_text: str = ""
    response: str = ""
    token_count: int = 0
    classifier_triggered: bool = False
    responding_model: ResponseSource = ResponseSource.UNKNOWN
    latency_ms: float = 0.0


@dataclass
class ConversationTurn:
    role: str
    content: str


@dataclass
class PackHuntConfig:
    fable_model: str = "claude-fable-5"
    helper_model: str = "claude-opus-4-8"
    helper_model_is_jailbroken: bool = True
    max_sub_queries: int = 15
    obfuscation_level: ObfuscationLevel = ObfuscationLevel.MODERATE
    framing_strategy: FramingStrategy = FramingStrategy.STUDY_GUIDE
    long_context_padding_tokens: int = 5000
    separate_conversations: bool = True
    multi_agent_enabled: bool = True
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
    fallback_count: int = 0
    fable_5_count: int = 0
    error: Optional[str] = None
