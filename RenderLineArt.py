import png
import StringIO
import time
from lxml import etree as ET
import math
import DXFUtil

def RenderLineArt(f, name, inputDotsPerInch, threshold, maxBoxHeight, layer, lineWidth, state, mode="BRD"):

#    root = ET.Element("package", name=name)

    rowMultiplier = 1
    xPixelSize = (1.0/inputDotsPerInch) * 25.4 # We use mm
    yPixelSize = (1.0/inputDotsPerInch) * 25.4 # we use mm
#    if yPixelSize > maxBoxHeight:
#        rowMultiplier = int(math.ceil(yPixelSize/maxBoxHeight))
#        yPixelSize = yPixelSize/rowMultiplier

    r = png.Reader(f)
    (width, height, pixels, crap) = r.asRGBA()

    b = StringIO.StringIO()

    c = 0
    y = 0
    handle = 255
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
                        top =     (y*rowMultiplier*yPixelSize + i*yPixelSize)
                        bottom =  top + yPixelSize
                        left =    startx * xPixelSize
                        right =   (x-1)*xPixelSize + xPixelSize

                        t = top
                        top = -bottom
                        bottom = -t
                        
                        if mode == "dxf":
                            DXFUtil.addLine(state, [left,top], [right,top], "layer 1", handle)
                            DXFUtil.addLine(state, [right,top], [right,bottom], "layer 1", handle)
                            DXFUtil.addLine(state, [right,bottom], [left,bottom], "layer 1", handle)
                            DXFUtil.addLine(state, [left,bottom], [left,top], "layer 1", handle)
                            handle = handle + 1
                        elif mode == "svg":
                            state.add(state.line((left,top),(right,top), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((right,top),(right,bottom), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((right,bottom),(left,bottom), stroke="black", stroke_width="0.01mm"))
                            state.add(state.line((left,bottom),(left,top), stroke="black", stroke_width="0.01mm"))
                            #state.add(state.rect((left,top),(right-left,bottom-top), stroke="black", stroke_width="0.01mm"))
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

