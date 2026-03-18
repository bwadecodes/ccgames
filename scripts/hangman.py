"""
Hangman — Guess letters before the stick figure is complete.
6 wrong guesses allowed. ASCII art gallows.
Zero network calls. Zero file I/O. Python stdlib only.
"""
import curses
import random
import sys

# 200+ words of varying length (5-10 letters)
WORDS = [
    "about", "above", "abstract", "accept", "account", "achieve", "action",
    "active", "actual", "address", "adjust", "advance", "advice", "affect",
    "afford", "agenda", "almost", "always", "amount", "ancient", "animal",
    "annual", "answer", "anyway", "appeal", "appear", "around", "arrive",
    "artist", "assume", "attach", "attack", "attend", "august", "author",
    "balance", "barrier", "battle", "become", "before", "behind", "belong",
    "benefit", "beside", "beyond", "bitter", "blanket", "bother", "bottom",
    "branch", "breath", "bridge", "bright", "broken", "bronze", "budget",
    "bundle", "burden", "button", "camera", "cancel", "carbon", "career",
    "castle", "center", "chance", "change", "charge", "choice", "choose",
    "circle", "client", "coffee", "colony", "column", "combat", "comedy",
    "common", "comply", "copper", "corner", "costly", "cotton", "county",
    "couple", "course", "cousin", "create", "credit", "crisis", "custom",
    "damage", "dancer", "danger", "debate", "decade", "decide", "defeat",
    "defend", "define", "degree", "demand", "depart", "depend", "deploy",
    "deputy", "desert", "design", "detail", "detect", "device", "devote",
    "differ", "dinner", "direct", "divide", "domain", "donate", "double",
    "dragon", "driver", "during", "easily", "eating", "editor", "effect",
    "effort", "emerge", "empire", "employ", "enable", "ending", "energy",
    "engage", "engine", "enough", "ensure", "entire", "entity", "equity",
    "escape", "estate", "ethnic", "evolve", "exceed", "except", "expand",
    "expect", "expert", "export", "extent", "fabric", "factor", "fairly",
    "family", "famous", "father", "feature", "federal", "fiction", "fifteen",
    "figure", "filter", "finger", "finish", "flavor", "flight", "flower",
    "follow", "forest", "forget", "formal", "former", "foster", "frozen",
    "future", "galaxy", "gamble", "garden", "gather", "gender", "gentle",
    "global", "golden", "govern", "growth", "guitar", "handle", "happen",
    "hardly", "heaven", "height", "hidden", "highway", "honest", "horror",
    "hunger", "hunter", "ignore", "impact", "import", "impose", "income",
    "indeed", "infant", "inform", "injury", "insert", "inside",
    "intend", "invest", "island", "jersey", "jockey", "junior",
    "justice", "kidney", "killer", "kitchen", "knight", "launch", "lawyer",
    "leader", "league", "legacy", "legend", "length", "lesson", "letter",
    "liberal", "likely", "listen", "little", "living", "lonely", "lovely",
    "luxury", "mainly", "manage", "manner", "market", "master", "matter",
    "medium", "member", "memory", "mental", "merger", "method", "middle",
    "mighty", "miller", "minute", "mirror", "mobile", "modern", "modest",
    "moment", "monkey", "mother", "motion", "motive", "murder", "museum",
    "mutual", "myself", "namely", "narrow", "nation", "nature", "nearby",
    "nearly", "nicely", "nobody", "normal", "notice", "notion", "number",
    "object", "obtain", "occupy", "offend", "office", "online", "oppose",
    "option", "orange", "origin", "outfit", "output", "oxygen", "palace",
    "parent", "partly", "patent", "patrol", "patron", "pencil", "people",
    "period", "permit", "person", "phrase", "planet", "player", "please",
    "plenty", "pocket", "poetry", "police", "policy", "portal", "poster",
    "potato", "powder", "prayer", "prefer", "prince", "prison", "profit",
    "prompt", "proper", "public", "purple", "pursue", "puzzle", "python",
    "rabbit", "random", "rather", "reason", "recipe", "record", "reduce",
    "reform", "regard", "regime", "region", "reject", "relate", "relief",
    "remain", "remote", "remove", "repair", "repeat", "report", "rescue",
    "resist", "resort", "result", "retain", "retire", "return", "reveal",
    "review", "reward", "rhythm", "ritual", "rocket", "rubber", "sacred",
    "safety", "salmon", "sample", "saying", "scheme", "school", "search",
    "season", "secret", "sector", "secure", "select", "senior", "series",
    "server", "settle", "shadow", "shield", "signal", "silent", "silver",
    "simple", "singer", "single", "sister", "smooth", "sought",
    "source", "speech", "spirit", "spread", "square", "stable", "status",
    "steady", "strain", "strand", "stream", "street", "stress", "strict",
    "strike", "string", "stroke", "strong", "studio", "submit", "sudden",
    "suffer", "summer", "summit", "supply", "surely", "survey", "switch",
    "symbol", "talent", "target", "temple", "tender", "terror", "thanks",
    "thread", "throat", "ticket", "timber", "tissue", "tongue", "toward",
    "treaty", "tribal", "tunnel", "turtle", "twelve", "unique", "united",
    "unlike", "update", "upward", "useful", "valley", "vendor", "vessel",
    "victim", "vision", "visual", "volume", "walker", "wealth", "weapon",
    "weekly", "weight", "window", "winner", "winter", "wisdom", "wonder",
    "worker", "worthy", "writer", "zombie",
]

# Filter to 5-10 letter words
WORDS = [w.lower() for w in WORDS if 5 <= len(w) <= 10]

HANGMAN_STAGES = [
    # 0 wrong
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │     ",
        "  │     ",
        "  │     ",
        "  ═════ ",
    ],
    # 1 wrong - head
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │     ",
        "  │     ",
        "  ═════ ",
    ],
    # 2 wrong - body
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │   │ ",
        "  │     ",
        "  ═════ ",
    ],
    # 3 wrong - left arm
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │  /│ ",
        "  │     ",
        "  ═════ ",
    ],
    # 4 wrong - right arm
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │  /│\\",
        "  │     ",
        "  ═════ ",
    ],
    # 5 wrong - left leg
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │  /│\\",
        "  │  /  ",
        "  ═════ ",
    ],
    # 6 wrong - right leg (dead)
    [
        "  ┌───┐ ",
        "  │   │ ",
        "  │   O ",
        "  │  /│\\",
        "  │  / \\",
        "  ═════ ",
    ],
]


def run_game(stdscr):
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_CYAN, -1)    # title
    curses.init_pair(2, curses.COLOR_WHITE, -1)    # text
    curses.init_pair(3, curses.COLOR_GREEN, -1)    # correct
    curses.init_pair(4, curses.COLOR_RED, -1)      # wrong/hangman
    curses.init_pair(5, curses.COLOR_YELLOW, -1)   # word display

    TITLE = curses.color_pair(1) | curses.A_BOLD
    TEXT = curses.color_pair(2)
    CORRECT = curses.color_pair(3) | curses.A_BOLD
    WRONG = curses.color_pair(4) | curses.A_BOLD
    WORD_COLOR = curses.color_pair(5) | curses.A_BOLD

    curses.curs_set(0)
    stdscr.nodelay(False)

    h, w = stdscr.getmaxyx()
    if h < 20 or w < 40:
        stdscr.clear()
        try:
            stdscr.addstr(0, 0, "Terminal too small. Need at least 40x20.")
            stdscr.addstr(1, 0, "Press any key to exit.")
        except curses.error:
            pass
        stdscr.getch()
        return False

    word = random.choice(WORDS).upper()
    guessed = set()
    wrong_guesses = 0
    max_wrong = 6
    message = ""
    game_over = False
    game_won = False

    def draw():
        stdscr.clear()
        off_x = max(0, (w - 40) // 2)
        off_y = max(0, (h - 20) // 2)

        # Title
        try:
            stdscr.addstr(off_y, off_x, "H A N G M A N", TITLE)
        except curses.error:
            pass

        # Hangman ASCII art
        stage = HANGMAN_STAGES[min(wrong_guesses, 6)]
        for i, line in enumerate(stage):
            try:
                stdscr.addstr(off_y + 2 + i, off_x, line, WRONG)
            except curses.error:
                pass

        # Word display
        word_display = ""
        for ch in word:
            if ch in guessed:
                word_display += ch + " "
            else:
                word_display += "_ "
        try:
            stdscr.addstr(off_y + 9, off_x, word_display.strip(), WORD_COLOR)
        except curses.error:
            pass

        # Guessed letters
        correct_letters = sorted([ch for ch in guessed if ch in word])
        wrong_letters = sorted([ch for ch in guessed if ch not in word])

        try:
            stdscr.addstr(off_y + 11, off_x, "Correct: ", TEXT)
            stdscr.addstr(off_y + 11, off_x + 9, " ".join(correct_letters) if correct_letters else "-", CORRECT)
            stdscr.addstr(off_y + 12, off_x, "Wrong:   ", TEXT)
            stdscr.addstr(off_y + 12, off_x + 9, " ".join(wrong_letters) if wrong_letters else "-", WRONG)
            stdscr.addstr(off_y + 13, off_x, f"Remaining: {max_wrong - wrong_guesses}", TEXT)
        except curses.error:
            pass

        # Message
        if message:
            try:
                stdscr.addstr(off_y + 15, off_x, message, TEXT)
            except curses.error:
                pass

        # Controls
        if not game_over:
            try:
                stdscr.addstr(off_y + 17, off_x, "Press a letter to guess, Esc to quit", curses.A_DIM)
            except curses.error:
                pass

        stdscr.refresh()

    while not game_over:
        draw()

        key = stdscr.getch()

        if key == 27:  # Escape to quit (not Q — it's a letter game!)
            return False

        if 65 <= key <= 122:
            ch = chr(key).upper()
            if not ch.isalpha():
                continue
            if ch in guessed:
                message = f"Already guessed '{ch}'!"
                continue

            guessed.add(ch)
            message = ""

            if ch in word:
                message = f"'{ch}' is in the word!"
                # Check win
                if all(c in guessed for c in word):
                    game_won = True
                    game_over = True
            else:
                wrong_guesses += 1
                message = f"'{ch}' is not in the word."
                if wrong_guesses >= max_wrong:
                    game_over = True

    # Final draw
    draw()

    # End screen
    off_x = max(0, (w - 40) // 2)
    off_y = max(0, (h - 20) // 2)

    if game_won:
        try:
            stdscr.addstr(off_y + 15, off_x, "                                    ", TEXT)
            stdscr.addstr(off_y + 15, off_x, f"You saved the stick figure! Word: {word}", CORRECT)
        except curses.error:
            pass
    else:
        try:
            stdscr.addstr(off_y + 15, off_x, "                                    ", TEXT)
            stdscr.addstr(off_y + 15, off_x, f"The word was: {word}", WRONG)
        except curses.error:
            pass

    try:
        stdscr.addstr(off_y + 17, off_x, "Press any key to continue", curses.A_DIM)
    except curses.error:
        pass

    stdscr.refresh()
    stdscr.getch()
    return game_won


def main(stdscr):
    return run_game(stdscr)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--inspect":
        print()
        print("  hangman.py — Classic Hangman")
        print("  ────────────────────────────")
        print("  Imports: curses, random, sys")
        print("  Network access:  NONE")
        print("  File writes:     NONE")
        print("  File reads:      NONE")
        print("  Subprocesses:    NONE")
        print(f"  Word list:       {len(WORDS)} words (hardcoded)")
        print()
    else:
        curses.wrapper(main)
