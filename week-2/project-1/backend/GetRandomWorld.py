import json
import logging
import multiprocessing
import time
import requests

logging.basicConfig(
    format="%(asctime)s-%(levelname)s - %(message)s",
    level=logging.INFO,
    datefmt="%d.%m.%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(filename=f"words.log"),
        logging.StreamHandler(),
    ],
)


def get_random_words() -> str:
    data = requests.get(
        "https://svnweb.freebsd.org/csrg/share/dict/words?revision=61569&view=co",
        headers={"User-Agent": "lasdjakljk"},
    )
    return data.text.split()


def check_insulting(word: str) -> dict:
    url = "https://community-purgomalum.p.rapidapi.com/json"

    querystring = {"text": word}

    return False


def get_full_definition(word: str) -> list:
    try:
        endpoint = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        data = requests.get(endpoint)
        return data.json()
    except Exception as e:
        logging.error(f"{data.text}")
        time.sleep(20)
        logging.info("sleeping")
        return []


def write_words(words, letter):
    _res = {"res": []}
    try:
        for word_num in range(len(words)):
            word = words[word_num]
            if not word.lower().startswith(letter):
                logging.info(f"{word} skipped, letter {letter}")
                continue
            _def = get_full_definition(word)
            if len(_def) == 0 or (
                len(_def) > 0
                and isinstance(_def, dict)
                and _def.get("title") == "No Definitions Found"
            ):
                continue

            if (
                "*" not in check_insulting(word)
                and len(_def) >= 1
                and len(word) > 3
                and word.lower().startswith(letter)
            ):
                _res["res"].append({"id": word_num, "word": word, "definitions": _def})
                with open(f"{letter}.json", "w") as f:
                    f.write(json.dumps(_res))
                logging.info(f"{word} added")
            else:
                logging.info(f"{word} skipped")
    finally:
        logging.info(f"{letter} done")
    time.sleep(0.5)


if __name__ == "__main__":
    _words = get_random_words()
    processes = [
        multiprocessing.Process(target=write_words, args=(_words, chr(letter)))
        for letter in range(97, 123)
    ]
    _c = 0
    for process in processes:
        logging.info(f"Process {_c} started")
        process.start()
        _c += 1

    for process in processes:
        process.join()
