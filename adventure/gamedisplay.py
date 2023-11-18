import curses
import collections

Displaytext = collections.namedtuple('Displaytext', ['text', 'color'])

class Display:
    DEFAULT = 0
    GREEN = 2
    YELLOW = 3

    def __init__(self, stdscr):
        self.stdscr = stdscr
        
        curses.start_color()
        curses.use_default_colors()

        curses.echo()

        curses.init_pair(2, 2, -1)
        curses.init_pair(3, 3, -1)

        self.displayable: list[Displaytext] = []
        
    def update(self):
        self.stdscr.clear()
        y = 0
        for k in range(max(0, len(self.displayable) - (curses.LINES - 1)), len(self.displayable)):
            self.stdscr.addnstr(y, 0, self.displayable[k].text, curses.COLS - 1, curses.color_pair(self.displayable[k].color))
            y += 1
        self.stdscr.refresh()

    def add_text(self, text: str, color: int=0):
        if text:
            for line in text.split("\n"):
                self.displayable.append(Displaytext(line, color))

    def hint_prompt(self) -> str:
        hint_prompt = "Give chatGPT a hint, or just press enter to continue: "
        self.stdscr.addnstr(curses.LINES - 1, 0, hint_prompt, curses.COLS - 1, curses.color_pair(Display.DEFAULT))
        hint = self.stdscr.getstr(curses.LINES - 1, len(hint_prompt)) 
        self.stdscr.clrtoeol()
        self.stdscr.refresh()
        return hint.decode('utf-8')
    
    def add_hint(self, hint: str):
        self.add_text(f"User hint: {hint}\n", Display.GREEN)

    def add_gameplay(self, gameplay: str):
        self.add_text(gameplay, Display.DEFAULT)

    def add_thinking(self, thinking: str):
        self.add_text(thinking, Display.YELLOW)
    
    def loading(self):
        self.stdscr.addnstr(curses.LINES - 1, 0, "ChatGPT is thinking...", curses.COLS - 1, curses.color_pair(Display.DEFAULT))
        self.stdscr.refresh()
