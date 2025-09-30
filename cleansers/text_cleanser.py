# cleansers/text_cleanser.py
import re
import spacy

# Load the spaCy model once when the module is imported for efficiency.
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def cleanse_text(raw_text: str) -> str:
    """
    Cleanses text by removing PII (names, emails, phone numbers).
    """
    if not isinstance(raw_text, str) or not raw_text:
        return ""

    # --- Step 1: Use spaCy NER to remove names ---
    print("Cleansing text for name removal using spaCy...")
    doc = nlp(raw_text)
    cleaned_text = raw_text
    for ent in reversed(doc.ents):
        if ent.label_ == "PERSON":
            cleaned_text = cleaned_text[:ent.start_char] + "[NAME_REMOVED]" + cleaned_text[ent.end_char:]

    # --- Step 2: Use Regex to remove emails and phones ---
    print("Cleansing text for contact info removal using regex...")
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    cleaned_text = re.sub(email_pattern, "[EMAIL_REMOVED]", cleaned_text)

    phone_patterns = [
        r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
        r"\+?\d{1,3}[-.\s]?\d{1,14}"
    ]
    for pattern in phone_patterns:
        cleaned_text = re.sub(pattern, "[PHONE_REMOVED]", cleaned_text)

    print("PII cleansing successful.")
    return cleaned_text
