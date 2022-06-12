import re
import time
import sys
from gpiozero import LED


class Transmitter:
    PAUSE_TIME = 0.15

    def __init__(self):
        self.astronaut = LED(17)
        self.dot = 1 * Transmitter.PAUSE_TIME
        self.dash = 3 * Transmitter.PAUSE_TIME
        self.separator = 1 * Transmitter.PAUSE_TIME
        self.letter_separator = 3 * Transmitter.PAUSE_TIME

    def turn_on_for(self, multiplier):
        self.astronaut.on()
        time.sleep(multiplier)
        self.astronaut.off()

    def signal(self, morse_code):
        for i, char in enumerate(morse_code):
            if char == '.':
                self.turn_on_for(self.dot)
                if len(morse_code) >= i + 1 and (morse_code[i + 1] == '.' or morse_code[i + 1] == '-'):
                    time.sleep(self.separator)
            elif char == '-':
                self.turn_on_for(self.dash)
                if len(morse_code) >= i + 1 and (morse_code[i + 1] == '.' or morse_code[i + 1] == '-'):
                    time.sleep(self.separator)
            elif char == ' ':
                time.sleep(self.letter_separator)


class Morse:
    MORSE_CODE_DICT = {'A': '.-', 'B': '-...',
                       'C': '-.-.', 'D': '-..', 'E': '.',
                       'F': '..-.', 'G': '--.', 'H': '....',
                       'I': '..', 'J': '.---', 'K': '-.-',
                       'L': '.-..', 'M': '--', 'N': '-.',
                       'O': '---', 'P': '.--.', 'Q': '--.-',
                       'R': '.-.', 'S': '...', 'T': '-',
                       'U': '..-', 'V': '...-', 'W': '.--',
                       'X': '-..-', 'Y': '-.--', 'Z': '--..',
                       '1': '.----', '2': '..---', '3': '...--',
                       '4': '....-', '5': '.....', '6': '-....',
                       '7': '--...', '8': '---..', '9': '----.',
                       '0': '-----', ', ': '--..--', '.': '.-.-.-',
                       '?': '..--..', '/': '-..-.', '-': '-....-',
                       '(': '-.--.', ')': '-.--.-', ' ': ''}

    def encrypt(self, in_message):
        message = re.sub('\s+', ' ', in_message.upper())
        cipher = ''
        for letter in message:
            if letter in Morse.MORSE_CODE_DICT:
                cipher += Morse.MORSE_CODE_DICT[letter] + ' '
        return cipher


def main():
    if len(sys.argv) < 2:
        print("No message provided")
        sys.exit(-1)

    message = sys.argv[1]
    result = Morse().encrypt(message)
    print(result)
    Transmitter().signal(result)


if __name__ == '__main__':
    main()
