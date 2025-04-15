# =============================================================================
# @file    main.py
# @project Flash Card App
# @version 1.0
# @date    15-April-2025
# @author  Brandon Trundle
# @brief   Application entry point.
#          This script initializes the Qt application and launches the
#          FlashCardApp main window.
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
import sys
from PyQt5.QtWidgets import QApplication
from Modules.flashcard_app import FlashCardApp

# =============================================================================
#    Entry Point
#    Description: Launches the Qt application and starts the flashcard system.
# =============================================================================
if __name__ == '__main__':
    app = QApplication(sys.argv)
    flashcard = FlashCardApp()
    flashcard.show()
    sys.exit(app.exec_())