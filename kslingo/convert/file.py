import json
from pathlib import Path
from kslingo.utils.fs import ensure_dir
import re
import csv
from kslingo.utils.fs import validate_file
from kslingo.utils.text import normalize_markdown_title
from kslingo.utils.text import normalize_separator
from kslingo.utils.text import extract_markdown_metadata
from kslingo.utils.text import remove_between
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Border, Side
def Convert_json2md(json_path: str, md_output_path: str, learn_lang: str, native_lang: str) -> None:
    """
    Converts a structured JSON file to Markdown format with flags for level, type, and enabled state.

    Args:
        json_path (str): Path to the input JSON file.
        md_output_path (str): Path to the output Markdown file.
        learn_lang (str): Language code to be shown first.
        native_lang (str): Language code to be shown second.
    """
    
    print("start Convert_json2md")
    
    json_path = Path(json_path)
    md_output_path = Path(md_output_path)

    if not json_path.is_file():
        raise FileNotFoundError(f"Input file '{json_path}' does not exist")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    lines = []

    for section in data:
        category = section.get("category", {})
        cat_learn = category.get(learn_lang, "Unknown")
        cat_native = category.get(native_lang, "Unknown")
        lines.append(f"### {cat_learn} - {cat_native}")

        for phrase in section.get("phrases", []):
            level = phrase.get("level", "A1")
            isword = phrase.get("isword", False)
            enabled = phrase.get("enabled", False)
            translations = phrase.get("translations", {})

            left = translations.get(learn_lang, "").strip()
            right = translations.get(native_lang, "").strip()
            if not left or not right:
                continue

            flag_w_p = "W" if isword else "P"
            flag_e_d = "E" if enabled else "D"

            flags = f"%%{level},{flag_w_p},{flag_e_d}%%"
            line = f"{flags} {left} - {right}"
            lines.append(line)

        lines.append("")

    ensure_dir(md_output_path.parent)
    
    with open(md_output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"Created markdown file : {md_output_path}")
    
def add_prefix_on_markdown(md_input_path: str, md_output_path: str, prefix: str = "%%A2,W,D%%") -> None:
    """
    Adds a given prefix to all phrase lines in a Markdown file, 
    excluding category headers (lines starting with '###') and empty lines.

    This is useful for tagging phrases with metadata (e.g., level, type, status)
    in preparation for conversion to structured formats like JSON.

    Args:
        md_input_path (str): Path to the original Markdown (.md) file.
        md_output_path (str): Path where the modified Markdown file will be saved.
        prefix (str): The prefix string to prepend to each phrase line.
    """
    
    # TODO: za sada bezuslovno ubacuje prefix, napravi da ubacuje samo ako ga nema.
    
    input_path = Path(md_input_path)
    output_path = Path(md_output_path)

    with open(input_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated_lines = []
    for line in lines:
        stripped = line.strip()

        if not stripped:
            updated_lines.append("")
        elif stripped.startswith("###"):
            updated_lines.append(line.rstrip())
        else:
            updated_lines.append(f"{prefix} {line.strip()}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(updated_lines) + "\n")
        
    print(f"Created prefixed markdown file : {output_path}")
    

def Convert_md2json(md_input_path: str, json_output_path: str, learn_lang: str, native_lang: str, default_en_lang: str = "en") -> None:
    """
    Converts a Markdown file with metadata prefixes into a structured JSON format for multilingual phrases.

    Args:
        md_input_path (str): Path to the Markdown input file.
        json_output_path (str): Path to save the generated JSON file.
        learn_lang (str): Language code used for learning (e.g., 'hu').
        native_lang (str): Native language code (e.g., 'sr').
        default_en_lang (str): Default fallback language code (used for 'en').
    """
    
    print("start Convert_json_to_markdown")

    # sanity
    validate_file(md_input_path, ".md")


    md_input_path = Path(md_input_path)
    json_output_path = Path(json_output_path)


    inside_code_block = False
    clean_lines = []

    # TODO: MOZE SE NAPRAVITI UTILS ZA OVO (da ignorise block ```)
    with open(md_input_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()

            # 1) Toggle code block on/off when encountering ```
            if line.startswith("```"):
                inside_code_block = not inside_code_block
                continue

            # 2) If inside code block, skip line
            if inside_code_block:
                continue

            # 3) Add valid lines
            if line:
                clean_lines.append(line)
    # -----------------------------------------

    sections = []
    current_category = None
    current_phrases = []

    for line in clean_lines:
        if line.startswith("###"):
            if current_category and current_phrases:
                sections.append({
                    "category": current_category,
                    "phrases": current_phrases
                })
                current_phrases = []

            # normalize title, remove ### and bold
            title_text = normalize_markdown_title(line)

            # split title to learn_lang and native_lang
            normalized_title = normalize_separator(title_text)
            parts = normalized_title.split(" - ", maxsplit=1)
            if len(parts) == 2:
                current_category = {
                    learn_lang: parts[0].strip(),
                    native_lang: parts[1].strip(),
                    default_en_lang: ""  # empty for now
                }
            else:
                current_category = {
                    learn_lang: title_text.strip(),
                    native_lang: title_text.strip(),
                    default_en_lang: "" # empty for now
                }
        else:
            # Extract metadata between %%...%%
            meta = extract_markdown_metadata(line)
            if meta:
                level, isword, enabled = meta
                phrase_line = remove_between(line, "%%").strip()
                phrase_line = normalize_separator(phrase_line)

                # Split translation pair
                parts = phrase_line.split(" - ", maxsplit=1)
                if len(parts) == 2:
                    left, right = parts[0].strip(), parts[1].strip()
                    translations = {
                        learn_lang: left,
                        native_lang: right,
                        default_en_lang: "" # empty for now
                    }
                    current_phrases.append({
                        "level": level,
                        "enabled": enabled,
                        "isword": isword,
                        "translations": translations
                    })

    if current_category and current_phrases:
        sections.append({
            "category": current_category,
            "phrases": current_phrases
        })

    ensure_dir(str(json_output_path.parent))
    
    with open(json_output_path, "w", encoding="utf-8") as f:
        json.dump(sections, f, ensure_ascii=False, indent=4)

    print(f"Created JSON file : {json_output_path}")
    

def Convert_json2csv(json_input_path: str, csv_output_path: str) -> None:
    """
    Loads a JSON file and converts it to a CSV file in a flat format.

    Each phrase becomes a row. Categories are visually separated with an empty row.

    Args:
        json_input_path (str): Path to the input JSON file.
        csv_output_path (str): Path to save the generated CSV file.
    """
    
    print("start Convert_json2csv")
    
    json_input_path = Path(json_input_path)
    csv_output_path = Path(csv_output_path)

    if not json_input_path.exists():
        raise FileNotFoundError(f"JSON file does not exist: {json_input_path}")

    with open(json_input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(csv_output_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)

        for category_block in data:
            category = category_block.get("category", {})
            phrases = category_block.get("phrases", [])

            # Write category as a row with translations, no metadata
            writer.writerow([
                "", "", "",  # empty: level, isword, enabled
                category.get("hu", ""),
                category.get("sr", ""),
                category.get("en", "")
            ])

            # Write all phrases for the category
            for phrase in phrases:
                writer.writerow([
                    phrase.get("level", ""),
                    "Yes" if phrase.get("isword", False) else "No",
                    "Yes" if phrase.get("enabled", False) else "No",
                    phrase["translations"].get("hu", ""),
                    phrase["translations"].get("sr", ""),
                    phrase["translations"].get("en", ""),
                ])

            # Blank row to separate categories
            writer.writerow([])
            

def Convert_json2xlsx(json_path: str, xlsx_path: str) -> None:
    print("start Convert_json2xlsx")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    wb = Workbook()
    ws = wb.active

    category_font = Font(size=13, bold=True)
    phrase_font = Font(size=12, bold=False)

    # blue fill on category
    category_fill = PatternFill(
        fill_type="solid",
        fgColor="D9EAF7"
    )
    
    # Red fill for enabled = false (0)
    red_fill = PatternFill(
        fill_type="solid",
        fgColor="FFC7CE"  # svetlo crvena
    )

    # Green fill for enabled = true (1)
    green_fill = PatternFill(
        fill_type="solid",
        fgColor="C6EFCE"  # svetlo zelena
    )

    # Grey border between cells
    gray_border = Border(
        left=Side(style="thin", color="B0B0B0"),
        right=Side(style="thin", color="B0B0B0"),
        top=Side(style="thin", color="B0B0B0"),
        bottom=Side(style="thin", color="B0B0B0")
    )


    # header row 
    header_row = ["Enabled","Level", "IsWord", "HU", "SR", "EN"]
    ws.append(header_row)
    ws.freeze_panes = "A2"

    # Set fixed with on languages
    ws.column_dimensions["D"].width = 30  # HU
    ws.column_dimensions["E"].width = 30  # SR
    ws.column_dimensions["F"].width = 30  # EN

    # center every cell on header
    for cell in ws[1]:
        cell.alignment = Alignment(horizontal="center")

    for block in data:
        category = block["category"]
        phrases = block["phrases"]

        # CATEGORY ROW (no flags, just translations)
        category_row = [
            "", "", "", 
            category.get("hu", ""),
            category.get("sr", ""),
            category.get("en", "")
        ]
        ws.append(category_row)

        for cell in ws[ws.max_row]:
            cell.font = category_font
            cell.fill = category_fill
            cell.border = gray_border

        # PHRASE ROWS
        for phrase in phrases:
            row = [
                "1" if phrase.get("enabled", False) else "0",
                phrase.get("level", ""),
                "1" if phrase.get("isword", False) else "0",
                phrase["translations"].get("hu", ""),
                phrase["translations"].get("sr", ""),
                phrase["translations"].get("en", ""),
            ]
            ws.append(row)
            
            current_row = ws[ws.max_row]
            is_disabled = row[0] == "0"

            for i, cell in enumerate(ws[ws.max_row], start=1):
                
                # apply border
                cell.border = gray_border
                
                # center flags (first three column)
                cell.font = phrase_font
                if i in (1, 2, 3):  # columns: Enabled, Level, IsWord
                    cell.alignment = Alignment(horizontal="center")
                    
                # colorize if enabled flag = false
                if is_disabled:
                    cell.fill = red_fill
                else:
                    cell.fill = green_fill
                    
        # Empty row after each category section
        ws.append([])



    # Dodaj uslovno formatiranje koje reaguje na vrednost A u svakom redu
    max_row = ws.max_row
    ws.conditional_formatting.add(
        f"A2:F{max_row}",
        FormulaRule(formula=['AND(ISNUMBER($A2), $A2=1)'], fill=green_fill)
    )

    ws.conditional_formatting.add(
        f"A2:F{max_row}",
        FormulaRule(formula=['AND(ISNUMBER($A2), $A2=0)'], fill=red_fill)
    )

    wb.save(xlsx_path)
    