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
    

def Convert_md2json(input, output_path, learn, native):
    print("start Convert_json_to_markdown")
    print(f"input={input} output_path={output_path} learn={learn} native={native}")
