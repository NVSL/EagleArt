#!/usr/bin/python

# This requires pyPNG.  You can get it with pip install pyPNG
# usage pngToLine.py foo.png foo.l

import sys
import io
import math
import re
from RenderLineArt import RenderLineArt
import argparse
from lxml import etree as ET
from EagleLibrary import *
from EagleLayers import * 

parser = argparse.ArgumentParser(description="Tool for auto-generating packages for breakout boards")
parser.add_argument("--png", required=True, type=str, nargs=1, dest='pngFile', help="PNG File")
parser.add_argument("--lbr", required=True, type=str, nargs=1, dest='lbrFile', help="Eagle Library to add the art to")
parser.add_argument("--package", required=False, type=str, nargs=1, dest='package', help="Package name")
parser.add_argument("--force", action="store_true", help="Replace current package")
parser.add_argument("--width", required=False, type=str, nargs=1, dest='width', help="Line width in mm")
parser.add_argument("--layer", required=False, type=str, nargs=1, dest='layer', help="Layer name")
parser.add_argument("--dpi", required=False, type=float, nargs=1, dest='dpi', help="Input dpi")
args = parser.parse_args()

inFile = args.pngFile[0]
outFile = args.lbrFile[0]

if args.dpi is None:
    inputDotsPerInch = 288.0
else:
    inputDotsPerInch = float(args.dpi[0])

threshold = 128

maxBoxHeight = 0.1

if args.package is None:
    f = inFile.split("/")[-1]
    name = f.replace(".png","").replace(".PNG","")
else:
    name = args.package[0]

input = io.open(inFile,mode='rb')

lbr = EagleLibrary(args.lbrFile[0])
layers = EagleLayers(lbr.getLayers())

if args.layer is None:
    layer = "tPlace"
else:
    layer = args.layer[0]

if args.width is None:
    width = "0.1"
else:
    width = args.width[0]

package = ET.Element("package", name=name)
RenderLineArt(input, name.upper(), inputDotsPerInch, threshold, maxBoxHeight, str(layers.nameToNumber(layer)), width, mode="brd", state=package)

try:
    lbr.addPackage(package)
except EagleError as e:
    if args.force:
        lbr.deletePackage(package.get("name"))
        lbr.addPackage(package)
    else:
        raise e

lbr.write(args.lbrFile[0])

#out = io.open(outFile,mode='wb')
#out.write(b)
