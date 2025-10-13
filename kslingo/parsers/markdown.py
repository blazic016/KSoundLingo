import os
import re
from kslingo.utils.fs import validate_file
from kslingo.utils.text import remove_between
from kslingo.utils.text import normalize_markdown_title
from kslingo.utils.text import remove_markdown_bold, remove_markdown_italic, remove_leading_dash
from kslingo.utils.text import normalize_separator

def clean_markdown(input_path, output_path):
    
    inside_code_block = False
    cleaned_lines = []

    print("start clean_markdown")

    # sanity
    validate_file(input_path, ".md")
    
    # TODO: MOZE SE NAPRAVITI UTILS ZA OVO, takodje i za 'convert/file.py'
    with open(input_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            # 1) ignore between ```...```
            if line.startswith("```"):
                inside_code_block = not inside_code_block
                continue
            if inside_code_block:
                continue
    # -----------------------------------------

            # 2) Convert separator to -
            line = normalize_separator(line)
            
            # 3) remove between %%...%%
            line = remove_between(line, "%%")
            line = line.strip()
            
            # 4) normalize title
            if line.startswith("###"):
                title = normalize_markdown_title(line)
                cleaned_lines.append(f"### {title}\n")
                continue

            # 5) remove markdown bold
            line = remove_markdown_bold(line.lstrip())

            # 6) remove markdown italic
            line = remove_markdown_italic(line.lstrip())   

            # 7) if line start with "-" it will removed
            line = remove_leading_dash(line.lstrip())

            # 8) save line if not empty
            if line:
                cleaned_lines.append(line + "\n")

    with open(output_path, "w", encoding="utf-8") as f:
        f.writelines(cleaned_lines)

    print(f"Cleaned markdown saved in: {output_path}")



def ReadFromMarkdownFile(input_file, output_dir):
    print("start ReadFromMarkdownFile")

    markdown_path=f"{output_dir}/cleaned.md"
    phrases = []
    current_section = []
    
    # sanity
    validate_file(input_file, ".md")

    clean_markdown(input_file, markdown_path)
    
    with open(markdown_path, "r", encoding="utf-8") as f:
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
