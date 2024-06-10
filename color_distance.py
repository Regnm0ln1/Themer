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

def invert_color(color:tuple) -> tuple:
    """
    Inverts a color
    takes in a color in the hsl colorspace and returns an inverted color in the hsl colorspace
    """

    h, s, l = color
    if h > 0.5: h -= 0.5 
    else: h += 0.5
    return (h, s, 1 - l)

def score_colors(colors:dict, scoring_options:dict, background_color):
    """
    Scores colors based on light value and saturation value, it aims to priortize colors that are more 'interesting' 
    It takes in a dictionary of colors, this dictionary is then mutated, nothing is returned
    """
    for color in colors.keys():
        h, s, l = RgbToHsl(color)
        l_score = 1 - l

        # If vibrancy scoring is active
        if scoring_options["vibrancy"]["active"]:

            # If exponential
            if scoring_options["vibrancy"]["exponential"]: colors[color] *= (s * l_score) ** scoring_options["vibrancy"]["scoring_var"]

            # If multiplicative
            else: colors[color] *= (s*l_score) * scoring_options["vibrancy"]["scoring_var"]
        
        # If scoring by closeness to inverted bg is acitve
        if scoring_options["inverted_bg"]["active"]:
            # Convert background color to hsl
            hsl_bg = RgbToHsl(background_color)
            
            # Invert background color
            inverted_bg = HslToRgb(invert_color(hsl_bg))

            dist_to_inv_bg = delta_e_cie2000(color, inverted_bg)

            # Get multiplier by taking 1/min_limit if dist is too small, 1/dist or 1/max_limit if dist is to big
            multiplier = 1/max(scoring_options["inverted_bg"]["min_limit"], min(dist_to_inv_bg, scoring_options["inverted_bg"]["max_limit"]))
            
            # If exponential
            if scoring_options["inverted_bg"]["exponential"]: colors[color] *= multiplier ** scoring_options["inverted_bg"]["scoring_var"]

            # If multiplicative
            else: colors[color] *= multiplier * scoring_options["inverted_bg"]["scoring_var"]

def triad_generation(colors:dict, chosen_colors:dict):
    """
    This function generates to new colors, 60 degs from each other and 60 deg from the background color
    Takes in colors (currently not used) and chosen_colors
    Returns both triad colors in the rgb colorspace
    """
    h_bg, s_bg, l_bg = RgbToHsl(chosen_colors["color_background"])
    triad1 = (abs(h_bg - 1/3), s_bg, l_bg)
    triad2 = (abs(h_bg - 2/3), s_bg, l_bg)
    return HslToRgb(triad1), HslToRgb(triad2)

def pairify_color(color:tuple, organisation_offset:int):
    """
    This function generates a second color that is either lighter or darker than the supplied color depending on wether the lightness of the supplied color is above or below 0.5
    Takes in a color (0 - 1) and an organisation_offset, how much the lightness of the second color will differ from the original color.
    Returns the lighter color followed by the darker color
    """

    hue, saturation, lightness = RgbToHsl(color)
    if lightness >= 0.5: 
        color_light_to_add = color
        color_dark_to_add = HslToRgb((hue, saturation, lightness - organisation_offset)) 

    # Make a new lighter color if color is darker than 0.5
    else: 
        color_light_to_add = HslToRgb((hue, saturation, lightness + organisation_offset))
        color_dark_to_add = color

    return color_light_to_add, color_dark_to_add

def apply_triads(colors:dict, chosen_colors:dict, organisation, organisation_offset:float, num_colors:int, color_pairs_chosen:int, colors_to_choose:int, num_color_pairs:int):
    """
    Adds the Triad colors to the chosen_colors dict, however many of them fit within the num_colors designated in themer_conf.py
    Takes in colors, chosen_colors, organisation, organisation_offset, num_colors, color_pairs_chosen, colors_to_chose, num_color_pairs
    Returns colors_to_choose and color_pairs chosen, since those are ints(immutable) and will change in the function
    """

    triad1, triad2 = triad_generation(colors, chosen_colors)
    if organisation == None:
        chosen_colors[f"color_{num_colors - 1 - colors_to_choose}"] = triad1
        chosen_colors[f"color_{num_colors - colors_to_choose}"] = triad2
        colors_to_choose -= 2

    else:
        if chosen_colors["color_0"] == None:
            chosen_colors["color_0"] = triad1
            triad_light, triad_dark = pairify_color(triad2, organisation_offset)
            match organisation:
                case "pairs":
                    chosen_colors["color_1"] = triad_dark
                    chosen_colors["color_9"] = triad_light

                case "pairs_reversed":
                    chosen_colors["color_1"] = triad_light
                    chosen_colors["color_9"] = triad_dark
                
            color_pairs_chosen += 1
            colors_to_choose -= 3
            
        else:
            triad2_light, triad2_dark = pairify_color(triad2, organisation_offset)
            triad1_light, triad1_dark = pairify_color(triad1, organisation_offset)
            match organisation:
                case "pairs":
                    chosen_colors[f"color_{color_pairs_chosen + 1}"] = triad1_dark
                    chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = triad1_light
                    color_pairs_chosen += 1
                    colors_to_choose -= 2

                    if None not in chosen_colors.values():
                        return colors_to_choose, color_pairs_chosen

                    chosen_colors[f"color_{color_pairs_chosen + 1}"] =  triad2_dark
                    chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = triad2_light
                    color_pairs_chosen += 1
                    colors_to_choose -= 2

                case "pairs_reversed":
                    triad1_light, triad1_dark = pairify_color(triad1, organisation_offset)
                    triad2_light, triad2_dark = pairify_color(triad2, organisation_offset)
                    chosen_colors[f"color_{color_pairs_chosen + 1}"] = triad1_light
                    chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = triad1_dark
                    color_pairs_chosen += 1
                    colors_to_choose -= 2

                    if None not in chosen_colors.values():
                        return colors_to_choose, color_pairs_chosen

                    chosen_colors[f"color_{color_pairs_chosen + 1}"] =  triad2_light
                    chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = triad2_dark
                    color_pairs_chosen += 1
                    colors_to_choose -= 2


    return colors_to_choose, color_pairs_chosen

def like_generation(chosen_colors:dict, deg_incrementation):
    """
    Generates like colors by rotating the hue of the foreground color based on deg_incrementation
    Takes chosen_colors, deg_incrementation
    Returns two like colors, one rotated positively and one negatively
    """

    h_fg, s_fg, l_fg = RgbToHsl(chosen_colors["color_0"])
    like1 = HslToRgb((h_fg + deg_incrementation, s_fg, l_fg))
    like2 = HslToRgb((h_fg - deg_incrementation, s_fg, l_fg))
    return like1, like2

def apply_likes(colors:dict, chosen_colors:dict, organisation, organisation_offset:float, num_colors:int, color_pairs_chosen:int, colors_to_choose:int, num_color_pairs:int, deg_incrementation:float, max_rotation:float):
    """
    Generates and applies like colors by rotating the hue more and more in different directions, until the max_rotation by degrees set using deg_incrementation
    Takes in colors, chosen_colors, organisation, organisation_offset, num_colors, colors_pairs_chosen, colors_to_choose, num_color_pairs, deg_incrementation and max_rotation
    It returns colors_to_choose and color_pairs_chosen, since both are ints(immutable) that are supposed to change in the function
    """

    if chosen_colors["color_0"] == None:
        # Like shouldnt be used as a first generation option in case there isn't a foreground color chosen, this is a quick fix until there are more options for generation
        chosen_colors["color_0"] = HslToRgb(invert_color(RgbToHsl(chosen_colors["color_background"])))

    # Rotate hue more and more until max_rotation (included) is reached or until all colors are filled
    for rotation in range(deg_incrementation, max_rotation + deg_incrementation, deg_incrementation):
        # Generate like colors
        like1, like2 = like_generation(chosen_colors, rotation/360)

        # Just add them if we dont care about organisation
        if organisation == None:
            chosen_colors[f"color_{num_colors - 1 - colors_to_choose}"] = like1
            chosen_colors[f"color_{num_colors - colors_to_choose}"] = like2

            colors_to_choose -= 2

        else:
            match organisation:
                # Darker color first in pair
                case "pairs":
                    # If no foreground, use first like color as forground
                    if chosen_colors["color_0"] == None:
                        chosen_colors["color_0"] = like1

                        # Make pair of second like color
                        like2_light, like2_dark = pairify_color(like2, organisation_offset)
                        # These are hardcoded because foreground will always be chosen first    ### Hope this doesn't come back to bite me
                        chosen_colors["color_1"] = like2_dark
                        chosen_colors["color_9"] = like2_light

                        # Three colors have been chosen
                        colors_to_choose -= 3

                    else:
                        # Make pairs of both like colors
                        like1_light, like1_dark = pairify_color(like1, organisation_offset) 
                        like2_light, like2_dark = pairify_color(like2, organisation_offset) 

                        # Insert first pair
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = like1_dark
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = like1_light
                        color_pairs_chosen += 1

                        # Check if all colors are chosen, break in that case
                        colors_to_choose -= 2
                        
                        if None not in chosen_colors.values():
                            break
                    
                        # Insert second pair
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = like2_dark
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = like2_light
                        color_pairs_chosen += 1

                        colors_to_choose -= 2
                
                # Lighter color first in pair
                case "pairs_reversed":
                    # If no foreground, use first like color as forground
                    if chosen_colors["color_0"] == None:
                        chosen_colors["color_0"] = like1
                        like2_light, like2_dark = pairify_color(like2, organisation_offset)

                        # Make pair of second like color
                        chosen_colors["color_1"] = like2_light
                        chosen_colors["color_9"] = like2_dark

                        # Three colors have been chosen
                        colors_to_choose -= 3

                    else:
                        # Make pairs of both like colors
                        like1_light, like1_dark = pairify_color(like1, organisation_offset) 
                        like2_light, like2_dark = pairify_color(like2, organisation_offset) 

                        # Insert first pair
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = like1_dark
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = like1_light
                        color_pairs_chosen += 1

                        # Check if all colors are chosen, break in that case
                        colors_to_choose -= 2
                        if None not in chosen_colors.values():
                            break

                        # Insert second pair
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = like2_dark
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = like2_light
                        color_pairs_chosen += 1

                        colors_to_choose -= 2

            # If the second pair was the last, break
            if None not in chosen_colors.values():
                break

    return colors_to_choose, color_pairs_chosen


def choose_colors(chosen_colors:dict, colors:dict, min_dist_to_bg: int, min_dist_to_others:int, num_colors:int, organisation, organisation_offset:float, generation_options:list) -> dict:
    """
    This function chooses colors by looping over a dict of colors and comparing their distance to the background color through the delta_e_cie2000 function, it returns a dict of the choosen colors
    It takes in a background_color (tuple) to compare other colors to, a colors (dict) to choose colors from, it should be sorted according to prioritized colors, it also takes in a min_color_dist (int) which is the minimum distance to background_color that is accepted, takes in num_colors (int) which includes the background_color
    """

    colors_to_choose = num_colors -1
    # Remove background (color_background) and foreground (color_0) before dividing by two, because they're pairs
    num_color_pairs = (num_colors - 2)//2
    color_pairs_chosen = 0
    for color in colors.keys():
        if delta_e_cie2000(chosen_colors["color_background"], color) > min_dist_to_bg:
            # Loop through all chosen_colors to see if color is far enough from them
            for chosen_color in chosen_colors.values():
                # If chosen_color is a color and its chosen color is to close to color, break to get a new color 
                if (chosen_color != None) and (delta_e_cie2000(color, chosen_color) < min_dist_to_others):
                    break

            # Reaching here means that color has made it through all already chosen_colors and is therefore far enough from them
            # If color_pairing is wanted and a foreground color has been chosen
            if (organisation != None) and (chosen_colors["color_0"] != None):
                # print(f"{color_pairs_chosen}: {color}")
                color_light_to_add, color_dark_to_add = pairify_color(color, organisation_offset)
                
                # print(color_pairs_chosen)
                # Depening on if lighter or darker colors should be the first in the pairs
                match organisation:
                    # Darker first
                    case "pairs":
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = color_dark_to_add
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = color_light_to_add
                        color_pairs_chosen += 1

                    # Lighter first
                    case "pairs_reversed":
                        chosen_colors[f"color_{color_pairs_chosen + 1}"] = color_light_to_add
                        chosen_colors[f"color_{color_pairs_chosen + 1 + num_color_pairs}"] = color_dark_to_add
                        color_pairs_chosen += 1
                        # print(color_pairs_chosen)
                        # print(f"{color_pairs_chosen}: {color_light_to_add}(light), {color_dark_to_add}(dark)")

                # Some of the ugliest shit ive ever written
                # Were only removing 1 to not mess up the numbering in the chosen_colors dict, and then making sure we aren't below half of num_colors (total colors to choose), this is because we actually choosing color pairs
                colors_to_choose -= 2
                if color_pairs_chosen == num_color_pairs:
                    break

            # First choose a foreground color or if colors shouldn't be organised
            else:
                chosen_colors[f"color_{num_colors - 1 - colors_to_choose}"] = color
                colors_to_choose -= 1
                if colors_to_choose == 0:
                    break

    # print(chosen_colors)

    if None in chosen_colors.values():
        for generation_method in generation_options:
            match generation_method["name"]:
                case "triad":
                    colors_to_choose, color_pairs_chosen = apply_triads(colors, chosen_colors, organisation, organisation_offset, num_colors, color_pairs_chosen, colors_to_choose, num_color_pairs)
                    print(chosen_colors)
                case "like":
                    if None in chosen_colors.values():
                        colors_to_choose, color_pairs_chosen = apply_likes(colors, chosen_colors, organisation, organisation_offset, num_colors, color_pairs_chosen, colors_to_choose, num_color_pairs, generation_method["deg_incrementation"], generation_method["max_rotation"])
    print(chosen_colors)
    # for color in chosen_colors.keys():
    #     print(f"{color}: {chosen_colors[color]}")


                
            
    # Make all chosen colors HEX
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
