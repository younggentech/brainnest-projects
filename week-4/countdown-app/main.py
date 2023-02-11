from time import sleep
import sys

number = input("Welcome to the countdown app\nEnter a number:\n")
while True:
    try:
        number = int(number)
        clear_console = "\b" * (len(str(number)) + 10)
        if number <= -1:
            number = input("Enter a number >= 0\n")
            continue
        seconds = int(number % 60)
        minutes = int(number / 60)
        hours = int(minutes / 60)
        print(f"the counter {number} will run for "
              f"{hours} {'hour' if hours == 1 else 'hours'}, "
              f"{minutes} {'minute' if minutes == 1 else 'minutes'}, and "
              f"{seconds} {'second' if seconds == 1 else 'seconds'}")
        while number >= 0:
            print(f"{clear_console}{hours}:{minutes}:{seconds}", end="", flush=True)
            sleep(1)
            number -= 1
            seconds = int(number % 60)
            minutes = int(number / 60)
            hours = int(minutes / 60)
        sys.exit(1)
    except ValueError as e:
        number = input("Enter only numbers ...")
