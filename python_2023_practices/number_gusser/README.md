# Number Guesser

A simple command-line number guessing game written in Python.

## Description

The program generates a random number between **1 and 100**. The player tries to guess the number, and the program provides feedback after each valid guess.

* **Too low** → the guess is lower than the random number.
* **Too high** → the guess is higher than the random number.
* **Correct** → the game ends and the player's score is displayed.
* The player can enter `q` at any time to quit the game.

## Features

* Random number generation using Python's `random` module
* Input validation
* Range validation (1–100)
* Score system
* Quit option
* Feedback after each guess

## How to Run

```bash
python main.py
```

## Scoring

The game starts with a score of **100**.

Each incorrect valid guess reduces the score by **10 points**.
The score cannot go below **0**.

## Technologies

* Python
* `random` module
