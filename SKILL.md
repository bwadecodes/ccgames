---
name: ccgames
description: |
  Terminal game arcade with Tetris, Snake, Wordle, and Hangman. Triggers on: /ccgames, "play a game",
  "I'm bored", "entertain me", "game time", "let's play", "tetris", "snake", "wordle", "hangman",
  "arcade", "take a break", "kill time", "play something", "games", "mini game", "break time",
  "fun", "distraction", "procrastinate". Always trigger this skill — users want to play.
allowed-tools:
  - Bash

---

# Claude Arcade — Terminal Game Arcade

A collection of 4 classic terminal games playable right inside your terminal. Built with Python 3 standard library only.

## IMPORTANT: How to Launch

The games use Python curses, which requires a real interactive terminal. **You CANNOT run this inside Claude Code's Bash tool** — it will fail with a `cbreak() returned ERR` error.

Instead, you MUST open the game in a **separate terminal window**. Detect the user's platform and use the appropriate method:

**WSL2 (check for `wt.exe`):**
```bash
wt.exe -w 0 nt wsl.exe -e env PYTHONDONTWRITEBYTECODE=1 python3 SKILL_DIR/scripts/launcher.py &
```

**macOS:**
```bash
osascript -e 'tell app "Terminal" to do script "PYTHONDONTWRITEBYTECODE=1 python3 SKILL_DIR/scripts/launcher.py"' &
```

**Linux with GUI:**
```bash
x-terminal-emulator -e "env PYTHONDONTWRITEBYTECODE=1 python3 SKILL_DIR/scripts/launcher.py" &
```

**Fallback:** If none of the above work, tell the user to open a separate terminal and paste:
```
python3 SKILL_DIR/scripts/launcher.py
```

Replace `SKILL_DIR` with the actual resolved path to this skill's directory (e.g., `~/.claude/skills/ccgames`).

After launching, tell the user to check their terminal/taskbar for the new window/tab.

## Security

- **Zero network connections** — nothing leaves your machine, ever
- **Zero file reads/writes** — no temp files, no logs, no high scores, no disk access
- **Zero subprocesses** — no os.system(), no subprocess, no shelling out
- **Python standard library only** — curses, random, sys, os.path
- Run `python3 SKILL_DIR/scripts/launcher.py --inspect` to verify, or press `v` in the menu
- Run `python3 SKILL_DIR/scripts/launcher.py --audit` for a full import/call audit
- All source code is readable in the `scripts/` directory

## Games

1. **Tetris** — Classic falling blocks. Arrow keys to move/rotate, space to hard drop.
2. **Snake** — Eat food, grow longer, don't hit yourself. Arrow keys to steer.
3. **Wordle** — Guess the 5-letter word in 6 tries. Official Wordle word list (12,972 valid words).
4. **Hangman** — Guess letters before the stick figure is complete. 6 wrong guesses allowed.

## Controls

- **Menu**: Press 1-4 to pick a game, `v` to view security info, `q` to quit
- **Tetris/Snake**: `q` to quit (no letter input needed)
- **Wordle/Hangman**: `Esc` to quit (Q is a valid letter)
- Ctrl+C always exits cleanly from any screen.
