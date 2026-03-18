"""
Snake — Classic snake game.
Controls: Arrow keys to steer. Eat food, grow longer, don't hit yourself or the walls.
Zero network calls. Zero file I/O. Python stdlib only.
"""
import curses
import random
import time
import sys


def run_game(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)    # snake head
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)  # snake body
    curses.init_pair(3, curses.COLOR_RED, -1)      # food
    curses.init_pair(4, curses.COLOR_WHITE, -1)    # border/text
    curses.init_pair(5, curses.COLOR_CYAN, -1)     # title
    curses.init_pair(6, curses.COLOR_YELLOW, -1)   # score

    curses.curs_set(0)

    h, w = stdscr.getmaxyx()
    # Play area dimensions (inside border)
    play_h = min(h - 4, 20)
    play_w = min(w - 4, 40)

    if play_h < 10 or play_w < 20:
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, "Terminal too small. Need at least 24x24.")
            stdscr.addstr(1, 0, "Press any key to exit.")
        except curses.error:
            pass
        stdscr.nodelay(False)
        stdscr.getch()
        return 0

    # Center the play area
    off_y = max(0, (h - play_h - 4) // 2)
    off_x = max(0, (w - play_w - 2) // 2)

    border_color = curses.color_pair(4)
    title_color = curses.color_pair(5) | curses.A_BOLD
    score_color = curses.color_pair(6)

    # Snake initial state
    snake = [(play_h // 2, play_w // 4 + i) for i in range(3)]
    snake.reverse()  # Head is at index 0
    direction = (0, 1)  # Moving right
    score = 0

    def place_food():
        while True:
            fy = random.randint(0, play_h - 1)
            fx = random.randint(0, play_w - 1)
            if (fy, fx) not in snake:
                return (fy, fx)

    food = place_food()

    # Speed: start at 100ms, get faster
    base_delay = 100
    stdscr.nodelay(True)
    stdscr.timeout(base_delay)

    game_over = False

    while not game_over:
        stdscr.erase()

        # Draw title and score
        try:
            stdscr.addstr(off_y, off_x, "SNAKE", title_color)
            stdscr.addstr(off_y, off_x + play_w - 8, f"Score: {score}", score_color)
        except curses.error:
            pass

        # Draw border
        border_y = off_y + 1
        border_x = off_x
        try:
            stdscr.addstr(border_y, border_x, "┌" + "─" * play_w + "┐", border_color)
            for i in range(play_h):
                stdscr.addstr(border_y + 1 + i, border_x, "│", border_color)
                stdscr.addstr(border_y + 1 + i, border_x + play_w + 1, "│", border_color)
            stdscr.addstr(border_y + play_h + 1, border_x, "└" + "─" * play_w + "┘", border_color)
        except curses.error:
            pass

        # Draw food
        fy, fx = food
        try:
            stdscr.addstr(border_y + 1 + fy, border_x + 1 + fx, "●", curses.color_pair(3) | curses.A_BOLD)
        except curses.error:
            pass

        # Draw snake
        for i, (sy, sx) in enumerate(snake):
            try:
                if i == 0:
                    # Head
                    heads = {(0,1): "▶", (0,-1): "◀", (-1,0): "▲", (1,0): "▼"}
                    ch = heads.get(direction, "●")
                    stdscr.addstr(border_y + 1 + sy, border_x + 1 + sx, ch, curses.color_pair(1) | curses.A_BOLD)
                else:
                    stdscr.addstr(border_y + 1 + sy, border_x + 1 + sx, "█", curses.color_pair(1))
            except curses.error:
                pass

        # Controls hint
        try:
            stdscr.addstr(border_y + play_h + 2, border_x, "Arrow keys: move | q: quit", curses.A_DIM)
        except curses.error:
            pass

        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            return score
        elif key == curses.KEY_UP and direction != (1, 0):
            direction = (-1, 0)
        elif key == curses.KEY_DOWN and direction != (-1, 0):
            direction = (1, 0)
        elif key == curses.KEY_LEFT and direction != (0, 1):
            direction = (0, -1)
        elif key == curses.KEY_RIGHT and direction != (0, -1):
            direction = (0, 1)

        # Move snake
        head_y, head_x = snake[0]
        new_y = head_y + direction[0]
        new_x = head_x + direction[1]

        # Check wall collision
        if new_y < 0 or new_y >= play_h or new_x < 0 or new_x >= play_w:
            game_over = True
            continue

        # Check self collision
        if (new_y, new_x) in snake:
            game_over = True
            continue

        snake.insert(0, (new_y, new_x))

        # Check food
        if (new_y, new_x) == food:
            score += 10
            # Check win condition (filled the board)
            if len(snake) >= play_h * play_w:
                game_over = True
                continue
            food = place_food()
            # Speed up slightly
            new_delay = max(40, base_delay - len(snake) * 2)
            stdscr.timeout(new_delay)
        else:
            snake.pop()

    # Game over screen
    stdscr.nodelay(False)
    stdscr.clear()

    msg = "GAME OVER"
    try:
        stdscr.addstr(h // 2 - 2, (w - len(msg)) // 2, msg, curses.color_pair(3) | curses.A_BOLD)
        score_msg = f"Score: {score}  |  Length: {len(snake)}"
        stdscr.addstr(h // 2, (w - len(score_msg)) // 2, score_msg, curses.color_pair(4))

        if score >= 200:
            quip = "Incredible run!"
        elif score >= 100:
            quip = "Solid snake skills."
        elif score >= 50:
            quip = "Not bad at all."
        else:
            quip = "The snake life is hard."
        stdscr.addstr(h // 2 + 1, (w - len(quip)) // 2, quip, curses.color_pair(5))

        cont = "Press any key to continue"
        stdscr.addstr(h // 2 + 3, (w - len(cont)) // 2, cont, curses.A_DIM)
    except curses.error:
        pass

    stdscr.refresh()
    stdscr.getch()
    return score


def main(stdscr):
    return run_game(stdscr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        print()
        print("  snake.py — Classic Snake")
        print("  ────────────────────────")
        print("  Imports: curses, random, time, sys")
        print("  Network access:  NONE")
        print("  File writes:     NONE")
        print("  File reads:      NONE")
        print("  Subprocesses:    NONE")
        print()
    else:
        curses.wrapper(main)
