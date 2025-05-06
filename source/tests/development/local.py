import json
import os


BR = "\n"


def check_settings_for_init_exclusion(settings_path=".vscode/settings.json"):
    if not os.path.exists(settings_path):
        print(f"File not found: {settings_path}")
        return
    try:
        with open(settings_path, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    files_exclude = settings.get("files.exclude", {})
    for pattern, excluded in files_exclude.items():
        if "**/__init__.py" in pattern and excluded:
            plus_n = BR + BR + "+ " * 40 + BR + BR
            message = "Warning: '__init__.py' is excluded in '.vscode/files.exclude'!"
            print(plus_n, message, plus_n)
            return


if __name__ == "__main__":
    check_settings_for_init_exclusion()
