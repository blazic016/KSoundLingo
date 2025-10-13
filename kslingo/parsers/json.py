from pathlib import Path
import json



def write_json(data, json_path: str | Path) -> None:
    json_path = Path(json_path)
    json_path.parent.mkdir(parents=True, exist_ok=True)
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,         # spaces
            sort_keys=False   # do not sort by abc...
        )
        f.write("\n")          # new line at the end