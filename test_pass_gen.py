#!/usr/bin/env python3
"""Smoke tests for pass_gen.py — run with: python3 test_pass_gen.py"""

import subprocess
import sys

FAILURES = []


def check(name, condition):
    print(("PASS" if condition else "FAIL"), "-", name)
    if not condition:
        FAILURES.append(name)


def run(*args):
    result = subprocess.run([sys.executable, "pass_gen.py", *args],
                            capture_output=True, text=True)
    return result


r = run()
check("default password is 16 chars", r.returncode == 0 and len(r.stdout.strip()) == 16)

r = run("-l", "24", "-n", "3")
lines = r.stdout.strip().splitlines()
check("3 passwords of 24 chars", r.returncode == 0 and len(lines) == 3
      and all(len(x) == 24 for x in lines))
check("passwords differ", len(set(lines)) == 3)

r = run("--no-symbols", "-l", "32")
import string
check("no-symbols has no punctuation",
      r.returncode == 0 and not any(c in string.punctuation for c in r.stdout.strip()))

r = run("--passphrase", "-w", "5")
check("passphrase has 5 words",
      r.returncode == 0 and len(r.stdout.strip().split()) == 5)

r = run("--passphrase", "-w", "4", "--separator", "-")
check("passphrase separator works",
      r.returncode == 0 and r.stdout.strip().count("-") == 3)

r = run("--entropy")
check("entropy flag prints bits",
      r.returncode == 0 and "bits" in r.stdout)

r = run("-l", "2")
check("length < 4 rejected", r.returncode == 2)

print()
if FAILURES:
    print(f"{len(FAILURES)} test(s) failed")
    sys.exit(1)
print("all tests passed")
