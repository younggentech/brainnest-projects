from abc import ABC, abstractmethod
from typing import Union


class AbstractHangman(ABC):
    @abstractmethod
    def set_word(self, word_data: dict) -> None:
        """Setting a word to start a game"""
        pass

    @abstractmethod
    def check_letter(self, letter: str) -> dict:
        """Check if letter exists, returns a dict with known letters and their positions"""
        pass

    @abstractmethod
    def finish_game(self) -> Union[bool, dict]:
        """Finishes the game and returns the results of the game"""
        pass


class Hangman(AbstractHangman):
    def __init__(self, word_data: dict):
        self.__words_details = word_data

    def finish_game(self) -> Union[bool, dict]:
        pass

    def check_letter(self, letter: str) -> dict:
        pass

    def set_word(self, word_data: dict) -> None:
        pass


if __name__ == "__main__":
    h = Hangman("love")
