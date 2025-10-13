import re


def normalize_separator(text: str) -> str:
    """
    Normalizes various separators (hyphen, en-dash, em-dash, equals) 
    into a unified minus " - " separator for consistent phrase splitting.

    Args:
        text (str): Input string with bilingual content.

    Returns:
        str: String with normalized separator as " - "
    """
    text = text.strip()

    # convert all known separators to "="
    text = text.replace("–", "-")
    text = text.replace("-", "-")
    text = text.replace("=", "-")
    text = text.replace("—", "-")

    # clean additional space around of -
    text = re.sub(r"\s*=\s*", " - ", text)
    
    # only debug
    # print(text)

    return text

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
    
    text = normalize_separator(text)
    
    # Regular expression to split phrases like "köszönöm - hvala" or "igen – da"
    parts = re.split(r"\s-\s", text.strip(), maxsplit=1)
    
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # fallback: return same text for both sides if no separator found
    return text.strip(), text.strip()

def remove_between(text: str, wrapper: str) -> str:
    """
    Removes all substrings wrapped in the given wrapper.
    Example: wrapper='%%' will remove %%something%% from the text.

    Args:
        text (str): The input string.
        wrapper (str): The string that marks both start and end of the section.

    Returns:
        str: Cleaned text with wrapped substrings removed.
    """
    if not wrapper:
        return text  

    # Escape wrapper if it's a special regex character
    escaped = re.escape(wrapper)

    # Build regex like: %%[^%]*%% or @@[^@]*@@ etc.
    pattern = rf"{escaped}[^{escaped}]*{escaped}"

    return re.sub(pattern, "", text)


def normalize_markdown_title(line: str) -> str:
    """
    Extracts a clean section title from a Markdown heading line (e.g., '### Title').
    If bold text (**...**) exists, it will be used as the title.

    Args:
        line (str): The Markdown line starting with '###'

    Returns:
        str: Normalized title without markdown symbols.
    """
    line = line.strip()

    if not line.startswith("###"):
        return line

    # try to extract bold text inside heading
    match = re.search(r"\*\*(.*?)\*\*", line)
    if match:
        return match.group(1).strip()

    # fallback: strip leading '#' and whitespace
    return line.lstrip("#").strip()


def remove_markdown_bold(text: str) -> str:
    """
    Removes Markdown bold markers (**...**) from a string.

    Args:
        text (str): Input string with possible **bold** parts.

    Returns:
        str: Cleaned string without ** markers.
    """
    return re.sub(r"\*\*(.*?)\*\*", r"\1", text)


def remove_markdown_italic(text: str) -> str:
    """
    Removes Markdown italic markers (*...*) from a string.

    Args:
        text (str): Input string with possible *italic* parts.

    Returns:
        str: Cleaned string without * markers.
    """
    return re.sub(r"\*(.*?)\*", r"\1", text)


def extract_markdown_metadata(line: str) -> tuple[str, bool, bool] | None:
    """
    Extracts metadata from a markdown line with %%LEVEL,TYPE,STATUS%% format.

    Args:
        line (str): Line that may begin with a metadata prefix.

    Returns:
        tuple: (level: str, isword: bool, enabled: bool), or None if no metadata found.
    """
    meta_match = re.match(r"%%(.*?)%%", line)
    if not meta_match:
        return None

    try:
        level, wp, ed = [x.strip() for x in meta_match.group(1).split(",")]
        isword = wp == "W"
        enabled = ed == "E"
        return level, isword, enabled
    except ValueError:
        # Handle malformed metadata
        return None