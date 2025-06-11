import re

def normalize_title(title: str) -> str:
    """
    Normalize generator titles for uniform display.
    - Remove 'Hinattava', 'Traileri', 'Trailer'
    - Ensure 'Generator Diesel' at start
    - Always use ≤ before power value
    - Remove extra/duplicate ≤ or < signs
    - Remove 'STAGE V' and similar suffixes
    - Standardize kVA/kW formatting
    - Remove trailing commas and duplicate 'diesel'
    """
    t = title.strip()

    # Remove 'Hinattava', 'Traileri', 'Trailer' (case-insensitive)
    t = re.sub(r'\b(Hinattava|Traileri|Trailer)\b', '', t, flags=re.IGNORECASE)

    # Remove 'STAGE V' and similar (case-insensitive, at end or after kVA/kW)
    t = re.sub(r'(,?\s*STAGE\s*[IVXLCDM0-9]+)$', '', t, flags=re.IGNORECASE)

    # Remove extra spaces left by removal
    t = re.sub(r'\s+', ' ', t).strip()

    # Remove 'generaattori' or 'generator' or 'diesel' at start
    t = re.sub(r'^(generaattori|generator)\s*', '', t, flags=re.IGNORECASE)
    t = re.sub(r'^diesel\s*', '', t, flags=re.IGNORECASE)

    # Remove trailing ", diesel" or ",diesel"
    t = re.sub(r',?\s*diesel$', '', t, flags=re.IGNORECASE)

    # Remove duplicate ≤ or <≤ or < signs before power value
    t = re.sub(r'[<≤]+', '≤', t)

    # Ensure ≤ is present before the power value (if not already)
    t = re.sub(r'(?<!≤)\b(\d+[,\.]?\d*)\s*(kVA|kW)\b', r'≤\1 \2', t, flags=re.IGNORECASE)

    # Ensure ≤ is kept and spaced correctly
    t = re.sub(r'≤\s*', '≤', t)

    # Standardize kVA/kW formatting (with or without ≤)
    t = re.sub(r'≤(\d+[,\.]?\d*)\s*[kK][vV][aA]', r'≤\1 kVA', t)
    t = re.sub(r'≤(\d+[,\.]?\d*)\s*[kK][wW]', r'≤\1 kW', t)
    t = re.sub(r'(\d+[,\.]?\d*)\s*[kK][vV][aA]', r'\1 kVA', t)
    t = re.sub(r'(\d+[,\.]?\d*)\s*[kK][wW]', r'\1 kW', t)

    # Remove duplicate spaces again
    t = re.sub(r'\s+', ' ', t).strip()

    # Always start with "Generator Diesel"
    t = f"Generator Diesel {t}".strip()

    return t

def normalize_tax_text(tax_text: str) -> str:
    """
    Normalize tax text to English.
    """
    if tax_text and "ei sis. ALV" in tax_text:
        return "excluding VAT"
    return tax_text