"""Build the tabbed four-report artifact page from the Markdown reports.
Usage: python build_guide.py <reports_dir> <out_html>
"""
import json, sys
from pathlib import Path

reports_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
files = {
    "php": "PHP ecosystem mastery path.md",
    "dotnet": "Dotnet ecosystem mastery path.md",
    "go": "Go ecosystem mastery path.md",
    "python": "Python ecosystem mastery path.md",
    "east-africa": "East Africa software problems for PHP projects.md",
}
data = {k: (reports_dir / v).read_text(encoding="utf-8") for k, v in files.items()}
payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
template = Path(__file__).with_name("guide_template.html").read_text(encoding="utf-8")
out.write_text(template.replace("/*__REPORTS__*/{}", payload), encoding="utf-8")
print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
