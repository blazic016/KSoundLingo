import json
from pathlib import Path
from kslingo.utils.fs import ensure_dir


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
        lines.append(f"### **{cat_learn} - {cat_native}**")

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
