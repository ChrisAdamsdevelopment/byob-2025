from gem_workflow.cli.redaction import redact_text


def test_redacts_common_pii_and_secrets():
    sample = (
        "Contact me at jane.doe@example.com or 555-123-4567. "
        "SSN 123-45-6789. "
        "password=supersecret "
        "api key sk-1234567890abcdef1234567890abcdef. "
        "123 Main Street"
    )
    redacted = redact_text(sample)
    assert "jane.doe@example.com" not in redacted
    assert "555-123-4567" not in redacted
    assert "123-45-6789" not in redacted
    assert "supersecret" not in redacted
    assert "sk-1234567890abcdef1234567890abcdef" not in redacted
    assert "[REDACTED:EMAIL]" in redacted
    assert "[REDACTED:PHONE]" in redacted
    assert "[REDACTED:SSN]" in redacted
    assert "[REDACTED:TOKEN]" in redacted
    assert "[REDACTED:API_KEY]" in redacted
