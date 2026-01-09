#!/usr/bin/env python3
'''
Keyboard-Walking Password Generator with Hashing Support

Original Author: Ronald Broberg
Edited by: Austin Scott & Anton Hibl
'''

import sys
import argparse
import itertools
import hashlib

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

def hash_ntlm(password):
    """NTLM: MD4 of UTF-16LE encoding."""
    return hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()

def hash_md5(password):
    """MD5: Standard UTF-8 encoding."""
    return hashlib.md5(password.encode('utf-8')).hexdigest().upper()

def hash_sha1(password):
    """SHA1: Standard UTF-8 encoding."""
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

def hash_sha256(password):
    """SHA256: Standard UTF-8 encoding."""
    return hashlib.sha256(password.encode('utf-8')).hexdigest().upper()

def generate_stream(segments):
    """Yields joined strings from the iterator (C-based speed)."""
    return map("".join, itertools.product(segments, repeat=4))

def main():
    parser = argparse.ArgumentParser(
        description="Keyboard-Walking Password Generator (Multi-Hash)",
        epilog="Example: python kwpg.py -m v --hash ntlm -f ntlm_hashes.txt"
    )
    parser.add_argument('-m', '--mode', choices=['v', 'h', 'b'], required=True,
                        help="Mode: (v)ertical, (h)orizontal, or (b)oth")
    parser.add_argument('-f', '--file', type=str,
                        help="Output file. If omitted, prints to STDOUT.")
    parser.add_argument('-l', '--length', type=int, default=4,
                        help="Length of horizontal walks (Default: 4)")
    parser.add_argument('--hash', choices=['none', 'ntlm', 'md5', 'sha1', 'sha256'], default='none',
                        help="Hashing algorithm to apply (Default: none)")

    parser.add_argument('--format', choices=['plain', 'pwd:hash'], default='plain',
                        help="Output format. 'plain' is just the hash (or pwd). 'pwd:hash' shows both.")
    args = parser.parse_args()
    hash_func = None
    if args.hash == 'ntlm':
        hash_func = hash_ntlm
    elif args.hash == 'md5':
        hash_func = hash_md5
    elif args.hash == 'sha1':
        hash_func = hash_sha1
    elif args.hash == 'sha256':
        hash_func = hash_sha256
    segments = []
    if args.mode in ['v', 'b']:
        segments.extend(KB_VERTICAL)
    if args.mode in ['h', 'b']:
        segments.extend(get_horizontal_walks(args.length))
    total_combos = len(segments) ** 4
    generator = generate_stream(segments)
    print_both = (args.format == 'pwd:hash')
    if args.file:
        print(f"[*] Processing {total_combos:,} combinations...")
        if hash_func:
            print(f"[*] Hashing algorithm: {args.hash.upper()}")
        try:
            with open(args.file, 'w') as f:
                chunk = []
                count = 0
                for password in generator:
                    output_line = password
                    if hash_func:
                        h = hash_func(password)
                        if print_both:
                            output_line = f"{password}:{h}"
                        else:
                            output_line = h
                    chunk.append(output_line)
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
            sys.stderr.write(f"\n[!] Error: {e}\n")
            sys.exit(1)
    else:
        for password in generator:
            output_line = password
            if hash_func:
                h = hash_func(password)
                if print_both:
                    output_line = f"{password}:{h}"
                else:
                    output_line = h
            sys.stdout.write(output_line + '\n')

if __name__ == "__main__":
    main()
