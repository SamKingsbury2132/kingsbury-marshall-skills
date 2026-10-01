"""Package the K&M sales suite: .skill files, install prompts, README and marketplace.json.

Run from km-sales-skills/:  python3 tools/package.py
Change REPO below if the GitHub repo name changes, then re-run.
"""
import json
import zipfile
from pathlib import Path

REPO = "SamKingsbury2132/kingsbury-marshall-skills"
ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"

SKILLS = [
    # slug, display name, key file to verify, one-line pitch, how to start it
    ("sales-brain-setup", "AI Sales Brain", "scripts/install_capture_rule.py",
     "Five quick questions that teach every K&M skill who you are, who you sell to and what you offer.",
     'type /sales-brain-setup or say "get me started". Do this one first: the other skills read what it learns.'),
    ("company-researcher", "Company Researcher", "scripts/scan_runner.py",
     "Researches one company or a list of thousands into ranked cheat sheets: what they do, why now, and the angle to use.",
     'say "research [company name]", or drop in a spreadsheet of companies and say "scan these".'),
    ("list-builder-apollo", "List Builder: Apollo", "scripts/build_coldlist_dashboard.py",
     "End-to-end prospect lists through your connected Apollo account. Nothing that costs credits runs without your yes.",
     'connect Apollo to Claude (Settings → Connectors), then say "build me a prospect list".'),
    ("cold-email-builder", "Cold Email Builder", "scripts/meter.py",
     "Writes a cold email for you, or scores and rebuilds the one you have, on a rubric calibrated against real replies.",
     'say "write me a cold email", or paste one you wrote and say "grade this".'),
    ("sales-control-panel", "Sales Control Panel", "scripts/build_panel.py",
     "Reads any deals export and shows what to do in the next hour, and whether your pipeline can be trusted.",
     'drop your deals spreadsheet (Excel or CSV from your CRM) into a chat and say "is my pipeline ok?" No data yet? Say "show me the demo".'),
]

ZIP_URL = f"https://github.com/{REPO}/archive/refs/heads/main.zip"


def build_skill_file(slug):
    src = PLUGINS / slug / "skills" / slug
    out = ROOT / "dist" / f"{slug}.skill"
    out.parent.mkdir(exist_ok=True)
    files = sorted(p for p in src.rglob("*") if p.is_file() and "__pycache__" not in p.parts and not p.name.startswith("."))
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.relative_to(src).as_posix())
    names = zipfile.ZipFile(out).namelist()
    assert "SKILL.md" in names, f"{slug}: SKILL.md not at archive root"
    return len(files), out.stat().st_size


def prompt(slug, name, key, n_files, start):
    return f"""Please install {name}, a sales skill from Kingsbury & Marshall. It's published openly on GitHub at github.com/{REPO} (folder plugins/{slug}/skills/{slug}), so you can read every file first.

Claude, please follow these steps. If any step fails, stop and tell me plainly what failed and what I should do next. Don't switch to a different install method, don't use a save_skill tool, and don't write any skill content from your own knowledge.

1. Check what you can do here. If you can run shell commands but can't present files to me, this is Claude Code: do steps 2 to 4, then copy the folder to ~/.claude/skills/{slug}/ (SKILL.md at its top level, replacing any older copy) and finish with: "Installed to ~/.claude/skills/{slug}. It's live from your next message." If you can't run shell commands at all (a browser tab or phone), stop and tell me this install needs the Claude desktop app with Code execution switched on under Settings → Capabilities.
2. Download {ZIP_URL} with curl -fL and a 60-second timeout. If the link arrived mangled (a trailing full stop, smart quotes, a line break), fix it to exactly that form and retry once. If it fails with 403 or a timeout, tell me to open that link in my own browser and drag the downloaded zip into this chat, then carry on with that file.
3. Unzip it and take the folder plugins/{slug}/skills/{slug}. Check that SKILL.md and {key} are both there (the folder normally holds {n_files} files, counted recursively). If they're not, stop and tell me: "The files on GitHub don't match this install prompt. Ask Kingsbury & Marshall for the current one."
4. Read SKILL.md and every script in the folder. In a few plain lines, tell me what the skill does, what it saves on my computer, and whether anything in it concerns you. Only carry on if it looks safe to you.
5. If I already have a saved copy of this skill with my own extra files in it (such as LOCAL.md), copy those into the new folder and tell me you kept them.
6. Zip the folder's contents as {slug}.skill with SKILL.md at the top level of the archive, not inside a subfolder. Check the archive listing shows SKILL.md at the root.
7. Save the file to your outputs folder and present it to me so I can click Save skill (it says Update skill if I already had it).
8. Close with one line on how to start it: {start}

You may be asked to approve steps along the way. That's you staying in control: approve what you're comfortable with. Nothing installs until you click Save skill."""


def main():
    rows, plugins = [], []
    (ROOT / "install").mkdir(exist_ok=True)
    for slug, name, key, pitch, start in SKILLS:
        assert (PLUGINS / slug / "skills" / slug / key).exists(), f"{slug}: {key} missing"
        n, size = build_skill_file(slug)
        p = prompt(slug, name, key, n, start)
        (ROOT / "install" / f"{slug}.md").write_text(
            f"# Install prompt: {name}\n\n{pitch}\n\nCopy everything in the box and paste it into a Claude chat "
            f"(the Claude desktop app, with Code execution switched on under Settings → Capabilities).\n\n"
            f"```text\n{p}\n```\n\n**Prompt not working?** Download [`dist/{slug}.skill`](../dist/{slug}.skill) "
            f"and add it under Settings → Capabilities → Skills → Upload skill.\n\n**Start it:** {start}\n")
        rows.append(f"| **{name}** | {pitch} | [install prompt](install/{slug}.md) · [.skill file](dist/{slug}.skill) |")
        plugins.append({"name": slug, "source": f"./plugins/{slug}", "description": pitch, "category": "sales"})
        print(f"{slug:22} {n:3} files  {size/1024:7.1f} KB")
    (ROOT / ".claude-plugin").mkdir(exist_ok=True)
    (ROOT / ".claude-plugin" / "marketplace.json").write_text(json.dumps({
        "name": "kingsbury-marshall-skills",
        "owner": {"name": "Kingsbury & Marshall", "url": "https://kingsbury-marshall-website.vercel.app"},
        "description": "The Kingsbury & Marshall sales suite for Claude. Install only the ones you want.",
        "plugins": plugins}, indent=2, ensure_ascii=False) + "\n")
    (ROOT / "README.md").write_text(f"""# Kingsbury & Marshall — sales suite for Claude

{len(SKILLS)} skills for Claude (the desktop app / Cowork, and Claude Code) that do real sales work.
Each one is its own plugin, so install only the ones you want.

| Skill | What it does | Install |
|---|---|---|
{chr(10).join(rows)}

## Install

**Easiest:** open the skill's install prompt, copy the box, and paste it into a chat in the Claude desktop app.
Claude downloads the skill from this repo, checks it, and hands you a file. Click **Save skill**. In Claude Code
it installs itself.

**Before you start:** you need the Claude desktop app ([claude.com/download](https://claude.com/download)) on a
paid plan, with **Code execution and file creation** switched on under Settings → Capabilities.

**Marketplace:** Settings → Plugins → Add marketplace → `{REPO}` → install the skills you want.

**By hand:** download a `.skill` file from `dist/` and add it under Settings → Capabilities → Skills → Upload skill.

## Start here

Install **AI Sales Brain** first and say **"get me started"**. Five quick questions teach every other skill who you
are and what you sell.

## What gets saved on your computer

The skills keep their memory in a `Claude HQ` folder in your working folder: your sales profile, and a dated copy
of the emails and research they produce (the `ledger` folder). Nothing is sent anywhere. AI Sales Brain offers to
add a short rule to your folder's `CLAUDE.md` so other chats keep your profile up to date, and asks before
creating that file.

## Credits

Adapted from [bingley-ai/bingley-skills](https://github.com/bingley-ai/bingley-skills) (MIT). The original
copyright notice is kept in `LICENSE`.
""")


if __name__ == "__main__":
    main()
