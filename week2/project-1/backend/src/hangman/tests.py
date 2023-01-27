import unittest
from . import Hangman


class HangmanTest(unittest.TestCase):
    def test_init_string(self):
        """Initialise the Hangman object with string value"""
        with self.assertRaises(TypeError):
            Hangman("Word")

    def test_json_structure(self):
        """Initialise the Hangman object with string value"""
        word_data = {"id": 3, "word": "aardvark"}
        with self.assertRaises(ValueError):
            Hangman(word_data)

    def test_init(self):
        """Try to initialize the object, put data there and get it back"""
        word_data = {
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
        self.assertEqual(Hangman(word_data).words_details, word_data)


if __name__ == "__main__":
    unittest.main()
