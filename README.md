# pass-gen

Generate random passwords and passphrases from the command line — zero-dependency Python CLI using the `secrets` module, so every output is cryptographically random.

## Install

Requires Python 3.8+. No dependencies to install.

```bash
git clone https://github.com/heyzcx/pass-gen.git
cd pass-gen
```

## Usage

```bash
python3 pass_gen.py                  # one 16-character password
python3 pass_gen.py -l 24 -n 5       # five 24-character passwords
python3 pass_gen.py --no-symbols     # letters and digits only
python3 pass_gen.py --no-digits --no-upper  # lowercase letters only
python3 pass_gen.py --passphrase -w 5        # five-word passphrase
python3 pass_gen.py --passphrase --separator -  # words joined with dashes
python3 pass_gen.py --entropy        # also print estimated entropy in bits
```

## Options

| Option | Description | Default |
| --- | --- | --- |
| `-l, --length` | Password length (min 4) | 16 |
| `-n, --count` | How many to generate | 1 |
| `--no-symbols` | Exclude punctuation | off |
| `--no-digits` | Exclude digits | off |
| `--no-upper` | Exclude uppercase letters | off |
| `--passphrase` | Generate a word passphrase instead | off |
| `-w, --words` | Words in a passphrase (min 2) | 4 |
| `--separator` | Word separator for passphrases | space |
| `--entropy` | Print estimated entropy in bits | off |

## Example

```bash
$ python3 pass_gen.py -l 20 --entropy
SYF:;qU~%.Y,A+~Mq=gL  (~131 bits)

$ python3 pass_gen.py --passphrase -w 5 --separator -
sable-quartz-haven-meadow-willow
```

## Tests

```bash
python3 test_pass_gen.py
```
