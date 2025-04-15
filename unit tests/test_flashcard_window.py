# =============================================================================
# @file    test_flashcard_window.py
# @project Flash Card App - Unit Tests
# @version 1.0
# @date    15-April-2025
# @author  Brandon Trundle
# @brief   Unit tests for flashcard_window.py
# =============================================================================

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add module directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from modules.flashcard_window import FlashCardWindow

app = QApplication([])

class TestFlashCardWindow(unittest.TestCase):
    def setUp(self):
        self.mock_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock'))
        self.mock_file = os.path.join(self.mock_dir, 'sample_flashcard.txt')
        os.makedirs(self.mock_dir, exist_ok=True)

        with open(self.mock_file, 'w') as f:
            f.write("""Topic: Math\n\nQuestion:\nWhat is 2+2?\n\nAnswer:\n4\n""")


        self.window = FlashCardWindow([self.mock_file], is_random=False, json_path=os.path.join(self.mock_dir, 'results.json'), sound_enabled=False)

    def tearDown(self):
        for file in os.listdir(self.mock_dir):
            file_path = os.path.join(self.mock_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    def test_load_flashcard_sets_content_correctly(self):
        self.assertEqual(self.window.topic, "Math")
        self.assertEqual(self.window.question.strip(), "What is 2+2?")
        self.assertEqual(self.window.answer.strip(), "4")

    def test_mark_correct_updates_results_json(self):
        self.window.mark_correct(Qt.Checked)
        with open(self.window.json_path, 'r') as file:
            results = json.load(file)
        self.assertTrue(results['flashcards'][self.mock_file])

    def test_mark_incorrect_updates_results_json(self):
        self.window.mark_incorrect(Qt.Checked)
        with open(self.window.json_path, 'r') as file:
            results = json.load(file)
        self.assertFalse(results['flashcards'][self.mock_file])

    def test_next_flashcard_loops_correctly(self):
        self.window.current_index = 0
        self.window.next_flashcard()
        self.assertEqual(self.window.current_index, 0)  # Should loop back since only 1 card

if __name__ == '__main__':
    unittest.main()