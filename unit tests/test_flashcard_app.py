# =============================================================================
# @file    test_flashcard_app.py
# @project Flash Card App - Unit Tests
# @version 1.0
# @date    15-April-2025
# @author  Brandon Trundle
# @brief   Unit tests for flashcard_app.py
# =============================================================================

import unittest
import sys
import os
import json
from unittest.mock import patch
from PyQt5.QtWidgets import QApplication
from modules.flashcard_app import FlashCardApp

app = QApplication([])  # Required for PyQt widget instantiation in tests

class TestFlashCardApp(unittest.TestCase):
    def setUp(self):
        self.window = FlashCardApp()

    def test_clear_results_no_folder_selected(self):
        self.window.selected_folder = None
        with patch('PyQt5.QtWidgets.QMessageBox.information') as mock_info:
            self.window.clear_results()
            mock_info.assert_called_once_with(self.window, "No Folder Selected", "Please select a folder to clear results.")

    def test_get_flashcard_files_returns_txt_files(self):
        mock_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock', 'card'))
        self.assertTrue(os.path.exists(mock_path), f"Mock path does not exist: {mock_path}")

        result = self.window.get_flashcard_files(folder=mock_path)
        expected = [os.path.join(mock_path, f) for f in os.listdir(mock_path) if f.endswith(".txt")]
        for file in expected:
            self.assertIn(file, result)

    def test_toggle_sound(self):
        initial_state = self.window.sound_enabled
        self.window.toggle_sound()
        self.assertNotEqual(initial_state, self.window.sound_enabled)

    def test_adjust_typing_speed_changes_speed(self):
        with patch('PyQt5.QtWidgets.QInputDialog.getInt', return_value=(80, True)):
            self.window.adjust_typing_speed()
            self.assertEqual(self.window.typing_speed, 80)

    @patch('os.path.exists', return_value=True)
    @patch('os.walk')
    def test_load_folders_populates_combo_box(self, mock_walk, mock_exists):
        mock_walk.return_value = [("/mock/path", ["set1", "set2"], [])]
        self.window.load_folders("/mock/path")
        self.assertEqual(self.window.folder_combo.count(), 2)

if __name__ == '__main__':
    unittest.main()