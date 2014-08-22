#!/usr/bin/python

# usage lCat.py 1.l 2.l ... n.l > all.l

import io
import sys

sys.stdout.write("*PADS-LIBRARY-LINE-ITEMS-V9*\r\n")

for name in sys.argv[1:]:
    f = io.open(name,"rb");
    lines = f.readlines()
    sys.stdout.write("".join(lines[1:-1]))

sys.stdout.write("*END*\r\n")
