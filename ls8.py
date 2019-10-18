#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

# cpu = CPU()

# cpu.load()
# cpu.run()

def main(argv):

    cpu = CPU()

    cpu.load(argv)
    cpu.run()
    

if len(sys.argv) != 2:
    print("usage: simple.py <filename>", file=sys.stderr)
    sys.exit(1)

    
main(sys.argv[1])