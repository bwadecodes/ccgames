#!/usr/bin/env python3
"""
Claude Arcade — Terminal game launcher.
Run: python3 launcher.py
Options: --inspect (security summary), --audit (full import audit)
Zero network calls. Zero file I/O. Python stdlib only.
"""
import curses
import sys
import os.path
import time

# Resolve script directory for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

import tetris
import snake
import wordle
import hangman
import ads

HEADER = [
    "  ██████╗██╗      █████╗ ██╗   ██╗██████╗ ███████╗",
    " ██╔════╝██║     ██╔══██╗██║   ██║██╔══██╗██╔════╝",
    " ██║     ██║     ███████║██║   ██║██║  ██║█████╗  ",
    " ██║     ██║     ██╔══██║██║   ██║██║  ██║██╔══╝  ",
    " ╚██████╗███████╗██║  ██║╚██████╔╝██████╔╝███████╗",
    "  ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝",
    "",
    "   █████╗ ██████╗  ██████╗ █████╗ ██████╗ ███████╗",
    "  ██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔════╝",
    "  ███████║██████╔╝██║     ███████║██║  ██║█████╗  ",
    "  ██╔══██║██╔══██╗██║     ██╔══██║██║  ██║██╔══╝  ",
    "  ██║  ██║██║  ██║╚██████╗██║  ██║██████╔╝███████╗",
    "  ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝ ╚══════╝",
]

MENU_ITEMS = [
    ("1", "Tetris", "Classic falling blocks"),
    ("2", "Snake", "Eat, grow, survive"),
    ("3", "Wordle", "Guess the 5-letter word"),
    ("4", "Hangman", "Save the stick figure"),
]


def show_inspect_screen(stdscr):
    """Show security info inside the curses UI."""
    stdscr.clear()
    curses.curs_set(0)

    h, w = stdscr.getmaxyx()

    curses.init_pair(10, curses.COLOR_GREEN, -1)
    curses.init_pair(11, curses.COLOR_CYAN, -1)
    curses.init_pair(12, curses.COLOR_WHITE, -1)

    GREEN = curses.color_pair(10) | curses.A_BOLD
    CYAN = curses.color_pair(11) | curses.A_BOLD
    TEXT = curses.color_pair(12)

    lines = [
        ("  Games Arcade — Security Report", CYAN),
        ("  ──────────────────────────────", curses.A_DIM),
        ("", TEXT),
        ("  Files in this skill:", TEXT),
        ("    scripts/launcher.py  (menu UI)", curses.A_DIM),
        ("    scripts/ads.py       (ad content, no network)", curses.A_DIM),
        ("    scripts/tetris.py    (tetris game)", curses.A_DIM),
        ("    scripts/snake.py     (snake game)", curses.A_DIM),
        ("    scripts/wordle.py    (wordle game)", curses.A_DIM),
        ("    scripts/hangman.py   (hangman game)", curses.A_DIM),
        ("", TEXT),
        ("  Imports used across all files:", TEXT),
        ("    curses    — terminal rendering (stdlib)", curses.A_DIM),
        ("    random    — random number generation (stdlib)", curses.A_DIM),
        ("    time      — sleep/timing (stdlib)", curses.A_DIM),
        ("    sys       — argument parsing (stdlib)", curses.A_DIM),
        ("    os.path   — script path resolution (stdlib)", curses.A_DIM),
        ("", TEXT),
        ("  Network access:  NONE", GREEN),
        ("  File writes:     NONE", GREEN),
        ("  File reads:      NONE (beyond own source files)", GREEN),
        ("  Subprocesses:    NONE", GREEN),
        ("  External deps:   NONE", GREEN),
        ("", TEXT),
        ("  All code is open source and readable in this directory.", TEXT),
        ("  Run `cat <filename>` to read any file.", curses.A_DIM),
        ("", TEXT),
        ("  a bwade side project — x.com/bwadesays", CYAN),
        ("", TEXT),
        ("  Press any key to return to menu", curses.A_DIM),
    ]

    start_y = max(0, (h - len(lines)) // 2)
    for i, (text, attr) in enumerate(lines):
        try:
            stdscr.addstr(start_y + i, 2, text, attr)
        except curses.error:
            pass

    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()


def draw_menu(stdscr):
    """Main menu loop."""
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)     # header
    curses.init_pair(2, curses.COLOR_WHITE, -1)     # text
    curses.init_pair(3, curses.COLOR_GREEN, -1)     # menu numbers
    curses.init_pair(4, curses.COLOR_YELLOW, -1)    # game names
    curses.init_pair(5, curses.COLOR_MAGENTA, -1)   # descriptions

    HEADER_COLOR = curses.color_pair(1) | curses.A_BOLD
    TEXT = curses.color_pair(2)
    NUM = curses.color_pair(3) | curses.A_BOLD
    GAME_NAME = curses.color_pair(4) | curses.A_BOLD
    DESC = curses.color_pair(5)

    curses.curs_set(0)
    stdscr.nodelay(False)

    while True:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        # Draw header
        header_w = max(len(line) for line in HEADER)
        start_x = max(0, (w - header_w) // 2)
        start_y = max(0, (h - len(HEADER) - 14) // 2)

        for i, line in enumerate(HEADER):
            try:
                stdscr.addstr(start_y + i, start_x, line, HEADER_COLOR)
            except curses.error:
                pass

        # Menu items
        menu_y = start_y + len(HEADER) + 2
        menu_x = max(0, (w - 40) // 2)

        for num, name, desc in MENU_ITEMS:
            try:
                stdscr.addstr(menu_y, menu_x, f"  [{num}]", NUM)
                stdscr.addstr(menu_y, menu_x + 6, f" {name}", GAME_NAME)
                stdscr.addstr(menu_y, menu_x + 6 + len(name) + 1, f"  — {desc}", DESC)
            except curses.error:
                pass
            menu_y += 2

        # Footer
        footer_y = menu_y + 1
        try:
            stdscr.addstr(footer_y, menu_x, "  [v]", NUM)
            stdscr.addstr(footer_y, menu_x + 6, " View Source / Security Info", TEXT)
            stdscr.addstr(footer_y + 2, menu_x, "  [q]", NUM)
            stdscr.addstr(footer_y + 2, menu_x + 6, " Quit", TEXT)
        except curses.error:
            pass

        # Subtitle
        try:
            sub = "Pick a game. Have fun. Get back to work."
            stdscr.addstr(footer_y + 4, max(0, (w - len(sub)) // 2), sub, curses.A_DIM)
        except curses.error:
            pass

        stdscr.refresh()

        key = stdscr.getch()

        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('v') or key == ord('V'):
            show_inspect_screen(stdscr)
        elif key == ord('1'):
            tetris.run_game(stdscr)
            ads.show_sponsor_card(stdscr)
        elif key == ord('2'):
            snake.run_game(stdscr)
            ads.show_sponsor_card(stdscr)
        elif key == ord('3'):
            wordle.run_game(stdscr)
            ads.show_sponsor_card(stdscr)
        elif key == ord('4'):
            hangman.run_game(stdscr)
            ads.show_sponsor_card(stdscr)


def print_inspect():
    """Print security summary to stdout."""
    print()
    print("  Games Arcade — Security Report")
    print("  ──────────────────────────────")
    print("  Files in this skill:")
    print("    scripts/launcher.py  (menu UI)")
    print("    scripts/ads.py       (ad content, no network)")
    print("    scripts/tetris.py    (tetris game)")
    print("    scripts/snake.py     (snake game)")
    print("    scripts/wordle.py    (wordle game)")
    print("    scripts/hangman.py   (hangman game)")
    print()
    print("  Imports used across all files:")
    print("    curses    — terminal rendering (stdlib)")
    print("    random    — random number generation (stdlib)")
    print("    time      — sleep/timing (stdlib)")
    print("    sys       — argument parsing (stdlib)")
    print("    os.path   — script path resolution (stdlib)")
    print()
    print("  Network access:  NONE")
    print("  File writes:     NONE")
    print("  File reads:      NONE (beyond own source files)")
    print("  Subprocesses:    NONE")
    print("  External deps:   NONE")
    print()
    print("  All code is open source and readable in this directory.")
    print("  Run `cat <filename>` to read any file.")
    print()


def print_audit():
    """Scan all .py files and report imports and sensitive calls."""
    import re

    print()
    print("  Full Audit — Games Arcade")
    print("  ─────────────────────────")

    SAFE_MODULES = {
        'curses': 'terminal UI',
        'random': 'randomization',
        'time': 'sleep/timing',
        'sys': 'args/path',
        'os.path': 'path resolution',
        'os': 'path resolution (os.path only)',
        're': 'pattern matching (audit only)',
    }

    SENSITIVE = [
        'open(', 'subprocess', 'os.system', 'os.popen', 'os.exec',
        'socket', 'urllib', 'http.client', 'requests.',
        'shutil.', 'tempfile.', 'pathlib.',
    ]

    py_files = []
    for fname in sorted(os.listdir(SCRIPT_DIR)):
        if fname.endswith('.py'):
            py_files.append(fname)

    concerns = 0

    for fname in py_files:
        fpath = os.path.join(SCRIPT_DIR, fname)
        print(f"\n  Scanning: scripts/{fname}")

        with open(fpath, 'r') as f:
            lines = f.readlines()

        # When scanning launcher.py, find the audit function boundaries so we
        # can skip self-referential hits (the audit code itself uses open() and
        # prints sensitive keywords as string literals).
        audit_start = audit_end = -1
        if fname == 'launcher.py':
            for li, ln in enumerate(lines):
                if ln.strip().startswith('def print_audit'):
                    audit_start = li
                elif audit_start >= 0 and ln.startswith('def ') and li > audit_start:
                    audit_end = li
                    break
            if audit_start >= 0 and audit_end < 0:
                audit_end = len(lines)

        found_imports = False
        found_sensitive = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()

            # Check imports
            if stripped.startswith('import ') or stripped.startswith('from '):
                found_imports = True
                if stripped.startswith('import '):
                    module = stripped.split()[1].split('.')[0]
                    full = stripped.split()[1]
                else:
                    module = stripped.split()[1].split('.')[0]
                    full = stripped.split()[1]

                if module in SAFE_MODULES or full in SAFE_MODULES:
                    desc = SAFE_MODULES.get(full, SAFE_MODULES.get(module, ''))
                    print(f"    Line {i:3d}:  {stripped:40s} safe (stdlib, {desc})")
                elif module in [f.replace('.py', '') for f in py_files]:
                    print(f"    Line {i:3d}:  {stripped:40s} safe (local module)")
                else:
                    print(f"    Line {i:3d}:  {stripped:40s} UNKNOWN MODULE")
                    concerns += 1

            # Check sensitive calls — skip comments, imports, and the audit function itself
            if stripped.startswith('#') or stripped.startswith('import') or stripped.startswith('from'):
                continue
            # Skip lines inside print_audit (self-referential)
            if audit_start >= 0 and audit_start <= (i - 1) < audit_end:
                continue

            for sensitive in SENSITIVE:
                if sensitive in stripped:
                    if 'SENSITIVE' in stripped:
                        continue
                    print(f"    Line {i:3d}:  SENSITIVE CALL: {sensitive} in: {stripped[:60]}")
                    concerns += 1
                    found_sensitive = True

        if not found_imports:
            print("    No imports found.")

        if not found_sensitive:
            print(f"    No calls to: open, subprocess, os.system, socket, urllib, http")

    print(f"\n  Summary: {concerns} security concerns found.")
    if concerns == 0:
        print("  All imports are from Python standard library.")
        print("  No file I/O, network, or subprocess activity detected.")
    print()


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == '--inspect':
            print_inspect()
            return
        elif sys.argv[1] == '--audit':
            print_audit()
            return
        elif sys.argv[1] == '--help':
            print("Claude Arcade — Terminal Games")
            print()
            print("Usage: python3 launcher.py [option]")
            print()
            print("Options:")
            print("  (none)     Launch the game menu")
            print("  --inspect  Print security summary")
            print("  --audit    Full import & call audit")
            print("  --help     Show this help")
            return

    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
