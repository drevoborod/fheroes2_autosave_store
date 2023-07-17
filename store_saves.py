#!/usr/bin/env python3

from pathlib import Path
import re
import shutil
import time


FILENAME = "AUTOSAVE"
FILEEXTENSION = "sav"
SOURCEDIR = "save"        # where source file is stored
STOREDIR = "save_backup"
MAX_SAVES = 100
POLLING_INTERVAL = 0.3  # seconds


def create_storedir(dirname: str) -> Path:
    store_dir = Path(dirname)
    if not store_dir.exists():
        store_dir.mkdir()
    return store_dir


def find_last_save_number(store_dir: Path) -> int:
    numbers = []
    for f in store_dir.glob(f"*.{FILEEXTENSION}"):
        if match_object := re.match(f"{FILENAME}_(\\d+)", f.stem):
            numbers.append(int(match_object.groups()[0]))
    last = max(numbers, default=0)
    if last < MAX_SAVES:
        return last + 1
    return 1


def copy_save(sourcefile: Path, store_dir: Path, current_number: int):
    shutil.copy(sourcefile, store_dir.joinpath(f"{FILENAME}_{current_number}.{FILEEXTENSION}"))


def store_forever():
    source_file = Path(SOURCEDIR).joinpath(f"{FILENAME}.{FILEEXTENSION}")
    store_dir = create_storedir(STOREDIR)
    current_number = find_last_save_number(store_dir)
    modification_time = source_file.stat().st_mtime
    while True:
        if modification_time != source_file.stat().st_mtime:
            print(current_number)
            modification_time = source_file.stat().st_mtime
            copy_save(source_file, store_dir, current_number)
            if current_number >= MAX_SAVES:
                current_number = 1
            else:
                current_number += 1
        time.sleep(POLLING_INTERVAL)


if __name__ == "__main__":
    store_forever()