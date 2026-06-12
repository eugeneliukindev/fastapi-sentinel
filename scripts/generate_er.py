#!/usr/bin/env -S uv run --group docs python
import sys
from pathlib import Path

from eralchemy import render_er

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))


from src.models import BaseOrm  # noqa: E402

_OUTPUT = BASE_DIR / "docs" / "er_diagram.png"


def main() -> None:
    _OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    old_content = _OUTPUT.read_bytes() if _OUTPUT.exists() else b""
    render_er(BaseOrm.metadata, str(_OUTPUT), title="FastAPI JWT ER Diagram")
    if _OUTPUT.read_bytes() != old_content:
        sys.exit(1)


if __name__ == "__main__":
    main()
