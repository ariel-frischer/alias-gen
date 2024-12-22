"""
Module for curses-based TUI implementation of alias generation.
"""

import curses
import curses.textpad
from typing import Dict, List, Set, Tuple
from .logger import debug

ResType = List[Tuple[str, int, str, str]]

class AliasGeneratorTUI:
    def __init__(self, commands: List[Tuple[str, int]], used_aliases: Set[str]):
        self.commands = commands
        self.used_aliases = used_aliases.copy()
        self.used_easy_aliases = used_aliases.copy()
        self.selected_commands = set()
        self.current_pos = 0
        self.top_line = 0
        self.custom_aliases: Dict[str, str] = {}
        self.max_y = 0
        self.max_x = 0
        
    def run(self) -> ResType:
        return curses.wrapper(self._main)
    
    def _main(self, stdscr) -> ResType:
        # Setup
        curses.use_default_colors()
        curses.curs_set(0)  # Hide cursor
        stdscr.keypad(True)
        
        # Get screen dimensions
        self.max_y, self.max_x = stdscr.getmaxyx()
        
        while True:
            stdscr.clear()
            
            # Draw header
            header = "Alias Generator TUI - Press '?' for help"
            stdscr.addstr(0, 0, header, curses.A_REVERSE)
            
            # Draw command list
            self._draw_commands(stdscr)
            
            # Draw footer
            footer = "[Space]Select [e]Edit [s]Save [q]Quit [↑↓]Navigate"
            stdscr.addstr(self.max_y-1, 0, footer, curses.A_REVERSE)
            
            stdscr.refresh()
            
            # Handle input
            try:
                key = stdscr.getch()
                if key == ord('q'):
                    return []
                elif key == ord('s'):
                    return self._generate_results()
                elif key == ord('e'):
                    self._edit_alias(stdscr)
                elif key == ord(' '):
                    cmd = self.commands[self.current_pos][0]
                    if cmd in self.selected_commands:
                        self.selected_commands.remove(cmd)
                    else:
                        self.selected_commands.add(cmd)
                elif key == ord('?'):
                    self._show_help(stdscr)
                elif key == curses.KEY_UP and self.current_pos > 0:
                    self.current_pos -= 1
                    if self.current_pos < self.top_line:
                        self.top_line = self.current_pos
                elif key == curses.KEY_DOWN and self.current_pos < len(self.commands) - 1:
                    self.current_pos += 1
                    if self.current_pos >= self.top_line + (self.max_y - 3):
                        self.top_line += 1
            except curses.error:
                continue
    
    def _draw_commands(self, stdscr):
        # Header row
        header = f"{'Command':<20}{'Freq':<8}{'Alias':<12}{'Selected':<8}"
        stdscr.addstr(1, 0, header)
        
        # Calculate visible range
        visible_commands = self.commands[self.top_line:self.top_line + (self.max_y - 3)]
        
        for i, (cmd, freq) in enumerate(visible_commands):
            y = i + 2
            x = 0
            
            # Truncate command if too long
            display_cmd = cmd[:17] + "..." if len(cmd) > 20 else cmd
            display_cmd = f"{display_cmd:<20}"
            
            # Get alias
            alias = self.custom_aliases.get(cmd, cmd[:3])
            
            # Format line
            line = f"{display_cmd}{freq:<8}{alias:<12}"
            
            # Highlight current line
            if self.top_line + i == self.current_pos:
                stdscr.addstr(y, x, line, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, line)
            
            # Show selection status
            if cmd in self.selected_commands:
                stdscr.addstr(y, x + 40, "[X]")
            else:
                stdscr.addstr(y, x + 40, "[ ]")
    
    def _edit_alias(self, stdscr):
        if not self.commands:
            return
        
        cmd = self.commands[self.current_pos][0]
        current_alias = self.custom_aliases.get(cmd, cmd[:3])
        
        # Create input window
        input_win = curses.newwin(3, 30, self.max_y//2-1, self.max_x//2-15)
        input_win.box()
        input_win.addstr(0, 1, f" Edit alias for {cmd[:15]}... ")
        
        # Create textbox
        editwin = curses.newwin(1, 20, self.max_y//2, self.max_x//2-10)
        editwin.addstr(0, 0, current_alias)
        box = curses.textpad.Textbox(editwin)
        
        # Let the user edit until Ctrl-G is struck
        box.edit()
        
        # Get resulting contents
        new_alias = box.gather().strip()
        if new_alias and new_alias not in self.used_aliases:
            self.custom_aliases[cmd] = new_alias
            self.used_aliases.add(new_alias)
    
    def _show_help(self, stdscr):
        help_text = [
            "Alias Generator TUI Help",
            "",
            "Navigation:",
            "↑/↓ - Move selection up/down",
            "Space - Toggle command selection",
            "e - Edit alias for selected command",
            "s - Save and generate aliases",
            "q - Quit without saving",
            "",
            "Press any key to continue..."
        ]
        
        # Create centered help window
        height = len(help_text) + 2
        width = max(len(line) for line in help_text) + 4
        y = (self.max_y - height) // 2
        x = (self.max_x - width) // 2
        
        help_win = curses.newwin(height, width, y, x)
        help_win.box()
        
        for i, line in enumerate(help_text):
            help_win.addstr(i + 1, 2, line)
        
        help_win.refresh()
        help_win.getch()
    
    def _generate_results(self) -> ResType:
        results = []
        for cmd, freq in self.commands:
            if cmd in self.selected_commands:
                alias = self.custom_aliases.get(cmd, cmd[:3])
                minimal_alias = alias  # In TUI mode, we use the same alias for both
                results.append((cmd, freq, alias, minimal_alias))
        return results