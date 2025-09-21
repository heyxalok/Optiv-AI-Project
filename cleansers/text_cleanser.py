import re


def cleanse_text(raw_text):
    if not isinstance(raw_text, str):
        return raw_text

    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    phone_patterns = [
        r"\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}",
        r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b",
        r"\(\d{3}\)\s?\d{3}[-.\s]?\d{4}",
        r"\+\d{1,3}[-.\s]?\d{1,14}",
    ]

    print("Cleansing text for PII removal...")

    cleaned_text = re.sub(email_pattern, "[EMAIL_REMOVED]", raw_text)

    for pattern in phone_patterns:
        cleaned_text = re.sub(pattern, "[PHONE_REMOVED]", cleaned_text)

    return cleaned_text
