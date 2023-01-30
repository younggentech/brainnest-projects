import unittest
from . import Hangman

CORRECT_DATA = {
    "id": 3,
    "word": "aardvark",
    "definitions": [
        {
            "word": "aardvark",
            "phonetic": "/ˈɑːd.vɑːk/",
            "phonetics": [
                {"text": "/ˈɑːd.vɑːk/", "audio": ""},
                {
                    "text": "/ˈɑɹd.vɑɹk/",
                    "audio": "https://api.dictionaryapi.dev/media/pronunciations/en/aardvark-us.mp3",
                    "sourceUrl": "https://commons.wikimedia.org/w/index.php?curid=50309155",
                    "license": {
                        "name": "BY-SA 4.0",
                        "url": "https://creativecommons.org/licenses/by-sa/4.0",
                    },
                },
            ],
            "meanings": [
                {
                    "partOfSpeech": "noun",
                    "definitions": [
                        {
                            "definition": "The nocturnal, insectivorous, burrowing, mammal Orycteropus afer, of the order Tubulidentata, somewhat resembling a pig, common in some parts of sub-Saharan Africa.",
                            "synonyms": [],
                            "antonyms": [],
                            "example": "The aardvark burrows in the ground and feeds mostly on termites, which it catches with its long, slimy tongue.",
                        },
                        {
                            "definition": "A silly or credulous person who is prone to mistakes or blunders.",
                            "synonyms": [],
                            "antonyms": [],
                            "example": "I walked into the wrong bathroom like a total aardvark.",
                        },
                    ],
                    "synonyms": [
                        "African anteater",
                        "ant bear",
                        "ant-bear",
                        "antbear",
                        "anteater",
                        "earth pig",
                        "fool",
                    ],
                    "antonyms": [],
                }
            ],
            "license": {
                "name": "CC BY-SA 3.0",
                "url": "https://creativecommons.org/licenses/by-sa/3.0",
            },
            "sourceUrls": ["https://en.wiktionary.org/wiki/aardvark"],
        }
    ],
}


class HangmanTest(unittest.TestCase):
    def test_init_string(self):
        """Initialise the Hangman object with string value"""
        with self.assertRaises(TypeError):
            Hangman("Word")

    def test_init(self):
        """Testing initiating of Hangman object"""
        # word aardvark
        """Try to initialize the object, put data there and get it back"""
        hgm = Hangman(CORRECT_DATA, 6)
        self.assertEqual(hgm.words_details, CORRECT_DATA)
        print(hgm.attempts)
        self.assertEqual(hgm.attempts, 6)

    def test_check_letters(self):
        """Trying to play a game, winning with 1 mistake"""
        hgm = Hangman(CORRECT_DATA, 6)

        self.assertEqual(
            hgm.check_letter("a"),
            {
                "letter": "a",
                "positions": [0, 1, 5],
                "attemptsLeft": 6,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("p"),
            {
                "letter": "p",
                "positions": [],
                "attemptsLeft": 5,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("r"),
            {
                "letter": "r",
                "positions": [2, 6],
                "attemptsLeft": 5,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("d"),
            {
                "letter": "d",
                "positions": [3],
                "attemptsLeft": 5,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("k"),
            {
                "letter": "k",
                "positions": [7],
                "attemptsLeft": 5,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("v"),
            {
                "letter": "v",
                "positions": [4],
                "attemptsLeft": 5,
                "isWin": True,
                "isLoss": False,
            },
        )

    def test_check_loose(self):
        """Trying to play a game, loosing"""
        hgm = Hangman(CORRECT_DATA, 6)

        self.assertEqual(
            hgm.check_letter("z"),
            {
                "letter": "z",
                "positions": [],
                "attemptsLeft": 5,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("x"),
            {
                "letter": "x",
                "positions": [],
                "attemptsLeft": 4,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("y"),
            {
                "letter": "y",
                "positions": [],
                "attemptsLeft": 3,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("m"),
            {
                "letter": "m",
                "positions": [],
                "attemptsLeft": 2,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("q"),
            {
                "letter": "q",
                "positions": [],
                "attemptsLeft": 1,
                "isWin": False,
                "isLoss": False,
            },
        )
        self.assertEqual(
            hgm.check_letter("w"),
            {
                "letter": "w",
                "positions": [],
                "attemptsLeft": 0,
                "isWin": False,
                "isLoss": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
