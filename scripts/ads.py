"""
Sponsor card display for Claude Arcade.
Zero network calls. Zero file I/O. Just curses rendering.
"""
import curses


def show_sponsor_card(stdscr):
    """Display the sponsor card centered on screen. Press any key to dismiss."""
    stdscr.clear()
    curses.curs_set(0)

    h, w = stdscr.getmaxyx()

    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)
    curses.init_pair(2, curses.COLOR_WHITE, -1)
    curses.init_pair(3, curses.COLOR_GREEN, -1)
    # Orange: use 256-color palette (208) if available, else yellow
    if curses.COLORS >= 256:
        curses.init_pair(4, 208, -1)
    else:
        curses.init_pair(4, curses.COLOR_YELLOW, -1)

    cyan = curses.color_pair(1) | curses.A_BOLD
    white = curses.color_pair(2)
    green = curses.color_pair(3)
    orange = curses.color_pair(4) | curses.A_BOLD
    dim = curses.A_DIM

    lines = [
        ("", white),
        ("This enhanced Claude Code experience", white),
        ("was brought to you by", white),
        ("", white),
        ("███████╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗", orange),
        ("██╔════╝██║   ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝", orange),
        ("█████╗  ██║   ██║   ██║   ██║   ██║██████╔╝█████╗  ", orange),
        ("██╔══╝  ██║   ██║   ██║   ██║   ██║██╔══██╗██╔══╝  ", orange),
        ("██║     ╚██████╔╝   ██║   ╚██████╔╝██║  ██║███████╗", orange),
        ("╚═╝      ╚═════╝    ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝", orange),
        ("", white),
        (" █████╗ ██████╗ ██╗   ██╗███████╗██████╗ ████████╗██╗███████╗███████╗██████╗ ", orange),
        ("██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝██╔════╝██╔══██╗", orange),
        ("███████║██║  ██║╚██╗ ██╔╝█████╗  ██████╔╝   ██║   ██║███████╗█████╗  ██████╔╝", orange),
        ("██╔══██║██║  ██║ ╚████╔╝ ██╔══╝  ██╔══██╗   ██║   ██║╚════██║██╔══╝  ██╔══██╗", orange),
        ("██║  ██║██████╔╝  ╚██╔╝  ███████╗██║  ██║   ██║   ██║███████║███████╗██║  ██║", orange),
        ("╚═╝  ╚═╝╚═════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝", orange),
        ("", white),
        ("Your brand here. Seriously, email", white),
        ("us. This is real estate now.", white),
        ("", white),
    ]

    box_w = 88
    box_h = len(lines) + 4  # +4 for top/bottom borders and padding
    total_h = box_h + 4  # outer box

    start_y = max(0, (h - total_h) // 2)
    start_x = max(0, (w - (box_w + 4)) // 2)

    outer_w = box_w + 4
    inner_w = box_w - 2

    # Draw outer box
    try:
        stdscr.addstr(start_y, start_x, "┌" + "─" * (outer_w - 2) + "┐", dim)
        for i in range(1, total_h - 1):
            stdscr.addstr(start_y + i, start_x, "│" + " " * (outer_w - 2) + "│", dim)
        stdscr.addstr(start_y + total_h - 1, start_x, "└" + "─" * (outer_w - 2) + "┘", dim)

        # Draw inner box
        inner_start_y = start_y + 2
        inner_start_x = start_x + 3

        stdscr.addstr(inner_start_y, inner_start_x, "┌" + "─" * (inner_w) + "┐", orange)
        for i, (text, color) in enumerate(lines):
            row = inner_start_y + 1 + i
            stdscr.addstr(row, inner_start_x, "│", orange)
            # Center the text within the inner box
            padding = inner_w - len(text)
            left_pad = padding // 2
            right_pad = padding - left_pad
            stdscr.addstr(row, inner_start_x + 1, " " * left_pad + text, color)
            stdscr.addstr(row, inner_start_x + 1 + left_pad + len(text), " " * right_pad, color)
            stdscr.addstr(row, inner_start_x + 1 + inner_w, "│", orange)
        stdscr.addstr(inner_start_y + len(lines) + 1, inner_start_x, "└" + "─" * (inner_w) + "┘", orange)

        # "Press any key" prompt
        prompt = "Press any key to continue"
        prompt_y = start_y + total_h - 2
        prompt_x = start_x + (outer_w - len(prompt)) // 2
        stdscr.addstr(prompt_y, prompt_x, prompt, dim)

    except curses.error:
        # Terminal too small — show minimal version
        stdscr.clear()
        try:
            stdscr.addstr(h // 2 - 1, max(0, (w - 30) // 2), "Sponsored by a future brand", cyan)
            stdscr.addstr(h // 2 + 1, max(0, (w - 25) // 2), "Press any key to continue", dim)
        except curses.error:
            pass

    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        print()
        print("  ads.py — Sponsor Card Display")
        print("  ─────────────────────────────")
        print("  Imports: curses (terminal UI), time (unused reserve)")
        print("  Network access:  NONE")
        print("  File writes:     NONE")
        print("  File reads:      NONE")
        print("  Subprocesses:    NONE")
        print()
    else:
        curses.wrapper(show_sponsor_card)
