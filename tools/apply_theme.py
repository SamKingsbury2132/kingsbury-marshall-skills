"""Apply the Kingsbury & Marshall house theme to every K&M room shell.

Run from km-sales-skills/:  python3 tools/apply_theme.py
Idempotent: re-running swaps in the latest tools/km-theme.css and sidebar.
"""
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent / "plugins"
THEME = (HERE / "km-theme.css").read_text().strip()

# The suite as shown in the sidebar, in order. Labels only (not links).
SUITE = [
    ("sales-brain-setup", "AI Sales Brain"),
    ("company-researcher", "Company Researcher"),
    ("list-builder-apollo", "List Builder"),
    ("cold-email-builder", "Cold Email Builder"),
    ("sales-control-panel", "Sales Control Panel"),
]
SHELLS = {
    "sales-control-panel": ("scripts/panel-shell.html", "Sales Control Panel"),
    "list-builder-apollo": ("scripts/assets/coldlist-shell.html", "List Builder"),
    "company-researcher": ("assets/cheatsheet-template.html", "Company Researcher"),
    "cold-email-builder": ("references/scorecard-template.html", "Cold Email Builder"),
}
VERSION = "1.0.0"


def sidebar(active, name):
    items = "\n".join(
        f'<li class="{"on" if slug == active else ""}"><span class="ix">{i:02d}</span>{label}</li>'
        for i, (slug, label) in enumerate(SUITE, 1)
    )
    return f'''<!-- KM-SIDE:BEGIN -->
<nav class="km-side" aria-label="Kingsbury &amp; Marshall sales suite">
<div class="km-mark">Kingsbury <span class="amp">&amp;</span><br>Marshall</div>
<div class="km-sub">Sales suite for Claude</div>
<div class="km-sec">The suite</div>
<ul class="km-suite">
{items}
</ul>
<div class="km-side-foot">Built by Kingsbury &amp; Marshall<br><a href="https://kingsbury-marshall-website.vercel.app" target="_blank" rel="noopener">Visit our website</a></div>
</nav>
<div class="km-date" id="kmDate"></div>
<div class="km-colophon"><b>Kingsbury &amp; Marshall</b><i></i>{name}<i></i>v{VERSION}</div>
<script>(function(){{var d=document.getElementById("kmDate");if(d)d.textContent=new Date().toLocaleDateString(undefined,{{weekday:"long",day:"numeric",month:"long"}});}})();</script>
<!-- KM-SIDE:END -->'''


def apply(slug):
    rel, name = SHELLS[slug]
    p = ROOT / slug / "skills" / slug / rel
    t = p.read_text()
    t = re.sub(r"<title>.*?</title>", f"<title>{name} · Kingsbury &amp; Marshall</title>", t, count=1)
    # drop old rails (first run) or old K&M sidebar (re-run)
    t = re.sub(r'<aside class="side left">.*?</aside>\s*<aside class="side right">.*?</aside>', "<!--KM-SIDE-->", t, count=1, flags=re.S)
    t = re.sub(r"<!-- KM-SIDE:BEGIN -->.*?<!-- KM-SIDE:END -->", "<!--KM-SIDE-->", t, count=1, flags=re.S)
    assert t.count("<!--KM-SIDE-->") == 1, f"{slug}: sidebar anchor not found"
    t = t.replace("<!--KM-SIDE-->", sidebar(slug, name))
    # theme block, last thing before </body>
    t = re.sub(r'<style id="km-theme">.*?</style>\s*', "", t, flags=re.S)
    assert t.count("</body>") == 1, f"{slug}: expected one </body>"
    t = t.replace("</body>", THEME + "\n</body>")
    p.write_text(t)
    print("themed", p.relative_to(ROOT))


if __name__ == "__main__":
    for s in SHELLS:
        apply(s)
