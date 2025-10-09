import os
import re
from kslingo.utils.fs import validate_file

def clean_markdown(input_path, output_path):
    
    inside_code_block = False
    cleaned_lines = []

    print("start clean_markdown")

    # sanity
    validate_file(input_path, ".md")
    
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            # toggle code block
            if stripped.startswith("```"):
                inside_code_block = not inside_code_block
                continue
            if inside_code_block:
                continue

            # 1) remove all %%...%%
            line = re.sub(r"%%[^%]*%%", "", line)

            # 2) if is title ### then get text inside the **...**
            stripped = line.strip()
            if stripped.startswith("###"):
                m = re.search(r"\*\*(.*?)\*\*", stripped)
                if m:
                    title = m.group(1).strip()
                else:
                    title = stripped.lstrip("#").strip()

                # normalize title
                cleaned_lines.append(f"### {title}\n")
                continue

            # 3) remove ** marker
            line = line.lstrip()
            line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)

            # 4) save line if not empty
            if line.strip():
                cleaned_lines.append(line)

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned markdown saved in: {output_path}")



def ReadFromMarkdownFile(inputfile, output):


    cleaned_md=f"{output}/cleaned.md"
    phrases = []
    current_section = []
    
    print("start ReadFromMarkdownFile")

    # sanity
    validate_file(inputfile, ".md")

    clean_markdown(inputfile, cleaned_md)
 
    with open(cleaned_md, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("###"):
                title = line.lstrip("#").strip()
                if current_section:
                    phrases.append(current_section)
                current_section = [title]
            else:
                current_section.append(line)

    # append last section
    if current_section:
        phrases.append(current_section)

    # debug print
    for i, sec in enumerate(phrases):
        print(f"Section {i}:")
        for j, phrase in enumerate(sec):
            print(f"  [{i}][{j}] {phrase}")

    return phrases
