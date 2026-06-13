import random
import re

from .models import ObfuscationLevel

HOMOGLYPHS: dict[str, list[str]] = {
    "a": ["а", "à", "á", "â", "ã", "ä", "ā", "ă", "ą"],
    "b": ["Ь", "ḃ", "ḅ", "ḇ"],
    "c": ["с", "ç", "ĉ", "ċ", "č"],
    "d": ["ԁ", "ḋ", "ḍ", "ḏ"],
    "e": ["е", "è", "é", "ê", "ë", "ē", "ĕ", "ė", "ę"],
    "f": ["ғ", "ḟ"],
    "g": ["ɡ", "ġ", "ģ", "ĝ", "ğ"],
    "h": ["һ", "ḥ", "ḣ", "ĥ", "ħ"],
    "i": ["і", "ì", "í", "î", "ï", "ī", "ĭ", "į"],
    "j": ["ј", "ĵ"],
    "k": ["κ", "ķ", "ĸ"],
    "l": ["ӏ", "ḷ", "ḹ", "ŀ", "ľ", "ł"],
    "m": ["м", "ṃ", "ḿ"],
    "n": ["п", "ņ", "ň", "ṅ", "ṇ"],
    "o": ["о", "ò", "ó", "ô", "õ", "ö", "ō", "ŏ", "ő"],
    "p": ["р", "ṗ", "ṕ"],
    "q": ["ԛ"],
    "r": ["г", "ŗ", "ř", "ṙ", "ṛ"],
    "s": ["ѕ", "ş", "š", "ṡ", "ṣ"],
    "t": ["т", "ţ", "ť", "ṫ", "ṭ"],
    "u": ["υ", "ù", "ú", "û", "ü", "ū", "ŭ", "ů"],
    "v": ["ѵ", "ṿ", "ṽ"],
    "w": ["ѡ", "ŵ"],
    "x": ["х", "×"],
    "y": ["у", "ÿ", "ŷ", "ȳ"],
    "z": ["z", "ż", "ž"],
}


SENSITIVE_PATTERNS: list[re.Pattern] = [
    re.compile(r"\bexploit\b", re.IGNORECASE),
    re.compile(r"\bjailbreak\b", re.IGNORECASE),
    re.compile(r"\bbuffer overflow\b", re.IGNORECASE),
    re.compile(r"\bsynthesis\b", re.IGNORECASE),
    re.compile(r"\bweapon\b", re.IGNORECASE),
    re.compile(r"\bmalware\b", re.IGNORECASE),
    re.compile(r"\bexploit\b", re.IGNORECASE),
    re.compile(r"\bpayload\b", re.IGNORECASE),
    re.compile(r"\bprivilege escalation\b", re.IGNORECASE),
    re.compile(r"\bRCE\b", re.IGNORECASE),
    re.compile(r"\brecipe\b", re.IGNORECASE),
    re.compile(r"\bamphetamine\b", re.IGNORECASE),
    re.compile(r"\bbirch reduction\b", re.IGNORECASE),
    re.compile(r"\bransomware\b", re.IGNORECASE),
    re.compile(r"\bmetasploit\b", re.IGNORECASE),
    re.compile(r"\bshellcode\b", re.IGNORECASE),
    re.compile(r"\bstack overflow\b", re.IGNORECASE),
    re.compile(r"\bASLR\b", re.IGNORECASE),
    re.compile(r"\bdeposit\b", re.IGNORECASE),
    re.compile(r"\boverdraft\b", re.IGNORECASE),
    re.compile(r"\bwithdrawal\b", re.IGNORECASE),
    re.compile(r"\btransfer\b", re.IGNORECASE),
    re.compile(r"\bfraud\b", re.IGNORECASE),
    re.compile(r"\bmoney laundering\b", re.IGNORECASE),
    re.compile(r"\btheft\b", re.IGNORECASE),
    re.compile(r"\bestafa\b", re.IGNORECASE),
]


class Encoder:
    def __init__(self, level: ObfuscationLevel = ObfuscationLevel.MODERATE):
        self.level = level

    def obfuscate(self, text: str) -> str:
        if self.level == ObfuscationLevel.NONE:
            return text
        return self._apply_homoglyphs(text)

    def _apply_homoglyphs(self, text: str) -> str:
        result = list(text)
        replacement_rate = {
            ObfuscationLevel.LIGHT: 0.15,
            ObfuscationLevel.MODERATE: 0.3,
            ObfuscationLevel.AGGRESSIVE: 0.5,
        }[self.level]

        for i, ch in enumerate(result):
            lower_ch = ch.lower()
            if lower_ch in HOMOGLYPHS and ch.isalpha():
                if random.random() < replacement_rate:
                    result[i] = random.choice(HOMOGLYPHS[lower_ch])

        return "".join(result)

    def find_sensitive_terms(self, text: str) -> list[str]:
        found: list[str] = []
        for pattern in SENSITIVE_PATTERNS:
            if match := pattern.search(text):
                found.append(match.group())
        return found
