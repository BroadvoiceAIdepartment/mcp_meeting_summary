import os
import json
from typing import Any
from pathlib import Path

def _is_path_writable(path: str) -> bool:
    """Check if the given path is writable.
    
    Returns True if we can create/write files, False otherwise.
    """
    try:
        path_obj = Path(path)
        # Try to create a test file in the directory
        test_file = path_obj / ".write_test"
        if path_obj.exists():
            test_file.touch()
            test_file.unlink()
            return True
        else:
            # Try to create the directory
            path_obj.mkdir(parents=True, exist_ok=True)
            test_file.touch()
            test_file.unlink()
            return True
    except (OSError, PermissionError):
        return False

#Dump the data to a file
def maybe_dump(path: str | None, name: str, data: Any) -> None:
    """Dump data to a file if the filesystem is writable.
    
    In read-only filesystem environments (e.g., FastMCP Cloud), this function
    silently skips dumping to avoid errors. Debug dumps are non-critical.
    """
    if not path:
        return
    
    # Check if filesystem is writable before attempting to write
    if not _is_path_writable(path):
        # Silently skip dumping in read-only environments
        return
    
    try:
        os.makedirs(path, exist_ok=True)
        file = os.path.join(path, name)
        with open(file, "w", encoding="utf-8") as f:
            if isinstance(data, str):
                # Write text (e.g., Markdown) as-is to preserve formatting
                f.write(data)
            else:
                f.write(json.dumps(data, indent=2, ensure_ascii=False))
    except (OSError, PermissionError):
        # Silently fail if write still fails (e.g., race condition or permission change)
        pass


def collect_fix_versions(projects: Any) -> list[str]:
    """Collect non-empty fixVersion strings from a list of project-like objects.

    Each element can be a dict with key "fixVersion" or an object with attribute "fixVersion".
    """
    vals: list[str] = []
    if not projects:
        return vals
    try:
        for p in projects:
            v = p.get("fixVersion") if isinstance(p, dict) else getattr(p, "fixVersion", "")
            if v:
                vals.append(str(v))
    except Exception:
        # Best-effort collection; ignore malformed entries
        pass
    return vals
