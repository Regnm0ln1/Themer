from PIL import Image
import colorsys
from math import floor, atan2, pi, cos, sin, exp, sqrt
from color_conversions import RgbToHsl, RgbToHex, HslToHex, HslToRgb, HueToRgb, RgbToLab, XyzToLab, LabToXyz
import sys



def delta_e_cie2000(rgb1:tuple, rgb2:tuple) -> float:
    """
    calculates the difference or distance between colors, i.e how easily they are to tell apart, 1 is just noticeable
    takes in to colors rgb1 (tuple) and rgb2 (tuple)
    returns a float, the difference
    """

    # Taken from Chat GPT
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

def score_colors(colors:dict, scoring_pow: float = 2):
    """
    Scores colors based on light value and saturation value, it aims to priortize colors that are more 'interesting' 
    It takes in a dictionary of colors, this dictionary is then mutated, nothing is returned
    """
    for color in colors.keys():
        h, s, l = RgbToHsl(color)
        l_score = 1 - l
        # Colors[color] = colors[color] + (s * l_score)*100000
        colors[color] *= (s * l_score)**scoring_pow


def choose_colors(chosen_colors:dict, colors:dict, min_dist_to_bg: int, min_dist_to_others:int, num_colors:int = 18) -> dict:
    """
    This function chooses colors by looping over a dict of colors and comparing their distance to the background color through the delta_e_cie2000 function, it returns a list of the choosen colors
    It takes in a background_color (tuple) to compare other colors to, a colors (dict) to choose colors from, it should be sorted according to prioritized colors, it also takes in a min_color_dist (int) which is the minimum distance to background_color that is accepted, takes in num_colors (int) which includes the background_color
    """


    colors_to_choose = num_colors
    for color in colors.keys():
        if delta_e_cie2000(chosen_colors["color_background"], color) > min_dist_to_bg:
            for chosen_color in chosen_colors.values():
                if chosen_color == None:
                    chosen_colors[f"color_{18 - colors_to_choose}"] = color
                    colors_to_choose -= 1
                    # if len(chosen_colors.keys()) == num_colors:
                    if colors_to_choose == 0:
                        break
                elif delta_e_cie2000(color, chosen_color) > min_dist_to_others:
                    continue
                
                break


            # chosen_colors[f"color_{18 - colors_to_choose}"] = color
            # colors_to_choose -= 1
            # # if len(chosen_colors.keys()) == num_colors:
            # if colors_to_choose == 0:
            #     break

    # print(chosen_colors)
    for color_key in chosen_colors.keys():
        chosen_colors[color_key] = RgbToHex(chosen_colors[color_key])

    return chosen_colors


def round_color(color: tuple, rounding: int = 32):
    """
    Rounds colors to (0-8, 0-8, 0-8) before scaling them up to (0-256, 0-256, 0-256)
    takes in a color (tuple) in rgb format
    """

    try:
        r, g, b = color
    except:
        r, g, b, a = color

    r = r // rounding * rounding
    g = g // rounding * rounding
    b = b // rounding * rounding

    
    return (r, g, b)