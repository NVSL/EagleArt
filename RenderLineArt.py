import png
import StringIO
import time
from lxml import etree as ET
import math

def RenderLineArt(f, name, inputDotsPerInch, threshold, maxBoxHeight, layer, lineWidth, state, mode="BRD"):

#    root = ET.Element("package", name=name)

    rowMultiplier = 1
    xPixelSize = (1.0/inputDotsPerInch) * 25.4 # file format requires mm
    yPixelSize = (1.0/inputDotsPerInch) * 25.4 # file format requires mm
#    if yPixelSize > maxBoxHeight:
#        rowMultiplier = int(math.ceil(yPixelSize/maxBoxHeight))
#        yPixelSize = yPixelSize/rowMultiplier

    r = png.Reader(f)
    (width, height, pixels, crap) = r.asRGBA()

    b = StringIO.StringIO()

    c = 0
    y = 0

    for row in pixels:
        startx = 0
        x = 0
        inBlack = False
        row = list(row)+[255,255,255,255] # This ensures that the we don't loose the right edge
        for p in row[::4]:

            if p < threshold:
                if not inBlack:
                    startx = x;
                inBlack = True;
            else:
                if inBlack:
                    for i in range(0, rowMultiplier):
                        top =     y*rowMultiplier*yPixelSize + i*yPixelSize
                        bottom =  top + yPixelSize
                        left =    startx * xPixelSize
                        right =   (x-1)*xPixelSize + xPixelSize

                        if mode == "dxf":
                            pass
                        elif mode == "svg":
                            print "start: "+  repr((left,top))
                            print "size: "+ repr((right-left,bottom-top))
                            state.add(state.rect((left,top),(right-left,bottom-top), stroke="black", stroke_width="0.01mm"))
                        elif mode == "brd":
                            poly = ET.SubElement(state, "polygon", layer=layer, width=lineWidth)
                            ET.SubElement(poly, "vertex", x=str(left), y=str(top))
                            ET.SubElement(poly, "vertex", x=str(right), y=str(top))
                            ET.SubElement(poly, "vertex", x=str(right), y=str(bottom))
                            ET.SubElement(poly, "vertex", x=str(left), y=str(bottom))
                            ET.SubElement(poly, "vertex", x=str(left), y=str(top))

                inBlack = False

            x = x + 1;
        y = y - 1;

