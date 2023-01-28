from abc import ABC, abstractmethod
from typing import Union


class AbstractHangman(ABC):
    @abstractmethod
    def check_letter(self, letter: str) -> dict:
        """Check if letter exists, returns a dict with known letters and their positions"""
        pass

    @abstractmethod
    def finish_game(self) -> Union[bool, dict]:
        """Finishes the game and returns the results of the game"""
        pass


class Hangman(AbstractHangman):
    def __init__(self, words_details):
        self.words_details = words_details

    def finish_game(self) -> Union[bool, dict]:
        pass

    def check_letter(self, letter: str) -> dict:
        pass

    @property
    def words_details(self):
        return self.__words_details

    @words_details.setter
    def words_details(self, word_data: dict):
        if not isinstance(word_data, dict):
            raise TypeError("word_data should be dict")
        if not word_data.get("definitions"):
            raise ValueError("definitions should exist")
        self.__words_details = word_data


if __name__ == "__main__":
    h = Hangman("ads")
    print(h.words_details)
