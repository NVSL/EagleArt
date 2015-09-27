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
from EagleUtil.EagleLibrary import *
from EagleUtil.EagleLayers import * 
import GCAM.DXFTemplate
import StringIO
import svgwrite
import GadgetronConfig as gtron


def pngToDXF(inputpng, mode, output, inputDotsPerInch, threshold, maxBoxHeight, width, layer, mirrored):
    if mode.upper() == "DXF":
        buffer = StringIO.StringIO()
        RenderLineArt(inputpng, None, inputDotsPerInch, threshold, maxBoxHeight, layer, width, output, mode,mirrored)
        output.write(buffer.getvalue())
    elif mode.upper() == "DXFSVG":
        RenderLineArt(inputpng, None, inputDotsPerInch, threshold, maxBoxHeight, layer, width, output,mode,mirrored)
    else:
        print "unknown mode = " + mode
        assert(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert PNG to DXF or SVG.  Output is based on the alpha channel of the input PNG.")
    parser.add_argument("--png", required=True, type=str, nargs=1, dest='pngFile', help="PNG File")
    parser.add_argument("--dxf", required=False, type=str, nargs=1, dest='dxfFile', help="DXF file for output")
    parser.add_argument("--svg", required=False, type=str, nargs=1, dest='svgFile', help="SVG file for output")
    parser.add_argument("--layer", required=False, type=str, nargs=1, dest='layer', help="Layer name")
    parser.add_argument("--dpi", required=True, type=float, nargs=1, dest='dpi', help="Input dpi")
    args = parser.parse_args()

    inFile = args.pngFile[0]

    if args.dxfFile is not None:
        outFile = args.dxfFile[0]
        mode = "dxf"
    else:
        outFile = args.svgFile[0]
        mode = "dxfsvg"

    inputDotsPerInch = float(args.dpi[0])

    threshold = 128

    maxBoxHeight = 0.1

    input = io.open(inFile,mode='rb')

    width = "0.1"

    if mode == "dxf":
        out = open(outFile, "wb")
        out.write(DXFTemplate.r14_header)
    elif mode == "dxfsvg":
        out = svgwrite.Drawing(outFile,
                               size=(gtron.config.DEFAULT_SVG_WIDTH,
                                     gtron.config.DEFAULT_SVG_WIDTH), 
                               viewBox=gtron.config.DEFAULT_SVG_VIEWBOX)
        

    pngToDXF(mode=mode,
             inputpng=input,
             output=out,
             inputDotsPerInch=inputDotsPerInch,
             threshold=threshold,
             maxBoxHeight=maxBoxHeight,
             width=width,
             layer="Layer0")             

    if mode == "dxf":
        out.write(DXFTemplate.r14_footer)
    elif mode == "dxfsvg":
        out.save()
