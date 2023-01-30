import json
import random
from typing import List

from hangman import Hangman


def choose_a_random_word() -> str:
    random_letter_number = random.randrange(97, 123)
    with open(f"./words/{chr(random_letter_number)}.json", "r") as f:
        detail = json.load(f)
    w_d = random.choice(detail.get("res"))
    return w_d


def render_word_state(hangman: Hangman) -> List[str]:
    game_state = hangman.get_current_letter_state()
    word_state = ["_ "] * hangman.word_len()["length"]
    for letter in game_state["letters"]:
        for positions in game_state["letter_to_position"][letter]:
            word_state[positions] = f"{letter} "
    return word_state


if __name__ == "__main__":
    try:
        print("Play Hangman!")
        h = Hangman(choose_a_random_word(), 6)
        while not h.finish_game()[0]:
            state = render_word_state(h)
            print(
                f'You have {h.attempts} tries left. Used letters: Word: {"".join(state)}'
            )
            letter = input("Guess a letter: ")
            h.check_letter(letter)
        state = render_word_state(h)
        print(f'You have no tries left. Used letters: {"".join(state)}')
        if h.finish_game()[1]["isWin"]:
            print("Congratulations! You won!")
        else:
            print(
                f"Sorry, try one more time, you lost. The word was {h.words_details['word']}"
            )

    except KeyboardInterrupt:
        print("Thanks for playing")
