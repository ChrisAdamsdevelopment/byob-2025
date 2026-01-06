import re
from typing import Iterable

REDACTION_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("EMAIL", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)),
    ("PHONE", re.compile(r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?){1}\d{3}[-.\s]?\d{4}\b")),
    ("SSN", re.compile(r"\b\d{3}-\d{2}-\d{4}\b")),
    ("API_KEY", re.compile(r"\bsk-[A-Za-z0-9]{20,}\b")),
    ("TOKEN", re.compile(r"\b(?:token|apikey|api_key|secret|password)\s*[:=]\s*[^\s]+", re.IGNORECASE)),
]

ADDRESS_HINTS = ["street", "st.", "avenue", "ave", "road", "rd.", "lane", "ln."]


def redact_line(line: str) -> str:
    redacted = line
    for label, pattern in REDACTION_PATTERNS:
        redacted = pattern.sub(f"[REDACTED:{label}]", redacted)
    lowered = redacted.lower()
    if any(hint in lowered for hint in ADDRESS_HINTS):
        redacted = re.sub(r"\b\d{1,5}\s+[^,\n]+", "[REDACTED:ADDRESS]", redacted)
    return redacted


def redact_text(text: str) -> str:
    return "\n".join(redact_line(line) for line in text.splitlines())


def redact_iter(lines: Iterable[str]) -> Iterable[str]:
    for line in lines:
        yield redact_line(line)
