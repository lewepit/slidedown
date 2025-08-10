import os
import sys
import re
import curses
import subprocess
import argparse

class SlideDown:
    def __init__(self, filename, timeout=3):
        with open(filename, 'r') as f:
            content = f.read()
        self.slides = re.split(r'\n---\n', content)
        self.current_slide = 0
        self.timeout = timeout
        
        self.themes = {
            "default": {
                "header": curses.COLOR_CYAN,
                "code": curses.COLOR_GREEN,
                "border": curses.COLOR_WHITE,
                "footer": curses.COLOR_BLACK,
                "output": curses.COLOR_WHITE,
                "shortened": curses.COLOR_YELLOW,
                "error": curses.COLOR_RED
            },
            "dark": {
                "header": curses.COLOR_RED,
                "code": curses.COLOR_YELLOW,
                "border": curses.COLOR_BLUE,
                "footer": curses.COLOR_BLUE,
                "output": curses.COLOR_YELLOW,
                "shortened": curses.COLOR_MAGENTA,
                "error": curses.COLOR_YELLOW
            },
            "matrix": {
                "header": curses.COLOR_GREEN,
                "code": curses.COLOR_GREEN,
                "border": curses.COLOR_BLACK,
                "footer": curses.COLOR_BLACK,
                "output": curses.COLOR_GREEN,
                "shortened": curses.COLOR_CYAN,
                "error": curses.COLOR_GREEN
            }
        }
        self.current_theme = "default"
        self.code_preview_size = {}
    
    def display_slide(self, stdscr):
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        if height < 10 or width < 20:
            stdscr.addstr(0, 0, "Terminal too small! Please resize.", curses.A_BOLD)
            stdscr.refresh()
            return
        
        theme = self.themes[self.current_theme]
        curses.init_pair(1, theme["header"], curses.COLOR_BLACK)
        curses.init_pair(2, theme["code"], curses.COLOR_BLACK)
        curses.init_pair(3, theme["border"], curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_BLACK, theme["footer"])
        curses.init_pair(5, theme["output"], curses.COLOR_BLACK)
        curses.init_pair(6, theme["shortened"], curses.COLOR_BLACK)
        curses.init_pair(7, theme["error"], curses.COLOR_BLACK)
        
        header_text = " SLIDEDOWN "
        try:
            stdscr.addstr(0, 0, header_text.center(width, '='), curses.color_pair(3) | curses.A_REVERSE)
        except curses.error:
            pass
        
        footer_text = (f" ←/→: Navigate | q: Quit | t: Theme | Timeout: {self.timeout}s | "
                       f"Slide {self.current_slide+1}/{len(self.slides)} ")
        safe_footer = footer_text[:width-1]
        try:
            stdscr.addstr(height-1, 0, safe_footer.ljust(width, '-'), curses.color_pair(4) | curses.A_REVERSE)
        except curses.error:
            pass
        
        content = self.slides[self.current_slide]
        y_offset = 2
        in_code_block = False
        code_lines = []
        code_lang = ""
        code_flags = []
        
        for line in content.split('\n'):
            if y_offset >= height - 2:  
                break
                
            if line.strip().startswith('```'):
                if in_code_block:
                    self._render_code_block(stdscr, y_offset, code_lang, code_flags, code_lines, height, width)
                    y_offset += len(code_lines) + 2
                    if y_offset >= height - 2:
                        break
                    in_code_block = False
                    code_lines = []
                    code_lang = ""
                    code_flags = []
                else:
                    in_code_block = True
                    lang_str = line.strip()[3:].strip()
                    parts = lang_str.split()
                    code_lang = parts[0] if parts else "text"
                    code_flags = parts[1:] if len(parts) > 1 else []
            elif in_code_block:
                code_lines.append(line)
            else:
                try:
                    if line.startswith('# '):
                        if y_offset < height - 2:
                            stdscr.addstr(y_offset, 2, line[2:], curses.color_pair(1) | curses.A_BOLD)
                            y_offset += 2
                    elif line.startswith('## '):
                        if y_offset < height - 2:
                            stdscr.addstr(y_offset, 2, line[3:], curses.color_pair(1))
                            y_offset += 2
                    elif line.startswith('### '):
                        if y_offset < height - 2:
                            stdscr.addstr(y_offset, 2, line[4:], curses.A_UNDERLINE)
                            y_offset += 1
                    elif line.startswith('- '):
                        if y_offset < height - 2:
                            stdscr.addstr(y_offset, 2, '• ' + line[2:])
                            y_offset += 1
                    elif line.strip() == '':
                        y_offset += 1
                    else:
                        if y_offset < height - 2:
                            stdscr.addstr(y_offset, 2, line)
                            y_offset += 1
                except curses.error:
                    y_offset += 1
        
        stdscr.refresh()

    def _render_code_block(self, stdscr, y_offset, lang, flags, code_lines, max_height, max_width):
        if not code_lines or y_offset >= max_height - 2:
            return
        
        height, width = max_height, max_width
        theme = self.themes[self.current_theme]
        output_only = "output_only" in flags
        is_live = "live" in flags
        
        if output_only:
            if is_live:
                try:
                    code = '\n'.join(code_lines)
                    process = subprocess.run(
                        ['python', '-c', code],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT,
                        text=True,
                        timeout=self.timeout
                    )
                    result = process.stdout
                    
                    output_lines = result.split('\n')
                    for i, line in enumerate(output_lines):
                        if y_offset + i < height - 2:
                            safe_line = line[:width-5]
                            stdscr.addstr(y_offset + i, 3, safe_line, curses.color_pair(5))
                except subprocess.TimeoutExpired as e:
                    error_msg = f"» Error: Execution timed out ({self.timeout}s)"
                    stdscr.addstr(y_offset, 3, error_msg, curses.color_pair(7) | curses.A_BOLD)
                except Exception as e:
                    error_msg = f"» Error: {str(e)}"
                    stdscr.addstr(y_offset, 3, error_msg, curses.color_pair(7) | curses.A_BOLD)
            return
        
        slide_id = f"{self.current_slide}-{lang}"
        if slide_id in self.code_preview_size:
            max_display_lines = self.code_preview_size[slide_id]
        else:
            max_display_lines = min(len(code_lines), max(10, height - y_offset - 10))
            self.code_preview_size[slide_id] = max_display_lines
        
        shortened = False
        if max_display_lines < len(code_lines):
            shortened = True
            max_display_lines = max(3, max_display_lines - 1)
        
        try:
            if y_offset - 1 < height:
                stdscr.addstr(y_offset - 1, 1, '+' + '-' * (width - 4) + '+', curses.color_pair(3))
            
            for i in range(max_display_lines + 2):
                current_y = y_offset + i
                if current_y < height:
                    stdscr.addstr(current_y, 1, '|', curses.color_pair(3))
                    stdscr.addstr(current_y, width - 2, '|', curses.color_pair(3))
            
            if y_offset + max_display_lines + 1 < height:
                stdscr.addstr(y_offset + max_display_lines + 1, 1, '+' + '-' * (width - 4) + '+', curses.color_pair(3))
        except curses.error:
            pass
        
        try:
            if y_offset - 1 < height:
                lang_label = f" {lang} "
                stdscr.addstr(y_offset - 1, 3, lang_label, curses.A_REVERSE)
        except curses.error:
            pass
        
        for i in range(max_display_lines):
            if i < len(code_lines):
                line = code_lines[i]
                safe_line = line[:width-5]
                try:
                    stdscr.addstr(y_offset + i, 3, safe_line, curses.color_pair(2))
                except curses.error:
                    pass
        
        if shortened and (y_offset + max_display_lines < height - 1):
            try:
                stdscr.addstr(y_offset + max_display_lines, 3, "... (code shortened)", curses.color_pair(6) | curses.A_ITALIC)
            except:
                pass
        
        if is_live:
            try:
                code = '\n'.join(code_lines)
                process = subprocess.run(
                    ['python', '-c', code],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=self.timeout
                )
                result = process.stdout
                
                output_start_y = y_offset + max_display_lines + 2
                max_output_lines = max(0, height - output_start_y - 1)
                
                output_lines = result.split('\n')
                
                if len(output_lines) > max_output_lines:
                    needed_space = len(output_lines) - max_output_lines
                    
                    new_max_display = max(3, max_display_lines - needed_space - 2)
                    
                    if new_max_display < max_display_lines:
                        self.code_preview_size[slide_id] = new_max_display
                        
                        stdscr.clear()
                        self.display_slide(stdscr)
                        return
                
                if output_start_y < height - 2 and max_output_lines > 0:
                    try:
                        stdscr.addstr(output_start_y, 3, "» Output:", curses.A_BOLD | curses.color_pair(5))
                        for i, line in enumerate(output_lines):
                            if output_start_y + i + 1 < height - 2:
                                safe_line = line[:width-5]
                                stdscr.addstr(output_start_y + i + 1, 5, safe_line, curses.color_pair(5))
                    except curses.error:
                        pass
            except subprocess.TimeoutExpired as e:
                self._handle_error(stdscr, y_offset, max_display_lines, f"Execution timed out ({self.timeout}s)", height, width)
            except Exception as e:
                self._handle_error(stdscr, y_offset, max_display_lines, str(e), height, width)
    
    def _handle_error(self, stdscr, y_offset, code_lines_count, message, max_height, max_width):
        height, width = max_height, max_width
        output_y = y_offset + code_lines_count + 2
        if output_y < height - 2:
            try:
                error_msg = f"» Error: {message}"
                error_lines = []
                current_line = ""
                for word in error_msg.split():
                    if len(current_line) + len(word) + 1 <= width - 5:
                        current_line += word + " "
                    else:
                        error_lines.append(current_line)
                        current_line = word + " "
                if current_line:
                    error_lines.append(current_line)
                
                max_error_lines = max(0, height - output_y - 1)
                display_lines = error_lines[:max_error_lines]
                
                for i, line in enumerate(display_lines):
                    if output_y + i < height - 2:
                        stdscr.addstr(output_y + i, 3, line, curses.color_pair(7) | curses.A_BOLD)
            except curses.error:
                pass

    def run(self):
        curses.wrapper(self._main_loop)

    def _main_loop(self, stdscr):
        curses.curs_set(0)  
        stdscr.keypad(True)  
        while True:
            self.code_preview_size = {}
            
            self.display_slide(stdscr)
            key = stdscr.getkey()
            
            if key in ('q', 'Q'):
                break
            elif key in ('KEY_RIGHT', 'n', ' ', 'l'):
                self.current_slide = min(self.current_slide + 1, len(self.slides) - 1)
            elif key in ('KEY_LEFT', 'p', 'h'):
                self.current_slide = max(self.current_slide - 1, 0)
            elif key == 't':
                themes = list(self.themes.keys())
                current_index = themes.index(self.current_theme)
                self.current_theme = themes[(current_index + 1) % len(themes)]
            elif key in ('KEY_HOME', 'g'):
                self.current_slide = 0
            elif key in ('KEY_END', 'G'):
                self.current_slide = len(self.slides) - 1
            elif key == '+':
                self.timeout = min(60, self.timeout + 1)
            elif key == '-':
                self.timeout = max(1, self.timeout - 1)
            elif key == 'r':
                pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Slidedown - Terminal Markdown Presentation Engine")
    parser.add_argument("file", help="Markdown presentation file")
    parser.add_argument("-t", "--timeout", type=int, default=3,
                        help="Execution timeout for live code blocks in seconds (default: 3)")
    args = parser.parse_args()
    
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found")
        sys.exit(1)
    
    presenter = SlideDown(args.file, timeout=args.timeout)
    presenter.run()