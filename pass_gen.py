#!/usr/bin/env python3
"""pass-gen: generate random passwords and passphrases.

Zero-dependency Python CLI. Uses the `secrets` module so generated
passwords are cryptographically random.

Usage:
    python3 pass_gen.py                  # one 16-char password
    python3 pass_gen.py -l 24 -n 5       # five 24-char passwords
    python3 pass_gen.py --no-symbols     # letters and digits only
    python3 pass_gen.py --passphrase -w 5  # five-word passphrase
    python3 pass_gen.py --passphrase --separator -
"""

import argparse
import math
import secrets
import string
import sys

# Small built-in word list for passphrases (common short English words).
WORDS = [
    "apple", "river", "stone", "cloud", "brave", "quiet", "solar", "meadow",
    "forest", "ocean", "mount", "valley", "bridge", "candle", "daniel",
    "eagle", "falcon", "garden", "harbor", "island", "jungle", "kitten",
    "lemon", "mango", "north", "olive", "panda", "queen", "rocket",
    "silver", "tiger", "urban", "velvet", "walnut", "yellow", "zebra",
    "amber", "basin", "cedar", "delta", "ember", "frost", "globe",
    "hazel", "ivory", "jade", "koala", "linen", "maple", "noble",
    "orbit", "pearl", "quilt", "raven", "sable", "topaz", "unity",
    "vivid", "whale", "xenon", "yonder", "zephyr", "acorn", "beacon",
    "cobalt", "dune", "elm", "fern", "grove", "honey", "ink", "jasper",
    "kelp", "lagoon", "mist", "nova", "onyx", "plum", "quartz",
    "ridge", "sage", "thorn", "umbra", "vine", "willow", "yacht",
    "alto", "birch", "coral", "dusk", "echo", "flint", "granite",
    "heron", "iris", "juniper", "karma", "lunar", "marble", "nylon",
    "opal", "prairie", "robin", "sierra", "tundra", "ulna", "vista",
    "wren", "yew", "zinc", "atlas", "breeze", "cinder", "drift",
    "elmwood", "fable", "garnet", "haven", "indra", "jovial", "keepsake",
]


def entropy_bits(pool_size: int, length: int) -> float:
    """Estimate entropy in bits for a random string of `length` chars
    drawn uniformly from a pool of `pool_size` characters."""
    if pool_size <= 1 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def generate_password(length: int, use_symbols: bool,
                      use_digits: bool = True, use_upper: bool = True) -> str:
    """Generate one random password of the given length."""
    pool = string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digits:
        pool += string.digits
    if use_symbols:
        pool += string.punctuation
    return "".join(secrets.choice(pool) for _ in range(length))


def generate_passphrase(word_count: int, separator: str) -> str:
    """Generate a passphrase of `word_count` random words."""
    return separator.join(secrets.choice(WORDS) for _ in range(word_count))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate random passwords and passphrases.")
    parser.add_argument("-l", "--length", type=int, default=16,
                        help="password length (default: 16)")
    parser.add_argument("-n", "--count", type=int, default=1,
                        help="how many to generate (default: 1)")
    parser.add_argument("--no-symbols", action="store_true",
                        help="exclude punctuation symbols")
    parser.add_argument("--no-digits", action="store_true",
                        help="exclude digits")
    parser.add_argument("--no-upper", action="store_true",
                        help="exclude uppercase letters")
    parser.add_argument("--passphrase", action="store_true",
                        help="generate a word passphrase instead of a password")
    parser.add_argument("-w", "--words", type=int, default=4,
                        help="words in a passphrase (default: 4)")
    parser.add_argument("--separator", default=" ",
                        help="word separator for passphrases (default: space)")
    parser.add_argument("--entropy", action="store_true",
                        help="also print estimated entropy in bits")
    args = parser.parse_args(argv)

    if args.length < 4:
        print("error: length must be at least 4", file=sys.stderr)
        return 2
    if args.count < 1:
        print("error: count must be at least 1", file=sys.stderr)
        return 2
    if args.words < 2:
        print("error: passphrase needs at least 2 words", file=sys.stderr)
        return 2

    for _ in range(args.count):
        if args.passphrase:
            value = generate_passphrase(args.words, args.separator)
            bits = args.words * math.log2(len(WORDS))
        else:
            value = generate_password(args.length, not args.no_symbols,
                                      not args.no_digits, not args.no_upper)
            pool = len(string.ascii_lowercase)
            pool += 0 if args.no_upper else len(string.ascii_uppercase)
            pool += 0 if args.no_digits else len(string.digits)
            pool += 0 if args.no_symbols else len(string.punctuation)
            bits = entropy_bits(pool, args.length)
        if args.entropy:
            print(f"{value}  (~{bits:.0f} bits)")
        else:
            print(value)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
