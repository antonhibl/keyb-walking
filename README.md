# Keyboard Walk Generator

A high-performance Python tool for generating password wordlists based on keyboard walking patterns (e.g., `1qaz`, `xsw2`, `qwer`). This tool is optimized for speed using buffered I/O and C-based iterators to handle massive lists (33M+ combinations) efficiently.

## Files

* **`kbwalk.py`**: The standard generator.
* **`kbwalk_ntlm.py`**: The generator that supports NTLM hashing to skip the piping overhead.
* **`LICENSE`**: BSD-2/Clause License.

## Features

* **High Performance:** Uses `itertools` and buffered writing to generate ~33 million lines in seconds.
* **Modes:** Supports Vertical (`1qaz`), Horizontal (`qwerty`), or Both.
* **NTLM Support:** Can output raw NTLM hashes or `password:hash` format directly.
* **No Dependencies:** Runs on standard Python 3 libraries.

## Usage

### 1. Standard Generation (`kbwalk.py`)

Generate the classic 33 million vertical keyboard walk list:

```bash
python3 kbwalk.py -m v -f wordlist.txt

```

Generate a horizontal walk list (length 4) and print to STDOUT (for piping):

```bash
python3 kbwalk.py -m h -l 4

```

**Arguments:**

* `-m`: Mode (`v` = vertical, `h` = horizontal, `b` = both).
* `-f`: Output filename (optional, prints to terminal if omitted).
* `-l`: Length of horizontal walk (default: 4).

### 2. NTLM Hashing (`kbwalk_ntlm.py`)

Generate a list of NTLM hashes directly (useful for rainbow tables):

```bash
python3 kbwalk_ntlm.py -m v --hash ntlm -f ntlm_hashes.txt

```

Generate in `password:hash` format for verification:

```bash
python3 kbwalk_ntlm.py -m v --hash ntlm --format pwd:hash -f combos.txt

```

## Disclaimer

This tool is designed for security research, authorized penetration testing, and educational purposes only. The authors are not responsible for misuse.

Original Author: Ronald Broberg
<br>
Edited by: Austin Scott & Anton Hibl
