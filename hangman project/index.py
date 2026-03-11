"""
Hangman — Console Game
OOP: WordBank, HangmanDisplay, Player, HangmanGame classes
"""

import random
# WordBank — manages the word pool
class WordBank:
    WORDS = [
        # Tech
        "python", "javascript", "algorithm", "database", "network",
        "compiler", "recursion", "variable", "function", "inheritance",
        # Animals
        "elephant", "crocodile", "butterfly", "penguin", "dolphin",
        # General
        "keyboard", "mountain", "umbrella", "calendar", "adventure",
        "chocolate", "hospital", "language", "treasure", "champion",
    ]

    @staticmethod
    def get_random_word() -> str:
        """Return a random word from the word bank."""
        return random.choice(WordBank.WORDS)


class HangmanDisplay:
    STAGES = [
        # 0 wrong guesses
        """
  +---+
  |   |
      |
      |
      |
      |
=========""",
        # 1 wrong guess
        """
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
        # 2 wrong guesses
        """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
        # 3 wrong guesses
        """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
        # 4 wrong guesses
        """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========""",
        # 5 wrong guesses
        """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========""",
        # 6 wrong guesses — dead
        """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========""",
    ]

    MAX_WRONG = len(STAGES) - 1  # 6

    @staticmethod
    def show(wrong_count: int):
        """Print the hangman stage for the given number of wrong guesses."""
        print(HangmanDisplay.STAGES[wrong_count])



# Player — tracks guesses and wrong attempts

class Player:
    def __init__(self, name: str):
        self.name          = name
        self.guessed       = set()   # all letters guessed so far
        self.wrong_guesses = []      # only the incorrect ones

    @property
    def wrong_count(self) -> int:
        return len(self.wrong_guesses)

    def has_guessed(self, letter: str) -> bool:
        return letter in self.guessed

    def record_guess(self, letter: str, correct: bool):
        """Record a guess. Add to wrong list if incorrect."""
        self.guessed.add(letter)
        if not correct:
            self.wrong_guesses.append(letter)

    def __str__(self):
        return self.name


# HangmanGame — orchestrates the game
class HangmanGame:
    def __init__(self, player: Player):
        self.player  = player
        self.word    = WordBank.get_random_word()
        self._won    = False


    def _show_word(self):
        """Print the word with guessed letters revealed."""
        display = " ".join(
            letter if self.player.has_guessed(letter) else "_"
            for letter in self.word
        )
        print(f"\n  Word: {display}  ({len(self.word)} letters)")

    def _show_status(self):
        """Print wrong guesses and remaining attempts."""
        remaining = HangmanDisplay.MAX_WRONG - self.player.wrong_count
        wrong     = ", ".join(self.player.wrong_guesses) if self.player.wrong_guesses else "none"
        print(f"  Wrong guesses : {wrong}")
        print(f"  Attempts left : {remaining}")

    def _is_word_solved(self) -> bool:
        """Return True if every letter in the word has been guessed."""
        return all(self.player.has_guessed(c) for c in self.word)

    def _get_input(self) -> str:
        """Prompt until a valid, unused single letter is entered."""
        while True:
            guess = input(f"\n  {self.player}, enter a letter: ").strip().lower()

            if len(guess) != 1 or not guess.isalpha():
                print("  Please enter a single letter (a–z).")
                continue

            if self.player.has_guessed(guess):
                print(f"  You already guessed '{guess}'. Try a different letter.")
                continue

            return guess

    def _process_guess(self, letter: str):
        """Check the guess, update player state, and give feedback."""
        correct = letter in self.word
        self.player.record_guess(letter, correct)

        if correct:
            print(f"  ✓ '{letter}' is in the word!")
        else:
            print(f"  ✗ '{letter}' is not in the word.")

    def play(self):
        """Main game loop."""
        print("\n" + "=" * 40)
        print(f"   Welcome to Hangman, {self.player}!")
        print("=" * 40)
        print(f"  Guess the {len(self.word)}-letter word one letter at a time.")
        print(f"  You have {HangmanDisplay.MAX_WRONG} wrong guesses allowed.\n")

        while True:
            HangmanDisplay.show(self.player.wrong_count)
            self._show_word()
            self._show_status()

            # ── win check ──
            if self._is_word_solved():
                self._won = True
                print(f"\n  🎉 You solved it! The word was '{self.word}'. Well done, {self.player}!")
                break

            # ── lose check ──
            if self.player.wrong_count >= HangmanDisplay.MAX_WRONG:
                print(f"\n  💀 Game over! The word was '{self.word}'. Better luck next time!")
                break

            guess = self._get_input()
            self._process_guess(guess)

    def result_summary(self):
        """Print a short summary after the game ends."""
        print("\n" + "-" * 40)
        print(f"  Result      : {'WIN 🎉' if self._won else 'LOSS 💀'}")
        print(f"  Word        : {self.word}")
        print(f"  Wrong guesses ({self.player.wrong_count}): "
              f"{', '.join(self.player.wrong_guesses) if self.player.wrong_guesses else 'none'}")
        print(f"  Total guesses: {len(self.player.guessed)}")
        print("-" * 40)

# Entry point
if __name__ == "__main__":
    name   = input("Enter your name: ").strip() or "Player"
    player = Player(name)
    game   = HangmanGame(player)
    game.play()
    game.result_summary()
