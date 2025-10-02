#!/usr/bin/env python3
import sys
import os
from subprocess import run


def cwd() -> str:
    return os.path.dirname(os.path.realpath(__file__))


def main():
    os.chdir(cwd() + "/cli")
    run(["uv", "sync"])
    run(["uv", "run", "main.py"])


if __name__ == "__main__":
    main()
else:
    sys.exit(1)
