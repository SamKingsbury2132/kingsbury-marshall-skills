"""One-off text rebrand of the Bingley skills into Kingsbury & Marshall versions.

Run from km-sales-skills/:  python3 tools/rebrand_text.py
Safe to re-run: every edit checks for its source text first.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "plugins"
SKILLS = ["sales-control-panel", "list-builder-apollo", "company-researcher", "sales-brain-setup", "cold-email-builder"]
DISPLAY = {
    "sales-control-panel": "Sales Control Panel",
    "list-builder-apollo": "List Builder: Apollo",
    "company-researcher": "Company Researcher",
    "sales-brain-setup": "AI Sales Brain",
    "cold-email-builder": "Cold Email Builder",
}
SHELLS = {
    "sales-control-panel": "scripts/panel-shell.html",
    "list-builder-apollo": "scripts/assets/coldlist-shell.html",
    "company-researcher": "assets/cheatsheet-template.html",
    "cold-email-builder": "references/scorecard-template.html",
}
VERSION = "1.0.0"

# Specific phrases first (order matters), then a generic sweep.
PHRASES = [
    ("Bingley’s talking points", "Talking points"),
    ("Bingley's talking points", "Talking points"),
    ("BINGLEY'S TALKING POINTS", "TALKING POINTS"),
    ("Ask Bingley...", "Ask Claude..."),
    ("Bingley’s activity →", "Claude’s activity →"),
    ("Copy answers for Bingley", "Copy answers for Claude"),
    ("Caroline Bingley", "Caroline Ashworth"),
    ("bingley-refined-v2.html", "desk-v4"),
    ("(bingley-refined-v2)", ""),
    ("bingley-refined-v2", "desk-v4"),
    ('<style id="bingley-interactions">', '<style id="km-interactions">'),
    ('id="bingley-v3-shell"', 'id="km-v3-shell"'),
    ("Bingley cold-list dashboard", "K&M cold-list dashboard"),
    ("real Bingley desk shell", "K&M desk shell"),
    ("genuine Bingley desk shell", "K&M desk shell"),
    ("Bingley desk shell", "K&M desk shell"),
    ("Bingley room template", "K&M room template"),
    ("every Bingley room", "every K&M room"),
    ("from its Bingley", "from its K&M"),
    ("(the Bingley", "(the K&M"),
    ('"bingley shell"', '"km shell"'),
    ("every other Bingley skill", "every other Kingsbury & Marshall sales skill"),
    ("a free sales skill from bingley.ai", "a sales skill from Kingsbury & Marshall"),
]
GENERIC = [(re.compile(r"\bBingley\b"), "Claude"), (re.compile(r"\bBINGLEY\b"), "KINGSBURY & MARSHALL")]

STAMP = """## Version stamp (house rule)

**Stamp.** The close-out of every run states this skill's name and version, read from the `version:` frontmatter at the top of this file (e.g. "{slug} v{v} · Kingsbury & Marshall").

"""


def cut_section(text, heading):
    """Remove a '## ' section (heading line to the next '## ' heading or EOF)."""
    i = text.find(heading)
    if i < 0:
        return text, False
    m = re.search(r"\n## ", text[i + len(heading):])
    j = i + len(heading) + m.start() + 1 if m else len(text)
    return text[:i] + text[j:], True


def rebrand_skill_md(slug):
    p = ROOT / slug / "skills" / slug / "SKILL.md"
    t = p.read_text()
    t = re.sub(r"^version: .*$", f"version: {VERSION}", t, count=1, flags=re.M)
    head = "## Version stamp + update check (house rule)"
    if head in t:
        i = t.index(head)
        t, _ = cut_section(t, head)
        t = t[:i] + STAMP.format(slug=slug, v=VERSION) + t[i:]
    if slug == "sales-control-panel":
        a = t.find("## Before you change the engine — MAINTAINER REPO ONLY")
        if a >= 0:
            end = "Then run `/skill-test` as the launch gate.\n"
            b = t.index(end, a) + len(end)
            t = t[:a] + t[b:]
    p.write_text(t)


def strip_rating_strip(t):
    t = re.sub(r'<div class="office" id="officeStrip"[^>]*><div class="office-ask"><span class="office-lbl"></span>'
               r'<span class="office-pips" id="officePips"></span></div><div class="office-done">'
               r'<span class="office-tick">&#10003;</span><span>Thanks</span></div></div>', "", t)
    a = t.find("/* Rate-this-skill strip")
    if a >= 0:
        b = t.index("})();\n", a) + len("})();\n")
        assert b - a < 3000, "rating IIFE bounds look wrong"
        t = t[:a] + t[b:]
    return t


def sweep(path):
    t = path.read_text()
    o = t
    for a, b in PHRASES:
        t = t.replace(a, b)
    for rx, b in GENERIC:
        t = rx.sub(b, t)
    if t != o:
        path.write_text(t)


def main():
    for slug in SKILLS:
        base = ROOT / slug
        pj = base / ".claude-plugin" / "plugin.json"
        d = json.loads(pj.read_text())
        d["version"] = VERSION
        d["displayName"] = DISPLAY[slug]
        d["author"] = {"name": "Kingsbury & Marshall"}
        d["homepage"] = "https://kingsbury-marshall-website.vercel.app"
        d["description"] = d["description"].replace("every other Bingley skill", "every other Kingsbury & Marshall sales skill")
        pj.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n")
        rebrand_skill_md(slug)
        if slug in SHELLS:
            sp = base / "skills" / slug / SHELLS[slug]
            sp.write_text(strip_rating_strip(sp.read_text()))
        for f in base.rglob("*"):
            if f.is_file() and f.suffix in {".md", ".py", ".html", ".js", ".json"}:
                sweep(f)
    left = [str(f.relative_to(ROOT)) for f in ROOT.rglob("*") if f.is_file() and re.search("bingley", f.read_text(errors="ignore"), re.I)]
    print("files still mentioning bingley:", left or "none")


if __name__ == "__main__":
    main()
