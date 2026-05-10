import os
import sys
import subprocess
import tomllib
from pathlib import Path

DEFAULT_SYSTEM_CONFIG = Path("/etc/cpustate.conf")
DEFAULT_USER_CONFIG = Path.home() / ".config" / "cpustate.conf"

EXAMPLE_CONFIG = """\
[cpu]
governor = "performance"
epp = "balance_performance"

# [ryzenadj]
# stapm-limit = 25000
# fast-limit = 28000
# slow-limit = 25000
# tctl-temp = 95

# [profiles.battery]
# governor = "powersave"
# epp = "power"
# stapm-limit = 15000

# [profiles.gaming]
# governor = "performance"
# epp = "performance"
# stapm-limit = 35000
"""


def config_path() -> Path:
    """Return the first config file that exists, preferring user over system."""
    if DEFAULT_USER_CONFIG.exists():
        return DEFAULT_USER_CONFIG
    if DEFAULT_SYSTEM_CONFIG.exists():
        return DEFAULT_SYSTEM_CONFIG
    return DEFAULT_USER_CONFIG


def load() -> dict:
    path = config_path()
    if not path.exists():
        print(f"[cpustate] No config found at {path}. Creating example config.")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(EXAMPLE_CONFIG)
        print(f"[cpustate] Edit {path} then run 'cpustate apply'.")
        sys.exit(0)

    with open(path, "rb") as f:
        try:
            return tomllib.load(f)
        except tomllib.TOMLDecodeError as e:
            print(f"[cpustate] Config parse error in {path}:\n  {e}")
            sys.exit(1)


def edit():
    path = config_path()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(EXAMPLE_CONFIG)
        print(f"[cpustate] Created example config at {path}")

    editor = os.environ.get("EDITOR", "vim")
    subprocess.run([editor, str(path)])