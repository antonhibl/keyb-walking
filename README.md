
# Keyboard Walk Generator

A high-performance Python tool for generating password wordlists based on keyboard walking patterns (e.g., `1qaz`, `xsw2`, `qwer`). This tool is optimized for speed using buffered I/O and C-based iterators to handle massive lists (33M+ combinations) efficiently.

## Files

* **`kbwalk.py`**: The all-in-one generator with built-in hashing support.
* **`LICENSE`**: BSD-2-Clause License.
* `README.md`: This file.

## Features

* **High Performance:** Uses `itertools` and buffered writing to generate ~33 million lines in seconds.
* **Modes:** Supports Vertical (`1qaz`), Horizontal (`qwerty`), or Both.
* **Multi-Hashing:** Can generate **NTLM**, **MD5**, **SHA1**, or **SHA256** hashes directly to skip piping overhead.
* **Flexible Output:** Supports raw hash lists or `password:hash` format.
* **No Dependencies:** Runs on standard Python 3 libraries.

## Usage

### 1. Standard Wordlist Generation

Generate the classic 33 million vertical keyboard walk list:

```bash
python3 kbwalk.py -m v -f wordlist.txt

```

Generate a horizontal walk list (length 4) and print to STDOUT (for piping):

```bash
python3 kbwalk.py -m h -l 4

```

### 2. Hash Generation (Rainbow Tables)

Generate a list of **NTLM** hashes directly (useful for Windows auditing):

```bash
python3 kbwalk.py -m v --hash ntlm -f ntlm_hashes.txt

```

Generate **MD5** hashes:

```bash
python3 kbwalk.py -m v --hash md5 -f md5_hashes.txt

```

Generate in `password:hash` format for verification:

```bash
python3 kbwalk.py -m v --hash sha1 --format pwd:hash -f combos.txt

```

### Arguments

* `-m`, `--mode`: Pattern mode (`v` = vertical, `h` = horizontal, `b` = both).
* `-f`, `--file`: Output filename (optional, prints to STDOUT if omitted).
* `-l`, `--length`: Length of horizontal walk segments (default: 4).
* `--hash`: Hashing algorithm to apply (`ntlm`, `md5`, `sha1`, `sha256`, `none`).
* `--format`: Output format (`plain` = hash only, `pwd:hash` = password and hash).

## Disclaimer

This tool is designed for security research, authorized penetration testing, and educational purposes only. The authors are not responsible for misuse.

**Original Author:** Ronald Broberg
<br>
**Edited by:** Austin Scott & Anton Hibl
