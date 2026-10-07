from pathlib import Path

from streamlit.testing.v1 import AppTest

from logic_utils import check_guess

APP_PATH = str(Path(__file__).resolve().parents[1] / "app.py")

# FIX: The three starter tests failed because check_guess returns a tuple, not a
# string. Claude suggested unpacking it rather than changing the return type,
# since app.py needs both the outcome and the message, and I agreed.


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result, _ = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result, _ = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result, _ = check_guess(40, 50)
    assert result == "Too Low"


# --- Regression tests for the backwards hints ---

def test_guess_above_secret_tells_player_to_go_lower():
    # The hint is advice for the next guess, not a restatement of the outcome.
    # Guessing above the secret must point the player DOWN.
    outcome, message = check_guess(15, 7)
    assert "LOWER" in message


def test_guess_below_secret_tells_player_to_go_higher():
    outcome, message = check_guess(3, 7)
    assert "HIGHER" in message


def test_comparison_is_numeric_not_alphabetical():
    # 9 < 10 numerically, but "9" > "10" alphabetically. If the secret is ever
    # compared as a string again, this flips to "Go LOWER".
    outcome, message = check_guess(9, 10)
    assert "HIGHER" in message


# --- Regression tests for the "New Game" / clear cache bug ---
#
# This bug is not in a pure function, so these use Streamlit's AppTest harness:
# it runs app.py heedlessly so we can click real buttons and read session_state.
#
# The bug: "New Game" reset the secret but left `status` as "won"/"lost", so the
# st.stop() guard killed the script before the Submit handler could run. The
# board looked fresh but the game was dead. Clearing the cache was the only way
# out, because that wiped session_state and re-ran the initializers.


def finished_game(status):
    """Run the app and leave it sitting in a finished ("won" or "lost") state."""
    at = AppTest.from_file(APP_PATH)
    at.run()
    at.session_state.status = status
    at.run()
    return at


def click(at, label):
    """Click the first button whose label contains `label`, then rerun."""
    button = next(b for b in at.button if label in b.label)
    button.click()
    at.run()
    return at


def test_new_game_makes_a_finished_game_playable_again():
    # The core regression: without resetting status, this stays "lost".
    at = finished_game("lost")
    click(at, "New Game")
    assert at.session_state.status == "playing"


def test_submit_works_after_new_game():
    # The symptom the player actually saw: the guess did nothing.
    at = finished_game("lost")
    click(at, "New Game")

    at.text_input(key="guess_input_Normal").set_value("42")
    click(at, "Submit Guess")

    assert at.session_state.history == [42]
    assert at.session_state.attempts == 1


def test_new_game_clears_the_previous_games_score_and_history():
    at = finished_game("won")
    at.session_state.score = 85
    at.session_state.history = [10, 20, 30]
    at.run()

    click(at, "New Game")

    assert at.session_state.score == 0
    assert at.session_state.history == []


def test_new_game_secret_respects_the_difficulty_range():
    # Easy is 1-20, but the reset hardcoded randint(1, 100), so a new Easy game
    # could hold an unreachable secret like 87. Repeat to beat the randomness.
    at = AppTest.from_file(APP_PATH)
    at.run()
    at.selectbox[0].set_value("Easy").run()

    for _ in range(15):
        click(at, "New Game")
        assert 1 <= at.session_state.secret <= 20
