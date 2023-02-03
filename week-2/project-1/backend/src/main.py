import json
import random
import pathlib
from typing import List
from setuptools import setup, find_packages
from .hangman import Hangman


def choose_a_random_word() -> dict:
    """A function aimed at choosing a random json dict with the word and its definition from predifined saved file"""
    random_letter_number = random.randrange(97, 123)
    with open(
        f"{pathlib.Path(__file__).parent.resolve()}/words/{chr(random_letter_number)}.json",
        "r",
    ) as f:
        detail = json.load(f)
    w_d = random.choice(detail.get("res"))
    return w_d


def render_word_state(hangman: Hangman) -> List[str]:
    """A function generates a list of string to print letters that are already guessed and used"""
    game_state = hangman.get_current_letter_state()
    word_state = ["_ "] * hangman.word_len()["length"]
    for letter in game_state["letters"]:
        for positions in game_state["letter_to_position"][letter]:
            word_state[positions] = f"{letter} "
    return word_state


def play():
    try:
        print("Play Hangman!")
        h = Hangman(choose_a_random_word(), 6)
        used_letters = []
        while not h.finish_game()[0]:
            state = render_word_state(h)
            print(
                f'You have {h.attempts} tries left. Used letters: {" ".join(used_letters)} Word: {"".join(state)}'
            )
            letter = input("Guess a letter: ")
            h.check_letter(letter)
            used_letters.append(letter)
        print(f'You have no tries left. Used letters: {" ".join(used_letters)}')
        if h.finish_game()[1]["isWin"]:
            print("Congratulations! You won!")
        else:
            print(
                f"Sorry, try one more time, you lost. The word was {h.words_details['word']}"
            )
    except KeyboardInterrupt:
        print("Thanks for playing")
