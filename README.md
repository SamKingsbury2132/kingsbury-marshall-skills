# Kingsbury & Marshall — sales suite for Claude

5 skills for Claude (the desktop app / Cowork, and Claude Code) that do real sales work.
Each one is its own plugin, so install only the ones you want.

| Skill | What it does | Install |
|---|---|---|
| **AI Sales Brain** | Five quick questions that teach every K&M skill who you are, who you sell to and what you offer. | [install prompt](install/sales-brain-setup.md) · [.skill file](dist/sales-brain-setup.skill) |
| **Company Researcher** | Researches one company or a list of thousands into ranked cheat sheets: what they do, why now, and the angle to use. | [install prompt](install/company-researcher.md) · [.skill file](dist/company-researcher.skill) |
| **List Builder: Apollo** | End-to-end prospect lists through your connected Apollo account. Nothing that costs credits runs without your yes. | [install prompt](install/list-builder-apollo.md) · [.skill file](dist/list-builder-apollo.skill) |
| **Cold Email Builder** | Writes a cold email for you, or scores and rebuilds the one you have, on a rubric calibrated against real replies. | [install prompt](install/cold-email-builder.md) · [.skill file](dist/cold-email-builder.skill) |
| **Sales Control Panel** | Reads any deals export and shows what to do in the next hour, and whether your pipeline can be trusted. | [install prompt](install/sales-control-panel.md) · [.skill file](dist/sales-control-panel.skill) |

## Install

**Easiest:** open the skill's install prompt, copy the box, and paste it into a chat in the Claude desktop app.
Claude downloads the skill from this repo, checks it, and hands you a file. Click **Save skill**. In Claude Code
it installs itself.

**Before you start:** you need the Claude desktop app ([claude.com/download](https://claude.com/download)) on a
paid plan, with **Code execution and file creation** switched on under Settings → Capabilities.

**Marketplace:** Settings → Plugins → Add marketplace → `SamKingsbury2132/kingsbury-marshall-skills` → install the skills you want.

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
