from abc import ABC, abstractmethod
from collections import defaultdict
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

    @abstractmethod
    def word_len(self) -> dict:
        """Returns tha length of the world"""
        pass


class Hangman(AbstractHangman):
    def __init__(self, words_details: dict, attempts: int):
        self.words_details = words_details
        self.__attempts = attempts
        self.__guessed = {
            "letters": set(),
            "letter_to_position": defaultdict(lambda: []),
        }

    def word_len(self) -> dict:
        return {"length": len(self.words_details["word"])}

    def finish_game(self) -> Union[bool, dict]:
        if len(self.__guessed["letters"]) == len(set(self.words_details["word"])):
            return True, {"isWin": True, "isLoss": False}
        elif self.__attempts == 0:
            return True, {"isWin": False, "isLoss": True}
        return False, {"isWin": False, "isLoss": False}

    def check_letter(self, letter: str) -> dict:
        if letter in self.words_details["word"]:
            self.__guessed["letters"].add(letter)
            self.__guessed["letter_to_position"][letter] = [
                pos
                for pos, char in enumerate(self.words_details["word"])
                if char == letter
            ]
        else:
            self.__attempts -= 1
        resp = {
            "letter": letter,
            "positions": self.__guessed["letter_to_position"][letter],
            "attemptsLeft": self.__attempts,
        }
        return resp | self.finish_game()[1]

    def get_current_letter_state(self) -> dict:
        return self.__guessed

    @property
    def attempts(self):
        return self.__attempts

    @attempts.setter
    def set_attempts(self, attempts: int):
        if not isinstance(attempts, int):
            raise TypeError("attempts should be of class int")
        self.__attempts = attempts

    @property
    def words_details(self):
        return self.__words_details

    @words_details.setter
    def words_details(self, word_data: dict):
        if not isinstance(word_data, dict):
            raise TypeError("word_data should be dict")
        if not word_data.get("word") or (
            word_data.get("word") and not isinstance(word_data.get("word"), str)
        ):
            raise ValueError("word key is essential, the value should be str")
        self.__words_details = word_data


if __name__ == "__main__":
    h = Hangman({"word": "hello"}, 6)
    print(h.check_letter("p"))
    print(h.check_letter("e"))
    print(h.get_current_letter_state())
