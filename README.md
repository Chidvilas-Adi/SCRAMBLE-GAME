# Word Scramble Arena

An interactive word-scramble puzzle game built with Python and Pygame. The player unscrambles randomly selected words, uses hints when needed, races against a round timer, and interacts with individual letter tiles.

## Features

* Random word selection from a built-in dictionary.
* Scrambled letters displayed as individual interactive tiles.
* Player can rearrange/select letters to form the intended word.
* Text-box input for submitting the unscrambled word.
* Correct-answer validation against the original secret word.
* `SUBMIT` button and Enter/Return key support.
* `HINT` button that reveals the next unrevealed letter.
* Hint usage applies a score penalty.
* Round countdown timer.
* Automatic transition to the next round when time expires.
* Score tracking.
* Feedback messages for correct and incorrect guesses.
* Empty submissions are handled without advancing the round.
* Automatic uppercase handling for player input.

## Requirements

* Python 3.10+
* Pygame

## Installation

Clone the repository:

```bash
git clone https://github.com/Chidvilas-Adi/SCRAMBLE-GAME.git
cd SCRAMBLE-GAME
```

Create and activate a virtual environment:

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install Pygame:

```bash
pip install pygame
```

Run the game:

```bash
python main.py
```

## Controls

* Type letters into the input box.
* Press `Enter` or click `SUBMIT` to submit an answer.
* Click `HINT` to reveal the next letter.
* Use the letter tiles to experiment with different arrangements.
* Complete the word before the countdown expires.

## Game Behavior

At the beginning of each round, a word is selected and its letters are shuffled.

For example:

```text
Original word:
PYTHON

Scrambled:
Y H T O N P
```

The player must enter:

```text
PYTHON
```

A correct answer awards one point and starts the next round.

An incorrect answer displays a warning and clears the input field without advancing the round.

Using a hint reveals the next unrevealed letter and applies a score penalty.

If the timer reaches zero before the player answers correctly, the game displays the correct word, shows a `TIME'S UP!` message, and starts the next round.

## Project Structure

```text
SCRAMBLE-GAME/
├── game/
│   ├── game_engine.py
│   └── text_box.py
├── main.py
├── README.md
├── .gitignore
└── .python-version
```

## Bug Fixed

The original implementation incorrectly compared the player's guess against the scrambled word:

```python
is_correct = (guess == self.scrambled_word)
```

This caused a correctly unscrambled answer to be rejected.

The validation was corrected to compare the player's guess with the original secret word:

```python
is_correct = (guess == self.secret_word)
```

## Completed Tasks

### Task 1 — Guess Validation

Fixed the comparison so the player's answer is checked against `self.secret_word`.

### Task 2 — Hint System

Added a `HINT` button that reveals unrevealed letters in their correct positions and applies a score penalty.

### Task 3 — Countdown Timer

Added a round timer that counts down while the player is solving the word. When the timer expires, the correct answer is revealed and the game moves to the next round.

### Task 4 — Interactive Letter Tiles

Changed the static scrambled-letter display into individual graphical letter tiles that can be interacted with to experiment with different letter arrangements.

## Development

This project was completed as part of Lab 4: Vibe Coding. An LLM was used as a debugging and pair-programming assistant. The implementation was developed iteratively by identifying the existing bug, reviewing the generated suggestions, testing the changes, and implementing the required features.

## Submission

The Lab 4 submission contains:

* Before-change gameplay video.
* After-change gameplay video.
* Updated source code.
* Complete LLM/chat history.
