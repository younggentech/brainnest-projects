from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Union


class AbstractHangman(ABC):
    """Abstract class to design the Hangman game logic"""

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
    """Implementation of the abstract AbstractHangman class"""

    def __init__(self, words_details: dict, attempts: int):
        """Initialising object"""
        self.words_details = words_details
        self.__attempts = attempts
        self.__guessed = {
            "letters": set(),
            "letter_to_position": defaultdict(lambda: []),
        }

    def word_len(self) -> dict:
        """Function return a dict with the word's length"""
        return {"length": len(self.words_details["word"])}

    def finish_game(self) -> Union[bool, dict]:
        """Checs if the game is finished and if yes, either it is win or lose"""
        if len(self.__guessed["letters"]) == len(set(self.words_details["word"])):
            return True, {"isWin": True, "isLoss": False}
        elif self.__attempts == 0:
            return True, {"isWin": False, "isLoss": True}
        return False, {"isWin": False, "isLoss": False}

    def check_letter(self, letter: str) -> dict:
        """Checking if the letter is in the word"""
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
        """Returns current state of the game: guessed letters and their positions"""
        return self.__guessed

    @property
    def attempts(self):
        """Getter for attempts"""
        return self.__attempts

    @attempts.setter
    def set_attempts(self, attempts: int):
        """A setter for attempts, it is checking whether the attempts parameter is int or not"""
        if not isinstance(attempts, int):
            raise TypeError("attempts should be of class int")
        self.__attempts = attempts

    @property
    def words_details(self):
        """Getter for words_details"""
        return self.__words_details

    @words_details.setter
    def words_details(self, word_data: dict):
        """
        Setter for words_details, inits the game,
        critical to be a dict and to have a word key inside matching a str value
        """
        if not isinstance(word_data, dict):
            raise TypeError("word_data should be dict")
        if not word_data.get("word") or (
            word_data.get("word") and not isinstance(word_data.get("word"), str)
        ):
            raise ValueError("word key is essential, the value should be str")
        self.__words_details = word_data
