ALPHABET = "".join([chr(i) for i in range(33, 126)])
ALPHABET += " "
ALPHABET *= 2


def encrypt(message, key):
    en = ""
    for i in message.lower():
        position = ALPHABET.find(i)
        newposition = position + key
        if i in ALPHABET:
            en += ALPHABET[newposition]
        else:
            en += i
    return en.upper()


def decrypt(message, key):
    de = ""
    for i in message:
        position = ALPHABET.find(i)
        newposition = position - key
        if i in ALPHABET:
            de += ALPHABET[newposition]
        else:
            de += i
    return de.upper()


def main():
    while True:
        mode = input("Do you want to (e)ncrypt or (d)ecrypt?\n> ")
        if mode != "e" and mode != "d":
            print("Incorrect mode")
            continue
        key = input("Please enter the key to use.\n> ")
        if not key.isnumeric():
            print("Incorrect key")
            continue

        match mode:
            case "e":
                msg = input("Enter the message to encrypt.\n> ")
                print(encrypt(msg, int(key)))
            case "d":
                msg = input("Enter the message to decrypt.\n> ")
                print(decrypt(msg, int(key)))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Have a nice day")
