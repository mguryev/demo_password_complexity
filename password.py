#!/usr/bin/env python

import argparse
import enum
import hashlib
import itertools
import string
import tqdm


class Complexity(enum.Enum):
    NUMBERS = 'numbers'
    LETTERS = 'letters'
    ALPHANUM = 'letters_numbers'

    @staticmethod
    def choices():
        return [
            Complexity.NUMBERS.value,
            Complexity.LETTERS.value,
            Complexity.ALPHANUM.value,
        ]


class BruteForce(object):

    def __init__(self, encoded_pass: str, max_chars: int, complexity: Complexity):
        self._goal_encoded = encoded_pass
        self._max_chars = max_chars
        self._characters = _password_characters(complexity)

    def guess(self):
        result = None

        for length in range(1, self._max_chars + 1):
            print('Attempting to guess password of length %s' % length)
            _guess = self._guess_for_length(length)

            if _guess is None:
                continue

            print('Guessed password: ', _guess)
            return _guess

        print('Could not guess password')
        return result

    def _guess_for_length(self, length):
        guesses = tqdm.tqdm(self._gen_passwords(self._characters, length), desc='Checked', unit=' passwords', )

        for guess_raw, guess_encoded in guesses:
            if self._goal_encoded == guess_encoded:
                guesses.close()
                return guess_raw
        else:
            return None

    @staticmethod
    def _gen_passwords(characters, length):
        for pass_raw in itertools.product(characters, repeat=length):
            pass_raw = ''.join(pass_raw)
            pass_encoded = _encode(pass_raw)

            yield pass_raw, pass_encoded


def encode(args):
    password = input('Enter password: ')
    password = _encode(password)
    print('Encoded password:', password)


def guess(args):
    max_chars = args.length
    complexity = Complexity(args.complexity)

    encoded_pass = input('Enter encoded password: ')

    brute_forcer = BruteForce(encoded_pass, max_chars, complexity)
    brute_forcer.guess()


def estimate(args):
    max_chars = args.length
    complexity = Complexity(args.complexity)
    performance = args.performance

    password_characters = len(_password_characters(complexity))

    combinations = 0

    for length in range(1, max_chars + 1):
        combinations += pow(password_characters, length)

    guess_time = combinations / performance
    guess_time = _format_guess_time(guess_time)

    print('Number of potential passwords:', combinations)
    print('Expected passwords/s: ', performance)
    print('Approximate time to guess: ', guess_time)


def _format_guess_time(guess_time_in_seconds):
    time_parts = [
        (guess_time_in_seconds // (365 * 24 * 60 * 60), 'years'),
        (guess_time_in_seconds // (24 * 60 * 60) % 365, 'days'),
        (guess_time_in_seconds // (60 * 60) % 24 , 'hours'),
        (guess_time_in_seconds // 60 % 60, 'minutes'),
        (guess_time_in_seconds // 1 % 60, 'seconds'),
    ]

    formatted_time = ', '.join([
        '{number:.0f} {units}'.format(number=number, units=unit)
        for number, unit in time_parts
        if number > 0
    ]) or '< 1 second'

    return formatted_time


def _encode(raw):
    utf_encoded = raw.encode('ascii', 'ignore')
    return hashlib.md5(utf_encoded).hexdigest()


def _password_characters(complexity: Complexity):
    if complexity == Complexity.NUMBERS:
        return list(string.digits)
    elif complexity == Complexity.LETTERS:
        return list(string.ascii_lowercase)
    elif complexity == Complexity.ALPHANUM:
        return list(string.ascii_lowercase) + list(string.digits)


def _print_help(parser):
    def _printer_fn(args):
        parser.print_help()
        parser.exit()

    return _printer_fn


def _init_parser():
    description = 'Password complexity demonstration'

    parser = argparse.ArgumentParser(description='Password complexity demonstration')
    parser.set_defaults(func=_print_help(parser))

    subparsers = parser.add_subparsers(help='sub-command help')

    parser_encode = subparsers.add_parser('encode', help='encode password')
    parser_encode.set_defaults(func=encode)

    parser_guess = subparsers.add_parser('guess', help='guess encoded password')
    parser_guess.add_argument('complexity', choices=Complexity.choices(), help='password complexity')
    parser_guess.add_argument('--max_length', default=10, dest='length', type=int, help='maximum characters to guess')
    parser_guess.set_defaults(func=guess)

    parser_estimate = subparsers.add_parser('time_to_guess', help='estimate time to guess password')
    parser_estimate.add_argument('complexity', choices=Complexity.choices(), help='password complexity')
    parser_estimate.add_argument('length', type=int, help='maximum characters to guess')
    parser_estimate.add_argument('--performance', type=int, default=700000, help='expected passwords/s')
    parser_estimate.set_defaults(func=estimate)

    return parser


if __name__ == '__main__':
    _parser = _init_parser()
    args = _parser.parse_args()
    args.func(args)
