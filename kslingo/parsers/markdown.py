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
# from kslingo.convert.file import Generate_pdf_from_md
from typing import List, Dict


def get_phrases_markdown(file_path: str, learn_lang: str, native_lang: str) -> List[Dict[str, any]]:
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
                        learn_lang: hu,
                        native_lang: sr
                    })

                else:
                    # fallback: line without flags and translation

                    if "%%" in line:
                        continue
                    
                    line = remove_leading_dash(line)

                    current_section["phrases"].append({
                        "flags": ["A2", "W", "D"],
                        "only_learn": True,
                        learn_lang: line,
                        native_lang: None
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


def just_only_reparse_md(input_file: str, output_file: str):
    print("start just_only_reparse_md")
    print(f"input_file={input_file}")

    inside_code_block = False

    with open(input_file, encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
        for line in fin:
            raw = line.rstrip('\n')

            # --- CODE BLOCKS ---
            if raw.strip().startswith("```"):
                inside_code_block = not inside_code_block
                fout.write(line)
                continue

            if inside_code_block:
                fout.write(line)
                continue

            if not raw.strip():
                fout.write("\n")
                continue

            if raw.strip().startswith("###"):
                fout.write(line)
                continue

            # --- EXTRACT FLAGS ---
            flag_match = re.search(r'%%(.*?)%%', raw)
            if flag_match:
                flags = flag_match.group(1).strip()
                # Remove all %%...%% occurrences
                raw = re.sub(r'%%.*?%%', '', raw).strip()
            else:
                flags = "A2,W,D"

            # Remove leading dash, normalize spacing
            raw = raw.lstrip("-").strip()
            raw = normalize_separator(raw)
            raw = remove_markdown_bold(raw)
            raw = remove_markdown_italic(raw)
            raw = remove_leading_dash(raw)


            # Split flags
            flag_list = [f.strip() for f in flags.split(",") if f.strip()]

            if len(flag_list) > 3:
                print("Error: Too much flags!")
                return


            # --- PARSE PHRASE ---
            if " - " in raw:
                hu, sr = raw.rsplit(" - ", 1)
                hu = hu.strip()
                sr = sr.strip()
                fout.write(f"- %%{flags}%% {hu} - {sr}\n")
                if flag_list[2] == "E":
                    # print(f"{flags} {hu} - {sr} | ENABLED")
                    fout.write(f"- %%{flags}%% **{hu}** - {sr}\n")
                else:
                    # print(f"{flags} {hu} - {sr} | DISABLED")
                    fout.write(f"- %%{flags}%% {hu} - {sr}\n")
            else:
                fout.write(f"- %%{flags}%% *{raw}*\n")

    print(f"\nFinish! File saved: {output_file}")
    return


def generate_output_md_from_phrases(
        phrases: List[Dict[str, any]],
        output_file: str,
        learn_lang: str,
        native_lang: str
    ) -> None:
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
                hu = phrase.get(learn_lang, "").strip()
                sr = phrase.get(native_lang, "")
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
