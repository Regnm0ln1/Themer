from PIL import Image
import colorsys
from math import floor, atan2, pi, cos, sin, exp, sqrt
from color_conversions import RgbToHsl, RgbToHex, HslToHex, HslToRgb, HueToRgb, RgbToLab, XyzToLab, LabToXyz



def delta_e_cie2000(rgb1, rgb2):
    #Taken from Chat GPT
    lab1 = RgbToLab(rgb1)
    lab2 = RgbToLab(rgb2)

    # Calculate CIEDE2000 color difference
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2

    # Convert Lab to XYZ
    xyz1 = LabToXyz(lab1)
    xyz2 = LabToXyz(lab2)

    # Calculate CIELab chroma (C)
    C1 = sqrt(a1 ** 2 + b1 ** 2)
    C2 = sqrt(a2 ** 2 + b2 ** 2)

    # Calculate average chroma
    C_avg = (C1 + C2) / 2

    # Calculate hue angles
    h1 = atan2(b1, a1)
    if h1 < 0:
        h1 += 2 * pi
    h2 = atan2(b2, a2)
    if h2 < 0:
        h2 += 2 * pi

    # Calculate delta L, delta C, delta h
    delta_L = L2 - L1
    delta_C = C2 - C1

    # Ensure hue difference falls within range of -π to +π
    delta_h = h2 - h1
    if abs(delta_h) > pi:
        if delta_h < 0:
            delta_h += 2 * pi
        else:
            delta_h -= 2 * pi

    # Calculate CIEDE2000 color difference
    delta_H = 2 * sqrt(C1 * C2) * sin(delta_h / 2)

    # Calculate CIEDE2000 terms
    L_avg = (L1 + L2) / 2
    C_avg = (C1 + C2) / 2

    h_avg = (h1 + h2) / 2
    if abs(h1 - h2) > pi:
        h_avg += pi

    T = 1 - 0.17 * cos(h_avg - pi / 6) + 0.24 * cos(2 * h_avg) + 0.32 * cos(3 * h_avg + pi / 30) - 0.20 * cos(4 * h_avg - 21 * pi / 60)

    delta_theta = 30 * exp(-((h_avg - 275) / 25) ** 2)

    R_C = 2 * sqrt(C_avg ** 7 / (C_avg ** 7 + 25 ** 7))

    S_L = 1 + (0.015 * (L_avg - 50) ** 2) / sqrt(20 + (L_avg - 50) ** 2)
    S_C = 1 + 0.045 * C_avg
    S_H = 1 + 0.015 * C_avg * T

    R_T = -sin(2 * delta_theta) * R_C

    # Calculate CIEDE2000 color difference
    delta_E = sqrt((delta_L / S_L) ** 2 + (delta_C / S_C) ** 2 + (delta_H / S_H) ** 2 + R_T * (delta_C / S_C) * (delta_H / S_H))

    return delta_E

def round_color(color: tuple):
    # rounds colors down to (0-8, 0-8, 0-8)

    r, g, b = color
    r = r // 32 * 32
    g = g // 32 * 32
    b = b // 32 * 32

    
    return (r, g, b)


def main() -> None:
    IMAGE_PATH = "images/purple-pink-sunset.jpg"
    image = Image.open(IMAGE_PATH)
    image_pixel_access = image.load()
    image_pixels = []
    colors = {}
    min_color_dist = 15
    for x in range(image.width):
        for y in range(image.height):
            # print(round_color(image_pixel_access[x, y]))
            #add all the color values to the list, either rgb or hsl depending on hsl param
            # image_pixels.append(image_pixel_access[x, y])
            try:
                colors[round_color(image_pixel_access[x, y])] += 1
            except:
                colors[round_color(image_pixel_access[x, y])] = 1

    colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))

    background_color = next(iter(colors))

    chosen_colors = []
    for color in colors.keys():
        if delta_e_cie2000(background_color, color) > min_color_dist:
            chosen_colors.append(color)
            if len(chosen_colors) == 17:
                break
    config_text = ""
    config_text += f"background {RgbToHex(background_color)} \n"
    config_text += f"foreground {RgbToHex(chosen_colors[0])} \n"
    for ind, color in enumerate(chosen_colors[1:]):
        config_text += f"color{ind} {RgbToHex(color)} \n"

    config_text += "background_opacity 0.8"


    print(config_text)


    



if __name__ == "__main__":
    main()