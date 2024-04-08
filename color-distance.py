from PIL import Image
import colorsys

IMAGE_PATH = "../test_image.jpg"

def get_pixels(image_path:str, to_hsl:bool) -> list:
    image = Image.open(image_path)
    image_pixel_access = image.load()
    image_pixels = []
    for x in range(image.width):
        for y in range(image.height):
            #add all the color values to the list, either rgb or hsl depending on hsl param
            image_pixels.append(RgbToHsl(image_pixel_access[x, y]) if to_hsl else image_pixel_access[x, y])

    return image_pixels


def RgbToHsl(pixel:tuple) -> tuple:
    #stolen from https://stackoverflow.com/questions/2353211/hsl-to-rgb-color-conversion

    r, g, b = pixel
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
    return (h, s, l)


def rgb2lab ( inputColor ) :

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

def HueExtremes(pixels):
    min_hue = min(pixel[0] for pixel in pixels)
    max_hue = max(pixel[0] for pixel in pixels)
    return min_hue, max_hue

def GetMostFrequent(pixels):
    #the amount of wanted colors not including dark and white
    NUM_WANTED_COLORS = 16
    RANGE_SIZE = 1/NUM_WANTED_COLORS

    # White cutoff is -0.120x^(2.00) + 0.220x + 0.850 where x is lum and y is the WHITE_CUTOFF, based off of lum 0, 50 and 100
    # Black cutoff is 0.0800x^(2.00) - 0.160x + 0.120 where x is lum andy is the WHITE_CUTOFF, based off of lum 0, 50 and 100
    num_per_color = [0] * (NUM_WANTED_COLORS + 2)

    num_pixels = 0
    num_allocated_pixels = 0
    for pixel in pixels:
        white_cutoff = -0.120 * pixel[1]**2 + 0.220 * pixel[1] + 0.85
        black_cutoff = 0.0800 * pixel[1]**2 - 0.160 * pixel[1] + 0.12
        num_pixels += 1
        if pixel[2] >= white_cutoff:
            num_per_color[-2] += 1
        
        elif pixel[2] <= black_cutoff:
            num_per_color[-1] += 1
    
        else:
            for i in range(NUM_WANTED_COLORS):
                if pixel[0] >= i * 1 / NUM_WANTED_COLORS and pixel[0] <= (i+1)* 1 / NUM_WANTED_COLORS:
                    num_per_color[i] += 1
                    num_allocated_pixels += 1
                    continue

    return num_per_color



def main():
    pixels = get_pixels(IMAGE_PATH, True)

    most_common_main_colors = GetMostFrequent(pixels)

    print(most_common_main_colors)


if __name__ == "__main__":
    main()