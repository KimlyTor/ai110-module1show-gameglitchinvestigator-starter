# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [X] Describe the game's purpose.

      The Impossible Guesser is a Streamlit guessing game. The app picks a secret number. You try to guess it before your attempts run out. It tells you "higher" or "lower" after each guess, and tracks your score. As an assignment, its real purpose is to give you broken AI-written code to debug and refactor.
- [X] Detail which bugs you found.

      Bug 1: The hints were wrong. If the guess was 15 and the secret was 7, the hint said "Go HIGHER!" Every hint pushed the player away from the secret instead of toward it.

      Bug 2: The "New Game" button did not start a new game. The secret number changed, but Submit did nothing until the cache was cleared.

      Bug 3: Every game was one attempt short. On Hard, the sidebar said 5 attempts, but the game ended after 4. The same thing happened on Easy and Normal.
- [X] Explain what fixes you applied.

      Bug 1: The hint messages in `check_guess` were swapped, so "Too High" now says "Go LOWER!" A string cast in `app.py` was also removed, so guesses are always compared as numbers. Regression tests were added.

      Bug 2: "New Game" now resets every key the game reads, not just `secret` and `attempts`. The leftover `status` was what blocked Submit. The new secret is also drawn from the current difficulty range.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Open Developer Debug Info. It shows the secret is 56
2. User guesses 36, game shows "Go HIGHER!"
3. User guesses 61, game shows "Go LOWER!"
4. Secret stays 56, attempts count down
5. User guesses 56, game ends with a final score
6. User clicks "New Game", next guess works

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

![A screenshot of a winning game](https://drive.google.com/file/d/1sY9HWgHggpSWCCN6DmPnUZylhiQa0CHv/view?usp=sharing)

## 🧪 Test Results

```
=============================== test session starts ===============================
platform darwin -- Python 3.9.10, pytest-8.4.2, pluggy-1.6.0
rootdir: /Users/ai110-module1show-gameglitchinvestigator-starter
collected 10 items                                                                

tests/test_game_logic.py ..........                                         [100%]

=============================== 10 passed in 1.72s ================================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
