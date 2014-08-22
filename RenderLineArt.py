import png
import StringIO
import time

def RenderLineArt(f, name, inputDotsPerInch, threshold, maxBoxHeight):
    rowMultiplier = 1
    xPixelSize = (1.0/inputDotsPerInch) * 1000 # file format requires mils
    yPixelSize = (1.0/inputDotsPerInch) * 1000 # file format requires mils
    if yPixelSize > maxBoxHeight:
        rowMultiplier = int(math.ceil(yPixelSize/maxBoxHeight))
        yPixelSize = yPixelSize/rowMultiplier

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

                        b.write("CLOSED 5 1 1 -1\r\n")
                        b.write("%d   %d\r\n" % (left, top))
                        b.write("%d   %d\r\n" % (right, top))
                        b.write("%d   %d\r\n" % (right, bottom))
                        b.write("%d   %d\r\n" % (left, bottom))
                        b.write("%d   %d\r\n" % (left, top))
                        c = c + 1
                inBlack = False

            x = x + 1;
        y = y - 1;

    out = StringIO.StringIO()
    out.write("*PADS-LIBRARY-LINE-ITEMS-V9*\r\n")
    out.write("\r\n") 
    out.write("%s LINES    I -16705 -16140 %d 0\r\n" % (name, c))
    out.write("TIMESTAMP %s\r\n" % time.strftime("%Y:%m:%d:%H:%M:%S")) 
    out.write(b.getvalue())
    out.write("""\r\n*END*\r\n""")

    return out.getvalue()
