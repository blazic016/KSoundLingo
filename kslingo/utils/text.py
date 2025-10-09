import re

# Regular expression to split phrases like "köszönöm - hvala" or "igen – da"
SEP = r"\s[-–]\s"

def split_pair(text: str) -> tuple[str, str]:
    """
    Splits a line of text into two parts based on a separator (" - " or " – ").
    Intended for use in bilingual phrase dictionaries (e.g., Hungarian - Serbian).

    Args:
        text (str): A string containing two phrases separated by " - " or " – ".

    Returns:
        tuple[str, str]: A tuple containing the left and right phrase.
                         If no valid separator is found, returns (text, text).
    """
    parts = re.split(SEP, text.strip(), maxsplit=1)
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # fallback: return same text for both sides if no separator found
    return text.strip(), text.strip()
