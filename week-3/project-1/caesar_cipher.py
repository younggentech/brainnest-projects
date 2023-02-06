import sys

capital_letters_to_index = {index: chr(counter) for index, counter in enumerate(range(65, 65 + 26))}
index_to_capital_letters = {chr(counter): index for index, counter in enumerate(range(65, 65 + 26))}

small_letters_to_index = {index: chr(counter) for index, counter in enumerate(range(97, 97 + 26))}
index_to_small_letters = {chr(counter): index for index, counter in enumerate(range(97, 97 + 26))}


def encrypt_message(key: int):
    message = input("Please enter the message:\n> ")
    result = ""
    for letter in message:
        if not letter.isalpha():
            result += letter
            continue
        if letter.islower():
            _index = index_to_small_letters.get(letter)
            result += small_letters_to_index.get((_index + key) % len(capital_letters_to_index))
        else:
            _index = index_to_capital_letters.get(letter)
            result += capital_letters_to_index.get((_index + key) % len(capital_letters_to_index))
    return message, result


def decrypt_message(key: int):
    message = input("Please enter the message:\n> ")
    result = ""
    for letter in message:
        if not letter.isalpha():
            result += letter
            continue
        if letter.islower():
            _index = index_to_small_letters.get(letter)
            result += small_letters_to_index.get((_index - key) % len(capital_letters_to_index))
        else:
            _index = index_to_capital_letters.get(letter)
            result += capital_letters_to_index.get((_index - key) % len(capital_letters_to_index))
    return message, result


while True:
    try:
        option = input("Do you want to (e)ncrypt or (d)ecrypt?\n> ")
        if option not in ("E", "e", "D", "d"):
            continue
        key = int(input("Please enter the key (0 to 25) to use.\n> "))
        message, result = encrypt_message(key=key) if option in ("E", "e") else decrypt_message(key=key)
        print(f"your message: {message} after {'encrypting' if option in ('E', 'e') else 'decrypting'}: {result}")

        while True:
            again = input("Again (Y/N)?\n> ")
            if again in ("Y", "y"):
                break
            elif again in ("N", "n"):
                print("Bye")
                sys.exit(1)
            else:
                continue

    except Exception as e:
        print(e)
