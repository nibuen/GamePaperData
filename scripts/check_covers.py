#!/usr/bin/env python3
"""Guard against a game silently shipping with no cover art.

Covers are sourced by the `/add-game` agent step (there is no automated fetch),
so it's easy for one to slip through -- this makes that impossible to miss.

Non-blocking by design: emits GitHub `::warning::` annotations + a job summary
listing every registry game with no `cover.jpg`/`cover.webp`, but exits 0 so it
never gates a merge (a legacy gap shouldn't hold up unrelated data PRs). Flip the
final exit to 1 if you later want it to hard-fail once every game has a cover.
"""
import json
import os
import sys

with open("registry.json", encoding="utf-8") as f:
    registry = json.load(f)

missing = []
for game in registry.get("games", []):
    gid = game["id"]
    has_cover = os.path.exists(f"files/{gid}/cover.jpg") or os.path.exists(
        f"files/{gid}/cover.webp"
    )
    if not has_cover:
        missing.append((gid, game.get("game_name", gid)))

lines = []
if missing:
    lines.append(f"### WARNING: {len(missing)} game(s) missing cover art")
    for gid, name in missing:
        print(
            f"::warning title=Missing cover art::{name} ({gid}) has no "
            f"cover.jpg or cover.webp"
        )
        lines.append(f"- **{name}** (`{gid}`)")
    lines.append("")
    lines.append(
        "Covers are sourced by the `/add-game` agent (publisher box front) -- "
        "add `files/<id>/cover.jpg` + `cover.webp`. The compress-json workflow "
        "then generates the OG card with the cover."
    )
else:
    lines.append("### All games have cover art")

report = "\n".join(lines)
print(report)
summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
if summary_path:
    with open(summary_path, "a", encoding="utf-8") as f:
        f.write(report + "\n")

# Non-blocking: surface loudly, do not fail the build.
sys.exit(0)
