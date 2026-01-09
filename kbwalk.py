#!/usr/bin/env python3
'''
Keyboard-Walking Password Generator
Includes optional tqdm support and NTLM/Multi-hashing.

Original Author: Ronald Broberg
Edited by: Austin Scott & Anton Hibl
'''
import sys
import argparse
import itertools
import hashlib

try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False

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
    if length < 1: length = 4
    if length > len(KEYBOARD_STRING): length = len(KEYBOARD_STRING)
    return [KEYBOARD_STRING[i : i + length] for i in range(len(KEYBOARD_STRING) - length + 1)]

def hash_ntlm(password):
    return hashlib.new('md4', password.encode('utf-16le')).hexdigest().upper()

def hash_md5(password):
    return hashlib.md5(password.encode('utf-8')).hexdigest().upper()

def hash_sha1(password):
    return hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

def hash_sha256(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest().upper()

def generate_stream(segments):
    return map("".join, itertools.product(segments, repeat=4))

def main():
    parser = argparse.ArgumentParser(
        description="Keyboard-Walking Password Generator",
        epilog="Example: python kbwalk.py -m v --hash ntlm -f ntlm.txt"
    )
    parser.add_argument('-m', '--mode', choices=['v', 'h', 'b'], required=True,
                        help="Mode: (v)ertical, (h)orizontal, or (b)oth")
    parser.add_argument('-f', '--file', type=str,
                        help="Output file. If omitted, prints to STDOUT.")
    parser.add_argument('-l', '--length', type=int, default=4,
                        help="Length of horizontal walks (Default: 4)")

    parser.add_argument('--hash', choices=['none', 'ntlm', 'md5', 'sha1', 'sha256'], default='none',
                        help="Hashing algorithm (Default: none)")

    parser.add_argument('--format', choices=['plain', 'pwd:hash'], default='plain',
                        help="Output format.")
    args = parser.parse_args()
    hash_func = None
    if args.hash == 'ntlm': hash_func = hash_ntlm
    elif args.hash == 'md5': hash_func = hash_md5
    elif args.hash == 'sha1': hash_func = hash_sha1
    elif args.hash == 'sha256': hash_func = hash_sha256
    segments = []
    if args.mode in ['v', 'b']:
        segments.extend(KB_VERTICAL)
    if args.mode in ['h', 'b']:
        segments.extend(get_horizontal_walks(args.length))
    total_combos = len(segments) ** 4
    generator = generate_stream(segments)
    print_both = (args.format == 'pwd:hash')
    if args.file:
        print(f"[*] Mode: {args.mode.upper()} | Base Segments: {len(segments)}")
        print(f"[*] Hashing: {args.hash.upper()} | Output: {args.file}")
        print(f"[*] Generating {total_combos:,} combinations...")
        try:
            with open(args.file, 'w') as f:
                chunk = []
                count = 0
                if TQDM_AVAILABLE:
                    pbar = tqdm(total=total_combos, unit="pw", unit_scale=True, smoothing=0.1)
                else:
                    pbar = None
                    print("[*] tqdm not found. Using simple counter.")
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
                        if pbar:
                            pbar.update(len(chunk))
                        else:
                            count += len(chunk)
                            sys.stdout.write(f"\rProgress: {count:,} / {total_combos:,}")
                            sys.stdout.flush()
                        chunk = []
                if chunk:
                    f.write('\n'.join(chunk) + '\n')
                    if pbar: pbar.update(len(chunk))
                if pbar: pbar.close()
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

# BRIDGE FOR COMPLEXITY SCANNER (https://github.com/antonhibl/occam)
class Solution:
    def run_analysis_entry(self, data):
        if isinstance(data, list): segments = [str(x) for x in data]
        elif isinstance(data, int): segments = [str(i) for i in range(data)]
        else: segments = ['1qaz']

        iterator = generate_stream(segments)
        for _ in iterator: pass
