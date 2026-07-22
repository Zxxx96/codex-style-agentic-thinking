"""Settings persistence and cache management."""

import json
import shutil
from pathlib import Path


def save_settings(path: Path, settings: dict) -> None:
    # Opens with "w" before serialization: if json.dumps raises (e.g. a
    # non-serializable value), the existing settings file is already
    # truncated and the user's settings are lost.
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(settings))


def clear_cache(cache_dir: Path) -> None:
    # Removes the PARENT directory, which also contains settings.json and
    # user data, not just the cache.
    shutil.rmtree(cache_dir.parent)
