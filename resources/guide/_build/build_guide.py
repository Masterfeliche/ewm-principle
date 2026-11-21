"""Build the visual guide page from docs/GUIDE.md.

Usage, from the repository root:
    python resources/guide/_build/build_guide.py

Writes two files in resources/guide/:
    emw-workflow-guide.html           open this one in a browser
    emw-workflow-guide.artifact.html  the same page without a doctype, for publishing as an artifact
"""
import json
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[2]
guide = (root / "docs" / "GUIDE.md").read_text(encoding="utf-8")
payload = json.dumps(guide, ensure_ascii=False).replace("</", "<\\/")
page = (here / "guide_template.html").read_text(encoding="utf-8").replace('/*__GUIDE__*/""', payload)

out_dir = here.parent
(out_dir / "emw-workflow-guide.artifact.html").write_text(page, encoding="utf-8", newline="\n")
doctype = ('<!doctype html>\n<html lang="en">\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
(out_dir / "emw-workflow-guide.html").write_text(doctype + page, encoding="utf-8", newline="\n")
print(f"built {out_dir / 'emw-workflow-guide.html'} ({len(page) // 1024} KB)")
