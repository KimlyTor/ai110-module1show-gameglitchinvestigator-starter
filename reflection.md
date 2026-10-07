# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?

  The game showed up as a guessing game with easy difficulty. The first thing I noticed was the title "Make a guess"; however, it wasn't clear at first what the player needed to guess. At the bottom of the page, the player entered a number in the input box, clicked "Submit Guess", and looked at the hint telling them to go higher or lower.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

  - Bug 1: The hints were wrong. When the player's guess was higher than the target, the hint showed up as "Go HIGHER", which pushed the player to keep entering a higher number instead of lowering it to get closer to the right answer. The opposite was also true when the player entered a lower number: the hint showed up as "Go LOWER". The correct hint should have helped the player guess a higher number.
  - Bug 2: The "New Game" button didn't start a new game. The target number changed, but the player couldn't submit a guess until the cache was cleared. To do so, the player had to click on the vertical ellipsis icon and click "Clear cache".


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `15`, secret 7 | "Go LOWER!" | "Go HIGHER!" | None|
| Click "New Game", then submit a guess | New game starts, guess accepted | Guess did nothing until cache cleared | None |
| Hard mode, submit wrong guesses | 5 attempts allowed | Game over after 4 | None |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

  Claude
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

  Claude suggested three regression tests for the backwards hints: guess 15 vs secret 7 should say LOWER, guess 3 vs secret 7 should say HIGHER, and guess 9 vs secret 10 should say HIGHER (that last one catches string comparison, since `"9" > "10"`). I accepted all three. I ran pytest in the terminal to verify, and all three passed. I also played the game manually to confirm the hints now point toward the secret.
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

  Claude said the three starter tests were failing because of a mismatch in the result — for instance, `check_guess` returns a tuple, `("Win", "🎉 Correct!")`, not the string `"Win"`. I rejected it because those tests had already been fixed, and I had confirmed that they passed. I ran pytest in the terminal again to be sure, and all three still passed. So I left them alone instead of editing working tests. It was a good reminder to check a claim about my code in the terminal before changing anything on the AI's say-so.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

  I played the game manually first, several times. For the hints, I guessed above and below the secret and checked that the hint pointed toward it. For the "New Game" bug, I finished a game, clicked New Game, and submitted a guess without clearing the cache, and I repeated that a few times to make sure it was not a one-off. Once the game behaved the way I expected, I ran pytest in the terminal so the fix was backed by a test and not just by me clicking around.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

  I thought the hints bug was fixed once I swapped the messages in `check_guess`. However, when I kept playing, I noticed the hint was right on some guesses and wrong on others, which did not match a fix that was supposed to be that simple. I went back to Claude, and it pointed me to app.py, which cast the secret to a string on every other attempt, so those guesses were compared alphabetically instead of numerically. It showed me that a function can be correct on its own and still be broken by how the caller passes data into it.
- Did AI help you design or understand any tests? How?

  Yes. After we fixed the string cast in app.py, I asked Claude how to test it, and it explained that most number pairs would not catch the bug: guess 15 vs secret 7 gives the same hint whether you compare them as ints or as strings. So it designed `test_comparison_is_numeric_not_alphabetical` around a pair where the two disagree — guess 9 vs secret 10, since 9 is less than 10 as numbers but `"9" > "10"` as text. That taught me to choose inputs where a correct and an incorrect version give different answers, instead of just picking any example. 

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

  Streamlit runs the whole file from the top again every time you click or type something. So the script is like a whiteboard that gets erased and redrawn on every click. `st.session_state` is the notebook next to it that nobody erases. That is the only place the game can remember the secret number, because a normal variable would be re-rolled on every click. The "New Game" bug happened because the reset forgot to clear `status` in that notebook.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
