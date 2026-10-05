"""打印 hub 测试题的 id 和 prompt（不含 expected），供实测者取题。

用法：python evals/tools/get_prompts.py 1,2,3
"""
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PROMPTS = Path(__file__).resolve().parents[2] / "skills" / "cross-system-hub" / "test-prompts.json"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("用法：python evals/tools/get_prompts.py 1,2,3")
    ids = {int(x) for x in sys.argv[1].split(",") if x.strip()}
    cases = json.loads(PROMPTS.read_text(encoding="utf-8"))
    for c in cases:
        if c["id"] in ids:
            print(c["id"], ":", c["prompt"])


if __name__ == "__main__":
    main()
