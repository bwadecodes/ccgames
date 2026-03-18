"""
Tetris — Classic falling-block game.
Controls: Left/Right arrows to move, Up to rotate, Down for soft drop, Space for hard drop.
Zero network calls. Zero file I/O. Python stdlib only.
"""
import curses
import random
import time
import sys

# Tetromino shapes (each rotation is a list of (row, col) offsets)
SHAPES = {
    'I': [[(0,0),(0,1),(0,2),(0,3)], [(0,0),(1,0),(2,0),(3,0)],
          [(0,0),(0,1),(0,2),(0,3)], [(0,0),(1,0),(2,0),(3,0)]],
    'O': [[(0,0),(0,1),(1,0),(1,1)]] * 4,
    'T': [[(0,0),(0,1),(0,2),(1,1)], [(0,0),(1,0),(2,0),(1,1)],
          [(1,0),(1,1),(1,2),(0,1)], [(0,0),(1,0),(2,0),(1,-1)]],
    'S': [[(0,1),(0,2),(1,0),(1,1)], [(0,0),(1,0),(1,1),(2,1)],
          [(0,1),(0,2),(1,0),(1,1)], [(0,0),(1,0),(1,1),(2,1)]],
    'Z': [[(0,0),(0,1),(1,1),(1,2)], [(0,1),(1,0),(1,1),(2,0)],
          [(0,0),(0,1),(1,1),(1,2)], [(0,1),(1,0),(1,1),(2,0)]],
    'L': [[(0,0),(0,1),(0,2),(1,0)], [(0,0),(1,0),(2,0),(2,1)],
          [(1,0),(1,1),(1,2),(0,2)], [(0,0),(0,1),(1,1),(2,1)]],
    'J': [[(0,0),(0,1),(0,2),(1,2)], [(0,0),(1,0),(2,0),(0,1)],
          [(1,0),(1,1),(1,2),(0,0)], [(0,0),(1,0),(2,0),(2,-1)]],
}

SHAPE_NAMES = list(SHAPES.keys())
COLORS = {'I': 1, 'O': 2, 'T': 3, 'S': 4, 'Z': 5, 'L': 6, 'J': 7}

BOARD_W = 10
BOARD_H = 20


def init_colors():
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_CYAN)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_YELLOW)
    curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_GREEN)
    curses.init_pair(5, curses.COLOR_RED, curses.COLOR_RED)
    curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_WHITE)
    curses.init_pair(7, curses.COLOR_BLUE, curses.COLOR_BLUE)
    curses.init_pair(8, curses.COLOR_WHITE, -1)  # text
    curses.init_pair(9, curses.COLOR_CYAN, -1)   # title


class Tetris:
    def __init__(self):
        self.board = [[0] * BOARD_W for _ in range(BOARD_H)]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.current_piece = None
        self.current_shape = None
        self.current_rot = 0
        self.current_x = 0
        self.current_y = 0
        self.next_piece = random.choice(SHAPE_NAMES)
        self.spawn_piece()

    def spawn_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = random.choice(SHAPE_NAMES)
        self.current_rot = 0
        self.current_x = BOARD_W // 2 - 1
        self.current_y = 0
        if self.collides(self.current_x, self.current_y, self.current_rot):
            self.game_over = True

    def get_cells(self, x, y, rot):
        shape = SHAPES[self.current_piece][rot % len(SHAPES[self.current_piece])]
        return [(y + r, x + c) for r, c in shape]

    def collides(self, x, y, rot):
        for r, c in self.get_cells(x, y, rot):
            if c < 0 or c >= BOARD_W or r >= BOARD_H:
                return True
            if r >= 0 and self.board[r][c]:
                return True
        return False

    def lock_piece(self):
        color = COLORS[self.current_piece]
        for r, c in self.get_cells(self.current_x, self.current_y, self.current_rot):
            if 0 <= r < BOARD_H and 0 <= c < BOARD_W:
                self.board[r][c] = color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        cleared = BOARD_H - len(new_board)
        if cleared > 0:
            self.lines_cleared += cleared
            points = {1: 100, 2: 300, 3: 500, 4: 800}
            self.score += points.get(cleared, 800) * self.level
            self.level = self.lines_cleared // 10 + 1
            self.board = [[0] * BOARD_W for _ in range(cleared)] + new_board

    def move(self, dx, dy):
        if not self.collides(self.current_x + dx, self.current_y + dy, self.current_rot):
            self.current_x += dx
            self.current_y += dy
            return True
        return False

    def rotate(self):
        new_rot = (self.current_rot + 1) % 4
        if not self.collides(self.current_x, self.current_y, new_rot):
            self.current_rot = new_rot
        elif not self.collides(self.current_x - 1, self.current_y, new_rot):
            self.current_x -= 1
            self.current_rot = new_rot
        elif not self.collides(self.current_x + 1, self.current_y, new_rot):
            self.current_x += 1
            self.current_rot = new_rot

    def hard_drop(self):
        while self.move(0, 1):
            self.score += 2
        self.lock_piece()

    def tick(self):
        if not self.move(0, 1):
            self.lock_piece()

    def get_drop_speed(self):
        speeds = [0.8, 0.72, 0.63, 0.55, 0.47, 0.38, 0.3, 0.22, 0.15, 0.1, 0.08, 0.07, 0.05]
        idx = min(self.level - 1, len(speeds) - 1)
        return speeds[idx]


def draw_board(stdscr, game, offset_y, offset_x):
    text_color = curses.color_pair(8)
    title_color = curses.color_pair(9) | curses.A_BOLD

    # Draw border
    for y in range(BOARD_H + 2):
        try:
            stdscr.addstr(offset_y + y, offset_x, "│", text_color)
            stdscr.addstr(offset_y + y, offset_x + BOARD_W * 2 + 1, "│", text_color)
        except curses.error:
            pass
    try:
        stdscr.addstr(offset_y, offset_x, "┌" + "──" * BOARD_W + "┐", text_color)
        stdscr.addstr(offset_y + BOARD_H + 1, offset_x, "└" + "──" * BOARD_W + "┘", text_color)
    except curses.error:
        pass

    # Draw board cells
    for y in range(BOARD_H):
        for x in range(BOARD_W):
            cell = game.board[y][x]
            if cell:
                try:
                    stdscr.addstr(offset_y + y + 1, offset_x + 1 + x * 2, "  ", curses.color_pair(cell))
                except curses.error:
                    pass
            else:
                try:
                    stdscr.addstr(offset_y + y + 1, offset_x + 1 + x * 2, " .", curses.A_DIM)
                except curses.error:
                    pass

    # Draw current piece
    if not game.game_over:
        color = curses.color_pair(COLORS[game.current_piece])
        for r, c in game.get_cells(game.current_x, game.current_y, game.current_rot):
            if 0 <= r < BOARD_H and 0 <= c < BOARD_W:
                try:
                    stdscr.addstr(offset_y + r + 1, offset_x + 1 + c * 2, "  ", color)
                except curses.error:
                    pass

    # Draw info panel
    info_x = offset_x + BOARD_W * 2 + 4
    try:
        stdscr.addstr(offset_y, info_x, "TETRIS", title_color)
        stdscr.addstr(offset_y + 2, info_x, f"Score: {game.score}", text_color)
        stdscr.addstr(offset_y + 3, info_x, f"Level: {game.level}", text_color)
        stdscr.addstr(offset_y + 4, info_x, f"Lines: {game.lines_cleared}", text_color)

        stdscr.addstr(offset_y + 6, info_x, "Next:", text_color)
        # Draw next piece preview
        next_shape = SHAPES[game.next_piece][0]
        next_color = curses.color_pair(COLORS[game.next_piece])
        for r, c in next_shape:
            try:
                stdscr.addstr(offset_y + 7 + r, info_x + c * 2, "  ", next_color)
            except curses.error:
                pass

        stdscr.addstr(offset_y + 12, info_x, "Controls:", text_color)
        stdscr.addstr(offset_y + 13, info_x, "← → Move", curses.A_DIM)
        stdscr.addstr(offset_y + 14, info_x, " ↑  Rotate", curses.A_DIM)
        stdscr.addstr(offset_y + 15, info_x, " ↓  Soft drop", curses.A_DIM)
        stdscr.addstr(offset_y + 16, info_x, "SPC Hard drop", curses.A_DIM)
        stdscr.addstr(offset_y + 17, info_x, " q  Quit", curses.A_DIM)
    except curses.error:
        pass


def run_game(stdscr):
    init_colors()
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(50)

    game = Tetris()
    last_tick = time.time()

    h, w = stdscr.getmaxyx()
    if h < BOARD_H + 4 or w < BOARD_W * 2 + 20:
        stdscr.nodelay(False)
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, f"Terminal too small. Need {BOARD_W*2+20}x{BOARD_H+4}, have {w}x{h}")
            stdscr.addstr(1, 0, "Press any key to exit.")
        except curses.error:
            pass
        stdscr.getch()
        return 0

    offset_y = max(0, (h - BOARD_H - 2) // 2)
    offset_x = max(0, (w - BOARD_W * 2 - 20) // 2)

    while not game.game_over:
        stdscr.erase()
        draw_board(stdscr, game, offset_y, offset_x)
        stdscr.refresh()

        key = stdscr.getch()
        if key == ord('q') or key == ord('Q'):
            return game.score
        elif key == curses.KEY_LEFT:
            game.move(-1, 0)
        elif key == curses.KEY_RIGHT:
            game.move(1, 0)
        elif key == curses.KEY_UP:
            game.rotate()
        elif key == curses.KEY_DOWN:
            if game.move(0, 1):
                game.score += 1
        elif key == ord(' '):
            game.hard_drop()

        now = time.time()
        if now - last_tick >= game.get_drop_speed():
            game.tick()
            last_tick = now

    # Game over screen
    stdscr.nodelay(False)
    stdscr.clear()
    text_color = curses.color_pair(8)
    title_color = curses.color_pair(5)

    msg = "GAME OVER"
    try:
        stdscr.addstr(h // 2 - 2, (w - len(msg)) // 2, msg, title_color | curses.A_BOLD)
        score_msg = f"Final Score: {game.score}"
        stdscr.addstr(h // 2, (w - len(score_msg)) // 2, score_msg, text_color)
        level_msg = f"Level {game.level} | {game.lines_cleared} lines"
        stdscr.addstr(h // 2 + 1, (w - len(level_msg)) // 2, level_msg, text_color)
        cont = "Press any key to continue"
        stdscr.addstr(h // 2 + 3, (w - len(cont)) // 2, cont, curses.A_DIM)
    except curses.error:
        pass
    stdscr.refresh()
    stdscr.getch()
    return game.score


def main(stdscr):
    return run_game(stdscr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        print()
        print("  tetris.py — Classic Tetris")
        print("  ──────────────────────────")
        print("  Imports: curses, random, time, sys")
        print("  Network access:  NONE")
        print("  File writes:     NONE")
        print("  File reads:      NONE")
        print("  Subprocesses:    NONE")
        print()
    else:
        curses.wrapper(main)
