# Install prompt: List Builder: Apollo

End-to-end prospect lists through your connected Apollo account. Nothing that costs credits runs without your yes.

Copy everything in the box and paste it into a Claude chat (the Claude desktop app, with Code execution switched on under Settings → Capabilities).

```text
Please install List Builder: Apollo, a sales skill from Kingsbury & Marshall. It's published openly on GitHub at github.com/SamKingsbury2132/kingsbury-marshall-skills (folder plugins/list-builder-apollo/skills/list-builder-apollo), so you can read every file first.

Claude, please follow these steps. If any step fails, stop and tell me plainly what failed and what I should do next. Don't switch to a different install method, don't use a save_skill tool, and don't write any skill content from your own knowledge.

1. Check what you can do here. If you can run shell commands but can't present files to me, this is Claude Code: do steps 2 to 4, then copy the folder to ~/.claude/skills/list-builder-apollo/ (SKILL.md at its top level, replacing any older copy) and finish with: "Installed to ~/.claude/skills/list-builder-apollo. It's live from your next message." If you can't run shell commands at all (a browser tab or phone), stop and tell me this install needs the Claude desktop app with Code execution switched on under Settings → Capabilities.
2. Download https://github.com/SamKingsbury2132/kingsbury-marshall-skills/archive/refs/heads/main.zip with curl -fL and a 60-second timeout. If the link arrived mangled (a trailing full stop, smart quotes, a line break), fix it to exactly that form and retry once. If it fails with 403 or a timeout, tell me to open that link in my own browser and drag the downloaded zip into this chat, then carry on with that file.
3. Unzip it and take the folder plugins/list-builder-apollo/skills/list-builder-apollo. Check that SKILL.md and scripts/build_coldlist_dashboard.py are both there (the folder normally holds 8 files, counted recursively). If they're not, stop and tell me: "The files on GitHub don't match this install prompt. Ask Kingsbury & Marshall for the current one."
4. Read SKILL.md and every script in the folder. In a few plain lines, tell me what the skill does, what it saves on my computer, and whether anything in it concerns you. Only carry on if it looks safe to you.
5. If I already have a saved copy of this skill with my own extra files in it (such as LOCAL.md), copy those into the new folder and tell me you kept them.
6. Zip the folder's contents as list-builder-apollo.skill with SKILL.md at the top level of the archive, not inside a subfolder. Check the archive listing shows SKILL.md at the root.
7. Save the file to your outputs folder and present it to me so I can click Save skill (it says Update skill if I already had it).
8. Close with one line on how to start it: connect Apollo to Claude (Settings → Connectors), then say "build me a prospect list".

You may be asked to approve steps along the way. That's you staying in control: approve what you're comfortable with. Nothing installs until you click Save skill.
```

**Prompt not working?** Download [`dist/list-builder-apollo.skill`](../dist/list-builder-apollo.skill) and add it under Settings → Capabilities → Skills → Upload skill.

**Start it:** connect Apollo to Claude (Settings → Connectors), then say "build me a prospect list".
