# Flash Card App

Flash Card App is a Python desktop application for creating, managing, and reviewing flashcards using a GUI built with PyQt5. It supports sound feedback via `pygame` and tracks user performance in a JSON file.

---

![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-green)
![License](https://img.shields.io/badge/License-MIT-blue.svg)

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the main entry point:

```bash
python main.py
```

### Features

- Create flashcards with `Topic`, `Question`, and `Answer` sections
- Save flashcards as `.txt` files organized in folders
- Review cards in:
  - Random order
  - Sequential order
  - "Incorrect only" mode
- Optional typing animation and sound effects
- Track correct/incorrect answers in `flashcard_results.json`

### Keyboard/Mouse Workflow

- **Flip Card** → `Flip Card` button
- **Mark Correct/Incorrect** → Use checkboxes
- **Advance** → `Next Card` button

## File Structure

| File / Folder                | Description                                                |
|-----------------------------|------------------------------------------------------------|
| `main.py`                   | Starts the application                                     |
| `modules/flashcard_app.py`  | Main window and settings logic                             |
| `modules/flashcard_creator.py` | GUI and logic for creating new flashcards             |
| `modules/flashcard_window.py`  | Flashcard display and review logic                     |
| `sounds/`                   | `.mp3` files for typing, correct, and incorrect sounds     |
| `images/`                   | Background image for flashcard display                    |
| `flashcard_results.json`    | Tracks whether each card was answered correctly            |

## Testing

Unit tests are provided for all main modules:

```bash
python -m unittest discover -s "unit tests"
```

Test coverage includes:

- File handling
- UI behavior
- State management
- JSON persistence

> Note: Sample flashcards for testing should be placed in `unit tests/mock/`

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

Please ensure all new functionality includes corresponding unit tests.

## License

[MIT](https://choosealicense.com/licenses/mit/)

