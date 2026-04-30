"""Entry point for the salah-calendar package."""

import subprocess
import sys
from pathlib import Path


def main():
    """Run the calendar generator."""
    generate_script = Path(__file__).parent / "generate.py"
    result = subprocess.run(
        [sys.executable, str(generate_script)],
        cwd=str(generate_script.parent),
    )
    raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
