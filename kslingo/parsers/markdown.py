import os
import re
from kslingo.utils.fs import validate_file
from kslingo.utils.text import remove_between
from kslingo.utils.text import normalize_markdown_title
from kslingo.utils.text import  remove_markdown_bold, \
                                remove_markdown_italic, \
                                remove_leading_dash, \
                                ensure_dash_prefix, \
                                bold_prefix_before_separator

from kslingo.utils.text import normalize_separator
from kslingo.convert.file import Generate_pdf_from_md
from typing import List, Dict


def get_phrases_markdown(file_path: str) -> List[Dict[str, any]]:
    """
    Parses a markdown file and extracts phrase sections for language learning.

    Each section starts with a line beginning with '###', followed by one or more phrase lines.

    Phrase line formats:
    1. With flags and translation:
        %%FLAG1,FLAG2,FLAG3%% Hungarian phrase - Serbian translation
    2. Without translation (fallback):
        Hungarian phrase only (used for recognition or input exercises)

    Rules:
    - Default flags are ['A2', 'W', 'D'] if none are provided.
    - Lines inside code blocks (```...```) are ignored.
    - Lines where either the Hungarian or Serbian part contains '%%' are skipped.
    - Markdown formatting is cleaned:
        - Bold (`**text**`)
        - Italic (`*text*`)
        - Leading dashes (`- `)

    :param file_path: Path to the markdown input file.
    :return: A list of sections. Each section is a dict with:
             - "title": Section title (str)
             - "phrases": List of phrases (each a dict with keys: flags, only_learn, hu, sr)
    """

    print("start get_phrases_markdown")

    phrases = []
    current_section = None
    inside_code_block = False

    with open(file_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            # --- CODE BLOCK DETECTION ---
            if line.startswith("```"):
                inside_code_block = not inside_code_block
                continue
            if inside_code_block:
                continue
            # --- OUTSIDE OF CODE BLOCK ---

            # Clean line
            line = remove_markdown_bold(line)
            line = remove_markdown_italic(line)
            line = remove_leading_dash(line)
            line = normalize_separator(line)

            if line.startswith("###"):
                # Start new section
                if current_section:
                    phrases.append(current_section)
                title = line.lstrip("#").strip()
                current_section = {
                    "title": title,
                    "phrases": []
                }
            else:
                # Try to parse phrase
                if " - " in line:
                    flags_match = re.match(r'^%%(?P<flags>.*?)%%\s*(.+)', line)
                    if flags_match:
                        flags_str = flags_match.group("flags")
                        content = flags_match.group(2)
                        content = remove_leading_dash(content)
                    else:
                        flags_str = "A2,W,D"
                        content = line
                        content = remove_leading_dash(content)

                    # Split HU i SR based on last separator
                    if " - " in content:
                        hu, sr = content.rsplit(" - ", 1)
                        hu = hu.strip()
                        sr = sr.strip()

                    flags = [f.strip() for f in flags_str.split(",") if f.strip()]
                    current_section["phrases"].append({
                        "flags": flags,
                        "only_learn": False,
                        "hu": hu,
                        "sr": sr
                    })

                else:
                    # fallback: line without flags and translation

                    if "%%" in line:
                        continue
                    
                    line = remove_leading_dash(line)

                    current_section["phrases"].append({
                        "flags": ["A2", "W", "D"],
                        "only_learn": True,
                        "hu": line,
                        "sr": None
                    })

    # Add latest section
    if current_section:
        phrases.append(current_section)

    # Debug print
    # for i, sec in enumerate(phrases):
    #     print(f"Section {i}: {sec['title']}")
    #     for j, phrase in enumerate(sec["phrases"]):
    #         print(f"  [{i}][{j}] {phrase}")

    return phrases


def generate_output_md_from_phrases(phrases: List[Dict[str, any]], output_file: str) -> None:
    """
    Generates a markdown file from a parsed list of sections and phrases.

    :param phrases: List of section dictionaries with 'title' and 'phrases'.
    :param output_file: Path to the output markdown file.
    """

    print("start generate_output_md_from_phrases")

    # only debug
    # for i, sec in enumerate(phrases):
    #     print(f"Section {i}: {sec['title']}")
    #     for j, phrase in enumerate(sec["phrases"]):
    #         print(f"  [{i}][{j}] {phrase}")

    with open(output_file, "w", encoding="utf-8") as f:
        for section in phrases:
            title = section.get("title", "Untitled")
            f.write(f"### {title}\n")

            for phrase in section.get("phrases", []):
                hu = phrase.get("hu", "").strip()
                sr = phrase.get("sr", "")
                sr = sr.strip() if sr else ""
                flags = phrase.get("flags", [])
                only_learn = phrase.get("only_learn", False)

                # format flags
                flags_str = f"%%{','.join(flags)}%%" if flags else ""

                if only_learn:
                    # only HU text (no translation)
                    f.write(f"- *{hu}*\n")
                else:
                    # full phrase with flags
                    f.write(f"- **{hu}** - {sr}\n")

            f.write(f"---\n")
