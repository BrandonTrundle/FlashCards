# =============================================================================
# @file    flashcard_window.py
# @project Flash Card App
# @version 1.0
# @date    15-April-2025
# @author  Brandon Trundle
# @brief   Flashcard review window.
#          This file handles displaying flashcards, flipping between question
#          and answer, playing typing and feedback sounds, and recording results.
# =============================================================================

# =============================================================================
# IMPORTS
# =============================================================================
import os
import random
import json
import pygame
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox, QHBoxLayout
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap

# =============================================================================
# CLASS DEFINITIONS
# =============================================================================
class FlashCardWindow(QWidget):
    def __init__(self, flashcard_files, is_random, json_path="flashcard_results.json", typing_speed=50, sound_enabled=True):
        super().__init__()
        self.flashcard_files = flashcard_files
        self.is_random = is_random
        self.current_index = 0
        self.current_file = None
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.json_path = json_path
        self.typing_speed = typing_speed
        self.sound_enabled = sound_enabled
        self.topic = ""
        self.typing_timer = None
        self.is_typing = False

        # Initialize results dictionary
        self.results = {}

        # Initialize Pygame mixer for sound playback
        pygame.mixer.init()

        # Initialize sound files
        self.typing_sound = pygame.mixer.Sound(os.path.join("sounds", "typing.mp3"))
        self.right_sound = pygame.mixer.Sound(os.path.join("sounds", "right.mp3"))
        self.wrong_sound = pygame.mixer.Sound(os.path.join("sounds", "wrong.mp3"))

        # Load existing results or create a new results dictionary
        self.load_or_create_json()

        if self.is_random:
            self.current_file = random.choice(self.flashcard_files)
        else:
            self.current_file = self.flashcard_files[self.current_index]

        self.initUI()

    # =============================================================================
    #    Function: initUI
    #    Description: Initializes the flashcard UI layout and widgets.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def initUI(self):
        # Set the window title with the topic and file name
        if self.current_file:
            self.setWindowTitle(f"Flashcard - {self.topic} - {os.path.basename(self.current_file)}")
        else:
            self.setWindowTitle("Flashcard")

        self.setGeometry(100, 100, 800, 600)

        self.layout = QVBoxLayout()

        # Label to display the flashcard background image
        self.image_label = QLabel(self)
        self.pixmap = QPixmap(os.path.join("images", "FC.jpg"))
        self.image_label.setPixmap(self.pixmap)
        self.image_label.setScaledContents(True)
        self.layout.addWidget(self.image_label)

        # Label to display topic
        self.topic_label = QLabel(self.image_label)
        self.topic_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        self.topic_label.setStyleSheet("font-size: 24px; color: black;")
        self.topic_label.setGeometry(0, 0, self.width(), 50)

        # Label to display question/answer on top of the image
        self.text_label = QLabel(self.image_label)
        self.text_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.text_label.setStyleSheet("font-size: 36px; color: black;")
        self.text_label.setGeometry(20, 70, self.width() - 40, self.height() - 150)
        
        # Enable word wrap
        self.text_label.setWordWrap(True)

        # Checkboxes for marking right or wrong answers
        checkbox_layout = QHBoxLayout()
        self.right_checkbox = QCheckBox("Right", self)
        self.wrong_checkbox = QCheckBox("Wrong", self)
        self.right_checkbox.stateChanged.connect(self.mark_correct)
        self.wrong_checkbox.stateChanged.connect(self.mark_incorrect)
        checkbox_layout.addWidget(self.right_checkbox)
        checkbox_layout.addWidget(self.wrong_checkbox)
        self.layout.addLayout(checkbox_layout)

        # Button to flip the flashcard
        self.flip_button = QPushButton("Flip Card", self)
        self.flip_button.clicked.connect(self.flip_card)
        self.layout.addWidget(self.flip_button)

        # Button to go to the next flashcard
        self.next_button = QPushButton("Next Card", self)
        self.next_button.clicked.connect(self.next_flashcard)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        # Load the question, answer, and topic from the selected file
        self.load_flashcard(self.current_file)

        # Show the topic and question initially
        self.show_topic()
        self.type_text(self.question)
    
    # =============================================================================
    #    Function: load_flashcard
    #    Description: Loads a flashcard file and extracts topic, question, answer.
    #    Arguments:
    #        - filepath: Path to the flashcard text file.
    #    Returns: None
    # =============================================================================
    def load_flashcard(self, filepath):
        try:
            with open(filepath, "r") as file:
                lines = file.readlines()

                # Find the indices of "Topic:", "Question:", and "Answer:"
                topic_index = None
                question_index = None
                answer_index = None

                for i, line in enumerate(lines):
                    if "Topic:" in line:
                        topic_index = i
                    elif "Question:" in line:
                        question_index = i
                    elif "Answer:" in line:
                        answer_index = i

                if topic_index is None or question_index is None or answer_index is None:
                    raise ValueError("File does not contain the required 'Topic:', 'Question:', and 'Answer:' headers.")

                # Extract the topic, question, and answer sections
                self.topic = lines[topic_index].strip().split(": ")[1]
                self.question = "".join(lines[question_index + 1:answer_index]).strip()
                self.answer = "".join(lines[answer_index + 1:]).strip()

                self.showing_answer = False

        except ValueError as e:
            print(f"ValueError: {e}")
            print("Please ensure the flashcard file contains the 'Topic:', 'Question:', and 'Answer:' headers correctly.")
            self.topic = "Error loading topic."
            self.question = "Error loading question."
            self.answer = "Error loading answer."
        except Exception as e:
            print(f"An error occurred: {e}")
            self.topic = "Error loading topic."
            self.question = "Error loading question."
            self.answer = "Error loading answer."
   
    # =============================================================================
    #    Function: show_topic
    #    Description: Displays the topic label in the flashcard window.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def show_topic(self):
        self.topic_label.setText(f"Topic: {self.topic}")
    
    # =============================================================================
    #    Function: type_text
    #    Description: Simulates typing animation with sound for displaying text.
    #    Arguments:
    #        - text: The text to type out.
    #    Returns: None
    # =============================================================================
    def type_text(self, text):
        # Disable the "Next Card" button while typing is in progress
        self.next_button.setEnabled(False)
        self.is_typing = True
        self.text_label.setText("")  # Clear previous text

        if self.sound_enabled:
            self.typing_sound.play(-1)  # Play typing sound if enabled

        def update_text(i=0):
            if i < len(text):
                self.text_label.setText(self.text_label.text() + text[i])
                self.typing_timer = QTimer.singleShot(int(1000 / self.typing_speed), lambda: update_text(i + 1))
            else:
                self.typing_sound.stop()
                self.is_typing = False  # Typing process is complete
                self.next_button.setEnabled(True)  # Enable the "Next Card" button

        update_text()  # Start the typing process

    # =============================================================================
    #    Function: show_question
    #    Description: Displays the question content.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def show_question(self):
        self.type_text(self.question)
        self.showing_answer = False
        self.right_checkbox.setChecked(False)
        self.wrong_checkbox.setChecked(False)

    # =============================================================================
    #    Function: show_answer
    #    Description: Displays the answer content.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def show_answer(self):
        self.type_text(self.answer)
        self.showing_answer = True
   
    # =============================================================================
    #    Function: flip_card
    #    Description: Flips between showing the question and answer.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def flip_card(self):
        if self.showing_answer:
            self.show_question()
        else:
            self.show_answer()
    
    # =============================================================================
    #    Function: mark_correct
    #    Description: Marks the current flashcard as answered correctly.
    #    Arguments:
    #        - state: The state of the checkbox (Qt.Checked/Unchecked)
    #    Returns: None
    # =============================================================================
    def mark_correct(self, state):
        if state == Qt.Checked:
            self.wrong_checkbox.setChecked(False)
            self.results["flashcards"][self.current_file] = True
            self.save_json()
            if self.sound_enabled:
                print("Right sound should play now")  # Debugging statement
                self.right_sound.play()
    
    # =============================================================================
    #    Function: mark_incorrect
    #    Description: Marks the current flashcard as answered incorrectly.
    #    Arguments:
    #        - state: The state of the checkbox (Qt.Checked/Unchecked)
    #    Returns: None
    # =============================================================================
    def mark_incorrect(self, state):
        if state == Qt.Checked:
            self.right_checkbox.setChecked(False)
            self.results["flashcards"][self.current_file] = False
            self.save_json()
            if self.sound_enabled:
                print("Wrong sound should play now")  # Debugging statement
                self.wrong_sound.play()
    
    # =============================================================================
    #    Function: next_flashcard
    #    Description: Advances to the next flashcard and loads its content.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def next_flashcard(self):
        # Prevent loading the next card if typing is still happening
        if self.is_typing:
            return

        # Stop typing when switching cards
        if self.typing_timer:
            self.typing_timer.stop()

        # Other next flashcard logic...
        if self.is_random:
            self.current_file = random.choice(self.flashcard_files)
        else:
            self.current_index += 1
            if self.current_index >= len(self.flashcard_files):
                self.current_index = 0  # Loop back to the start
            self.current_file = self.flashcard_files[self.current_index]

        # Reset the checkboxes
        self.right_checkbox.setChecked(False)
        self.wrong_checkbox.setChecked(False)

        # Update the window title and load the new flashcard
        self.setWindowTitle(f"Flashcard - {self.topic} - {os.path.basename(self.current_file)}")
        self.load_flashcard(self.current_file)

        # Start typing the question of the new flashcard
        self.show_topic()
        self.type_text(self.question)

    # =============================================================================
    #    Function: load_or_create_json
    #    Description: Loads or initializes the JSON file for tracking results.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def load_or_create_json(self):
        # Load existing results from the JSON file or create a new one
        if os.path.exists(self.json_path):
            with open(self.json_path, "r") as file:
                self.results = json.load(file)
        else:
            self.results = {"flashcards": {}}
    
    # =============================================================================
    #    Function: save_json
    #    Description: Saves the current flashcard results to the JSON file.
    #    Arguments: None
    #    Returns: None
    # =============================================================================
    def save_json(self):
        # Save the current results to the JSON file
        with open(self.json_path, "w") as file:
            json.dump(self.results, file, indent=4)
