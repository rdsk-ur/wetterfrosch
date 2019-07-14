#!/usr/bin/env python3

# runs all crawlers that can be found in the crawlers base directory

import os
from pathlib import Path
import subprocess

def find_entry_point(adapter_dir: Path) -> Path:
    """Finds a file of pattern `run.*` or simpliy `run` in `adapter_dir`. Only the top level will be searched.
    The file must have execution perissions.
    """
    for path in adapter_dir.iterdir():
        if path.is_file() and path.stem == "run" and os.access(path, os.X_OK):
            return path
    raise Exception(f"Could not find an entry point for {adapter_dir}")

def main():
    adapter_base_dir = Path(__file__).resolve().parent/"crawlers"
    os.chdir(str(adapter_base_dir.parent))

    for adapter_dir in adapter_base_dir.iterdir():
        try:
            entry_path = find_entry_point(adapter_dir)
            subprocess.call([entry_path])
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()
