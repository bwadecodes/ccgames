```
  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗
 ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝
 ██║     ██║     ███████║██║   ██║██║  ██║█████╗
 ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝
 ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗
  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝

   █████╗ ██████╗  ██████╗ █████╗ ██████╗ ███████╗
  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝
  ███████║██████╔╝██║     ███████║██║  ██║█████╗
  ██╔══██║██╔══██╗██║     ██╔══██║██║  ██║██╔══╝
  ██║  ██║██║  ██║╚██████╗██║  ██║██████╔╝███████╗
  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝
```

**4 classic terminal games, right inside Claude Code.**

Type `/ccgames` or just say "I'm bored" — Claude opens an arcade in a new terminal tab.

Tetris. Snake. Wordle (with the real word list). Hangman. No installs. No dependencies. No internet.

---

## Install

**One command. That's it.**

```bash
git clone https://github.com/bwadecodes/ccgames.git ~/.claude/skills/ccgames
```

Next time you start Claude Code, type `/ccgames` or say "let's play" and the arcade opens in a new terminal tab.

**Requirements:** Python 3 (you already have it).

---

## What You Get

| Game | What It Is | Controls |
|------|-----------|----------|
| **Tetris** | Classic falling blocks. It speeds up. You panic. | Arrow keys, Space = hard drop |
| **Snake** | Eat. Grow. Don't hit yourself. | Arrow keys |
| **Wordle** | Guess the 5-letter word in 6 tries. Real NYT word list — 12,972 valid words. | Type + Enter, Esc = quit |
| **Hangman** | Save the stick figure. 6 wrong guesses. | Type letters, Esc = quit |

---

## How It Works

```
You: "I'm bored"
Claude: *opens arcade in a new terminal tab*
You: *plays Wordle for 3 minutes*
You: *closes tab, gets back to work*
```

The games run in a separate terminal window using Python's `curses` library. Claude Code detects your platform (WSL, macOS, Linux) and opens the right kind of terminal automatically.

---

## Security — Read This, It Matters

This runs code on your machine. You should care what it does. Here's the deal:

- **Zero network connections** — nothing leaves your machine, ever
- **Zero file reads/writes** — no temp files, no logs, no high scores
- **Zero subprocesses** — no `os.system()`, no `subprocess`, no shelling out
- **Python standard library only** — `curses`, `random`, `sys`, `os.path`
- **No external dependencies** — no `pip install`, no `requirements.txt`

Don't trust us? Good. Run the built-in audit:

```bash
python3 ~/.claude/skills/ccgames/scripts/launcher.py --audit
```

Or press `v` in the arcade menu to see the security report. Or just read the source — it's 6 Python files.

---

## Uninstall

```bash
rm -rf ~/.claude/skills/ccgames
```

Gone. No config files, no cache, no traces.

---

## Update

```bash
cd ~/.claude/skills/ccgames && git pull
```

---

## FAQ

**Does this actually work inside Claude Code?**
Yes. Claude opens the arcade in a new terminal tab. The games need a real terminal (curses), so they can't run inside Claude's tool execution — but Claude handles that automatically.

**Does this phone home?**
No. Zero network calls. Verified by the `--audit` flag and source code inspection.

**Does this write anything to disk?**
No. Not even high scores. (We considered it. We decided purity was funnier.)

**Can I add my own games?**
Yes. Add a `.py` file to `scripts/`, import it in `launcher.py`, and add a menu entry. Follow the pattern of the existing games — `run_game(stdscr)` function, curses-only.

**Why does Wordle accept "aahed" as a word?**
Because the official Wordle word list says so. Take it up with the NYT.

---

## The Fine Print

A [bwade](https://x.com/bwadesays) side project. MIT licensed. No warranty. No support SLA. But honestly, it's 6 Python files — if something breaks, you can probably fix it faster than you can file an issue.

Built with Claude Code, obviously.
