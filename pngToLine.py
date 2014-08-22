#!/usr/bin/python

# This requires pyPNG.  You can get it with pip install pyPNG
# usage pngToLine.py foo.png foo.l

import sys
import io
import math
import re
from RenderLineArt import RenderLineArt

inFile = sys.argv[1]
outFile = sys.argv[2]

inputDotsPerInch = 288.0
threshold = 128

maxBoxHeight = 13.888 # 1/72 of an inch.
maxBoxHeight = 13.888/2.0 # 1/144 of an inch.

p = re.compile('^(.*).l$')
name = p.search(outFile).group(1)

input = io.open(inFile,mode='rb')

b = RenderLineArt(input, name, inputDotsPerInch, threshold, maxBoxHeight);

out = io.open(outFile,mode='wb')
out.write(b)
