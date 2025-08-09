import os
import sys
import re
import curses

class SlideDown:
    def __init__(self, filename):
        with open(filename, 'r') as f:
            content = f.read()
        self.slides = re.split(r'\n---\n', content)
        self.current_slide = 0
    
    def display_slide(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        stdscr.addstr(0, 0, " SLIDEDOWN ".center(width, '▓'), curses.A_REVERSE)
        footer = f" ←/→: Navigate | q: Quit | Slide {self.current_slide+1}/{len(self.slides)} "
        stdscr.addstr(height-1, 0, footer.center(width, '░'), curses.A_REVERSE)
        
        content = self.slides[self.current_slide]
        for y, line in enumerate(content.split('\n'), 2):
            if y < height-1:
                stdscr.addstr(y, 2, line[:width-4])
        
        stdscr.refresh()

    def run(self):
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr):
        while True:
            self.display_slide(stdscr)
            key = stdscr.getkey()
            
            if key in ('q', 'Q'):
                break
            elif key in ('KEY_RIGHT', 'n', ' '):
                self.current_slide = min(self.current_slide + 1, len(self.slides) - 1)
            elif key in ('KEY_LEFT', 'p'):
                self.current_slide = max(self.current_slide - 1, 0)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: slidedown presentation.md")
        sys.exit(1)
    
    presenter = SlideDown(sys.argv[1])
    presenter.run()
