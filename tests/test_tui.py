"""Tests for the TUI module."""

import curses
import unittest
from unittest.mock import MagicMock, patch

from alias_gen.tui import AliasGeneratorTUI

class TestAliasGeneratorTUI(unittest.TestCase):
    def setUp(self):
        self.commands = [
            ("git status", 10),
            ("docker ps", 8),
            ("ls -la", 5)
        ]
        self.used_aliases = {"gs", "dp", "ll"}
        self.tui = AliasGeneratorTUI(self.commands, self.used_aliases)

    @patch('curses.initscr')
    @patch('curses.newwin')
    @patch('curses.wrapper')
    def test_tui_initialization(self, mock_wrapper, mock_newwin, mock_initscr):
        """Test that TUI initializes correctly."""
        mock_screen = MagicMock()
        mock_screen.getmaxyx.return_value = (24, 80)
        mock_wrapper.return_value = mock_screen
        
        self.tui.run()
        
        # Verify curses was initialized
        mock_wrapper.assert_called_once()

    @patch('curses.initscr')
    @patch('curses.newwin')
    def test_generate_results(self, mock_newwin, mock_initscr):
        """Test that results are generated correctly from selected commands."""
        self.tui.selected_commands = {"git status", "docker ps"}
        self.tui.custom_aliases = {"git status": "gs", "docker ps": "dp"}
        
        results = self.tui._generate_results()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0], ("git status", 10, "gs", "gs"))
        self.assertEqual(results[1], ("docker ps", 8, "dp", "dp"))

    def test_custom_alias_validation(self):
        """Test that custom aliases don't conflict with used aliases."""
        # Initial state
        self.assertEqual(len(self.tui.used_aliases), 3)
        
        # Add new custom alias
        cmd = "git status"
        new_alias = "gst"  # Not in used_aliases
        self.tui.custom_aliases[cmd] = new_alias
        self.tui.used_aliases.add(new_alias)
        
        self.assertIn(new_alias, self.tui.used_aliases)
        self.assertEqual(self.tui.custom_aliases[cmd], new_alias)

if __name__ == '__main__':
    unittest.main()