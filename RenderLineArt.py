import png
import StringIO
import time
from lxml import etree as ET
import math
import GCAM.DXFUtil

def RenderLineArt(f, name, inputDotsPerInch, threshold, maxBoxHeight, layer, lineWidth, state, mode,mirrored):

#    root = ET.Element("package", name=name)

    rowMultiplier = 1
    xPixelSize = (1.0/inputDotsPerInch) * 25.4 # We use mm
    yPixelSize = (1.0/inputDotsPerInch) * 25.4 # we use mm
#    if yPixelSize > maxBoxHeight:
#        rowMultiplier = int(math.ceil(yPixelSize/maxBoxHeight))
#        yPixelSize = yPixelSize/rowMultiplier

    r = png.Reader(f)
    (width, height, pixels, crap) = r.asRGBA()

    xOffset = -(width*xPixelSize)/2.0
    yOffset = (height*yPixelSize)/2.0

    b = StringIO.StringIO()

    c = 0
    y = 0
    handle = 255
    for row in pixels:
        startx = 0
        x = 0
        inBlack = False
        row = list(row)+[255,255,255,255] # This ensures that the we don't loose the right edge
        for p in row[3::4]:

            if p > threshold:
                if not inBlack:
                    startx = x;
                inBlack = True;
            else:
                if inBlack:
                    for i in range(0, rowMultiplier):
                        top =     (y*rowMultiplier*yPixelSize + i*yPixelSize) + yOffset
                        bottom =  top + yPixelSize
                        left =    startx * xPixelSize + xOffset
                        right =   (x-1)*xPixelSize + xPixelSize + xOffset

                        if mirrored:
                            left = -left
                            right = -right

                        t = top
                        top = -bottom
                        bottom = -t
                        
                        if mode.upper() == "DXF":
                            GCAM.DXFUtil.addLine(state, [left,top], [right,top], layer, handle)
                            GCAM.DXFUtil.addLine(state, [right,top], [right,bottom], layer, handle)
                            GCAM.DXFUtil.addLine(state, [right,bottom], [left,bottom], layer, handle)
                            GCAM.DXFUtil.addLine(state, [left,bottom], [left,top], layer, handle)
                            handle = handle + 1
                        elif mode.upper() == "DXFSVG":
                            state.add(state.line((left,top),(right,top), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((right,top),(right,bottom), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((right,bottom),(left,bottom), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((left,bottom),(left,top), stroke="black", stroke_width="0.01mm"))
                            #state.add(state.rect((left,top),(right-left,bottom-top), stroke="black", stroke_width="0.01mm"))
                        elif mode.upper() == "BRD":
                            poly = ET.SubElement(state, "polygon", layer=layer, width=lineWidth)
                            ET.SubElement(poly, "vertex", x=str(left), y=str(top))
                            ET.SubElement(poly, "vertex", x=str(right), y=str(top))
                            ET.SubElement(poly, "vertex", x=str(right), y=str(bottom))
                            ET.SubElement(poly, "vertex", x=str(left), y=str(bottom))
                            ET.SubElement(poly, "vertex", x=str(left), y=str(top))
                        else:
                            print "unknown mode = " + mode
                            assert(0)

                inBlack = False

            x = x + 1;
        y = y - 1;

