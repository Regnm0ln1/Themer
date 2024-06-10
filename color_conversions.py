"""
File to handle all color conversions needed for Themer.
"""

def RgbToHsl(color:tuple) -> tuple:
    """
    stolen from https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion
    Convert from RGB to HSL by supplying a tuple of (Red, Green, Blue)
    Returns the same color in HSL, also in the form of a tuple
    """


    r, g, b = color
    r /= 255
    g /= 255
    b /= 255

    vmax = max(r, g, b)
    vmin = min(r, g, b)
    h = (vmax + vmin) / 2
    s = (vmax + vmin) / 2
    l = (vmax + vmin) / 2

    if (vmax == vmin):
        return (0, 0, l)

    d = vmax - vmin
    s = d / (2 - vmax - vmin) if l > 0.5 else d / (vmax + vmin)
    if vmax == r:
        h = (g - b) / d + (6 if g < b else 0)
    if vmax == g:
        h = (b - r) / d + 2
    if vmax == b:
        h = (r - g) / d + 4

    h /= 6
    return (round(h, 2), round(s, 2), round(l, 2))


def HslToRgb(color: tuple):
    """
    Convert from hsl to Rgb by supplying a tuple of (Hue, Saturation, Luminance)
    Returns the same color 
    """
    h, s, l = color
    if s == 0:
        return (round(l*255), round(l*255), round(l*255))
    
    if l < 0.5:
        q = l * (1 + s)
    else:
        q = l + s - l * s
    
    p = 2 * l - q
    r = HueToRgb(p, q, h + 1/3)
    g = HueToRgb(p, q, h)
    b = HueToRgb(p, q, h - 1/3)
    return (round(r*255), round(g*255), round(b*255))

def HueToRgb(p, q, t):
    """
    'subfunction' of HslTORgb, not meant to be called from outside it
    """
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1/6:
        return p + (q - p) * 6 * t
    if t < 1/2:
        return q
    if t < 2/3:
        return p + (q - p) * (2/3 - t) * 6
    return p


def RgbToHex(color):
    """
    Convert RGB color space to hexadecimal color code.
    All values assumed to be in the range [0, 1].
    """
    r, g, b = color

    return "#{:02X}{:02X}{:02X}".format(int(r), int(g), int(b))

def HslToHex(color:tuple):
    """
    Convert HSL color space to hexadecimal color code.
    All values assumed to be in the range [0, 1].
    """

    r, g, b = HslToRgb(color)
    return RgbToHex(r, g, b)


def RgbToLab (inputColor:tuple) -> list:
    """
    stolen form https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python
    takes an color in the RGB color space. InputColor should be a tuple. (0-255, 0-255, 0-255)
    Reurns a List in the LAB color space. The LAB conversion uses D65 as an illuminant (something I dont really understand)
    """
    num = 0
    RGB = [0, 0, 0]

    for value in inputColor :
        value = float(value) / 255

        if value > 0.04045 :
            value = ( ( value + 0.055 ) / 1.055 ) ** 2.4
        else :
            value = value / 12.92

        RGB[num] = value * 100
        num = num + 1

    XYZ = [0, 0, 0,]

    X = RGB [0] * 0.4124 + RGB [1] * 0.3576 + RGB [2] * 0.1805
    Y = RGB [0] * 0.2126 + RGB [1] * 0.7152 + RGB [2] * 0.0722
    Z = RGB [0] * 0.0193 + RGB [1] * 0.1192 + RGB [2] * 0.9505
    XYZ[ 0 ] = round( X, 4 )
    XYZ[ 1 ] = round( Y, 4 )
    XYZ[ 2 ] = round( Z, 4 )

    XYZ[ 0 ] = float( XYZ[ 0 ] ) / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    XYZ[ 1 ] = float( XYZ[ 1 ] ) / 100.0          # ref_Y = 100.000
    XYZ[ 2 ] = float( XYZ[ 2 ] ) / 108.883        # ref_Z = 108.883

    num = 0
    for value in XYZ :

        if value > 0.008856 :
            value = value ** ( 0.3333333333333333 )
        else :
            value = ( 7.787 * value ) + ( 16 / 116 )

        XYZ[num] = value
        num = num + 1

    Lab = [0, 0, 0]

    L = ( 116 * XYZ[ 1 ] ) - 16
    a = 500 * ( XYZ[ 0 ] - XYZ[ 1 ] )
    b = 200 * ( XYZ[ 1 ] - XYZ[ 2 ] )

    Lab [ 0 ] = round( L, 4 )
    Lab [ 1 ] = round( a, 4 )
    Lab [ 2 ] = round( b, 4 )

    return Lab

def XyzToLab(xyz):
    # XYZ to Lab conversion
    X, Y, Z = xyz
    var_X = X / 95.047
    var_Y = Y / 100.000
    var_Z = Z / 108.883

    if var_X > 0.008856:
        var_X = var_X ** (1 / 3)
    else:
        var_X = 7.787 * var_X + 16 / 116
    if var_Y > 0.008856:
        var_Y = var_Y ** (1 / 3)
    else:
        var_Y = 7.787 * var_Y + 16 / 116
    if var_Z > 0.008856:
        var_Z = var_Z ** (1 / 3)
    else:
        var_Z = 7.787 * var_Z + 16 / 116

    L = 116 * var_Y - 16
    a = 500 * (var_X - var_Y)
    b = 200 * (var_Y - var_Z)

    return L, a, b

def LabToXyz(lab):
    # Lab to XYZ conversion
    L, a, b = lab
    var_Y = (L + 16.0) / 116.0
    var_X = a / 500.0 + var_Y
    var_Z = var_Y - b / 200.0

    if var_Y ** 3 > 0.008856:
        var_Y = var_Y ** 3
    else:
        var_Y = (var_Y - 16.0 / 116.0) / 7.787
    if var_X ** 3 > 0.008856:
        var_X = var_X ** 3
    else:
        var_X = (var_X - 16.0 / 116.0) / 7.787
    if var_Z ** 3 > 0.008856:
        var_Z = var_Z ** 3
    else:
        var_Z = (var_Z - 16.0 / 116.0) / 7.787

    X = var_X * 95.047
    Y = var_Y * 100.000
    Z = var_Z * 108.883

    return X, Y, Z