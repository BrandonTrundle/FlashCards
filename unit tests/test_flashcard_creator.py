# =============================================================================
# @file    test_flashcard_creator.py
# @project Flash Card App - Unit Tests
# @version 1.0
# @date    15-April-2025
# @author  Brandon Trundle
# @brief   Unit tests for flashcard_creator.py
# =============================================================================

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication

# Add the 'modules' directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modules')))
from modules.flashcard_creator import FlashCardCreator

app = QApplication([])  # Required for QWidget-based testing

class TestFlashCardCreator(unittest.TestCase):
    def setUp(self):
        self.mock_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'mock'))
        os.makedirs(self.mock_dir, exist_ok=True)
        self.creator = FlashCardCreator(self.mock_dir)

    def tearDown(self):
        # Clean up any created files
        for root, dirs, files in os.walk(self.mock_dir):
            for file in files:
                os.remove(os.path.join(root, file))

    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    @patch('PyQt5.QtWidgets.QFileDialog.getExistingDirectory')
    def test_select_existing_folder(self, mock_get_dir, mock_get_item):
        mock_get_item.return_value = ("Select existing folder", True)
        mock_get_dir.return_value = self.mock_dir

        self.creator.select_or_create_folder()
        self.assertEqual(self.creator.selected_folder, self.mock_dir)

    @patch('PyQt5.QtWidgets.QInputDialog.getItem')
    @patch('PyQt5.QtWidgets.QInputDialog.getText')
    def test_create_new_folder(self, mock_get_text, mock_get_item):
        new_folder = os.path.join(self.mock_dir, "NewFolder")
        mock_get_item.return_value = ("Create new folder", True)
        mock_get_text.return_value = ("NewFolder", True)

        self.creator.select_or_create_folder()
        self.assertTrue(os.path.exists(new_folder))

    @patch('PyQt5.QtWidgets.QInputDialog.getText', return_value=("Math", True))
    @patch.object(FlashCardCreator, 'multi_line_input_dialog', return_value="Some content")
    def test_prompt_flashcard_content_success(self, mock_multi, mock_topic):
        result = self.creator.prompt_flashcard_content()
        self.assertTrue(result)
        self.assertEqual(self.creator.flashcard_content['Topic'], "Math")
        self.assertEqual(self.creator.flashcard_content['Question'], "Some content")
        self.assertEqual(self.creator.flashcard_content['Answer'], "Some content")

    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_save_flashcard_creates_file(self, mock_msg):
        self.creator.selected_folder = self.mock_dir
        self.creator.flashcard_content = {
            "Topic": "Test",
            "Question": "What is 2+2?",
            "Answer": "4"
        }
        self.creator.save_flashcard()

        created_files = [f for f in os.listdir(self.mock_dir) if f.endswith(".txt")]
        self.assertTrue(any("Test" in f for f in created_files))

if __name__ == '__main__':
    unittest.main()