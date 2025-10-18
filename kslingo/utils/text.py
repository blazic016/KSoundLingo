import re


def normalize_separator(text: str) -> str:
    """
    Normalizes phrase separators (en dash, em dash, minus, equals)
    into a unified ' - ' separator, without breaking compound words
    like 'team-mate'.

    Skips replacing hyphens surrounded by word characters.
    """
    text = text.strip()

    # Step 1: Replace separator-like characters with placeholder
    text = re.sub(r"[–—−=]", " <SEP> ", text)

    # Step 2: Replace remaining hyphens that are not part of a word (i.e., not between letters)
    # i.e., space-hyphen-space or similar
    text = re.sub(r"(?<!\w)-{1}(?!\w)", " <SEP> ", text)

    # Step 3: Normalize placeholder to standard ' - '
    text = re.sub(r"\s*<SEP>\s*", " - ", text)

    # Step 4: Normalize multiple spaces
    text = re.sub(r"\s{2,}", " ", text)

    return text.strip()

def split_pair(text: str) -> tuple[str, str]:
    """
    Splits a line of text into two parts based on a separator (" - " or " – ").
    Intended for use in bilingual phrase dictionaries (e.g., Hungarian - Serbian).

    Args:
        text (str): A string containing two phrases separated by " - " or " – ".

    Returns:
        tuple[str, str]: (left, right) if separator found,
                         otherwise ("", text).
    """
    
    text = normalize_separator(text)
    
    # Regular expression to split phrases like "köszönöm - hvala" or "igen – da"
    parts = re.split(r"\s-\s", text.strip(), maxsplit=1)
    
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    # fallback: no separator found ; left full, right empty
    return text.strip(), ""

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

def remove_leading_dash(text: str) -> str:
    """
    Removes a leading dash '-', including variants like '- ', ' -', or ' - ' at the beginning of a string.

    Args:
        text (str): Input string that may start with combinations of spaces and dashes.

    Returns:
        str: String without the leading dash.
    """
    return re.sub(r"^\s*-\s*", "", text)


def ensure_dash_prefix(text: str) -> str:
    """
    Ensures that the string starts with exactly '- ' by normalizing any existing leading dashes.

    Args:
        text (str): Input string that may or may not start with a dash.

    Returns:
        str: String starting with '- '.
    """
    cleaned = re.sub(r"^[-\s]*", "", text)
    return f"- {cleaned}"


def bold_prefix_before_separator(line: str) -> str:
    """
    Bolds the part before ' - ' in a single line by wrapping it with '**'.

    Args:
        line (str): Input line containing ' - '.

    Returns:
        str: Line with bolded prefix if ' - ' is present; unchanged otherwise.
    """
    if " - " in line:
        prefix, suffix = line.split(" - ", 1)
        return f"**{prefix.strip()}** - {suffix.strip()}"
    return line


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