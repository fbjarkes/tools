#!/usr/bin/env python3
"""Set each tool's "updated" date in index.html to the date of the last commit touching its folder.

A tool row looks like:
  <li><a href="my-tool/index.html">...<time datetime="YYYY-MM-DD">YYYY-MM-DD</time>...</a></li>
Rows whose folder has no commits yet are left alone. Prints the tools it changed.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX = ROOT / "index.html"
ROW = re.compile(r'(<li><a href="(?P<dir>[^"/]+)/index\.html">.*?<time datetime=")[^"]*(">)[^<]*(</time>)', re.S)


def last_commit_day(folder):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", folder],
                         cwd=ROOT, capture_output=True, text=True, check=True)
    return out.stdout.strip()


def main():
    html = INDEX.read_text()
    changed = []

    def fix(m):
        day = last_commit_day(m["dir"])
        if not day:
            return m[0]
        new = f"{m[1]}{day}{m[3]}{day}{m[4]}"
        if new != m[0]:
            changed.append(f"{m['dir']} -> {day}")
        return new

    html = ROW.sub(fix, html)
    if changed:
        INDEX.write_text(html)
        print("\n".join(changed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
