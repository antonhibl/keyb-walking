#!/usr/bin/env python3
'''
Keyboard-Walking Password Generator (Optimized)
Modernized for Python 3 with buffered I/O and itertools.

Original Author: Ronald Broberg
Edited by: Austin Scott & Anton Hibl
'''

import sys
import argparse
import itertools

BUFFER_SIZE = 20000

KEYBOARD_STRING = (
    'qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./`1234567890-=ZXCVBNM<>?ASDFGHJKL:"QWERTYUIOP{}~!@#$%^&*()_+'
)

KB_VERTICAL = [
    '1qaz', '2wsx', '3edc', '4rfv', '5tgb', '6yhn', '7ujm', '8ik,', '9ol.', '0p;/',
    '!QAZ', '@WSX', '#EDC', '$RFV', '%TGB', '^YHN', '&UJM', '*IK<', '(OL>', ')P:?',
    'zaq1', 'xsw2', 'cde3', 'vfr4', 'bgt5', 'nhy6', 'mju7', ',ki8', '.lo9', '/;p0',
    'ZAQ!', 'XSW@', 'CDE#', 'VFR$', 'BGT%', 'NHY^', 'MJU&', '<KI*', '>LO(', '?:P)',
    '4esz', '5rdx', '6tfc', '7ygv', '8uhb', '9ijn', '0okm', '-pl,', '=[;.',
    '$ESZ', '%RDX', '^TFC', '&YGV', '*UHB', '(IJN', ')OKM', '_PL<', '+{:>',
    'zse4', 'xdr5', 'cft6', 'vgy7', 'bhu8', 'nji9', 'mko0', ',lp-', '.;[=',
    'ZSE$', 'XDR%', 'CFT^', 'VGY&', 'BHU*', 'NJI(', 'MKO)', '<LP_', '>:{+',
]

def get_horizontal_walks(length):
    """Generates horizontal walks using a fast sliding window."""
    if length < 1: length = 4
    if length > len(KEYBOARD_STRING): length = len(KEYBOARD_STRING)
    return [KEYBOARD_STRING[i : i + length] for i in range(len(KEYBOARD_STRING) - length + 1)]

def generate_stream(segments):
    """Yields joined strings from the iterator."""
    return map("".join, itertools.product(segments, repeat=4))

def main():
    parser = argparse.ArgumentParser(
        description="Keyboard-Walking Password Generator (Optimized)",
        epilog="Example: python kwpg.py -m v -f wordlist.txt"
    )

    parser.add_argument('-m', '--mode', choices=['v', 'h', 'b'], required=True,
                        help="Mode: (v)ertical, (h)orizontal, or (b)oth")
    parser.add_argument('-f', '--file', type=str,
                        help="Output file (e.g., wordlist.txt). If omitted, prints to STDOUT.")
    parser.add_argument('-l', '--length', type=int, default=4,
                        help="Length of horizontal walks (Default: 4)")

    args = parser.parse_args()
    segments = []

    if args.mode in ['v', 'b']:
        segments.extend(KB_VERTICAL)

    if args.mode in ['h', 'b']:
        segments.extend(get_horizontal_walks(args.length))

    total_combos = len(segments) ** 4
    generator = generate_stream(segments)

    if args.file:
        print(f"[*] Generating {total_combos:,} combinations using {len(segments)} base segments...")
        print(f"[*] Writing to '{args.file}'...")
        try:
            with open(args.file, 'w') as f:
                chunk = []
                count = 0
                for word in generator:
                    chunk.append(word)
                    if len(chunk) >= BUFFER_SIZE:
                        f.write('\n'.join(chunk) + '\n')
                        count += len(chunk)
                        chunk = []
                        print(f"\rProgress: {count:,} / {total_combos:,}", end='', flush=True)
                if chunk:
                    f.write('\n'.join(chunk) + '\n')
                    count += len(chunk)
            print(f"\n[+] Done! Output saved to {args.file}")
        except IOError as e:
            sys.stderr.write(f"\n[!] Error writing file: {e}\n")
            sys.exit(1)
    else:
        for word in generator:
            sys.stdout.write(word + '\n')

if __name__ == "__main__":
    main()
