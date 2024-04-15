from PIL import Image
import colorsys
from math import floor, atan2, pi, cos, sin, exp
from color_conversions import RgbToHsl, RgbToHex, HslToHex, HslToRgb, HueToRgb, RgbToLab, XyzToLab, LabToXyz

IMAGE_PATH = "images/castle-in-the-clouds.png"

def get_pixels(image_path:str, to_hsl:bool) -> list:
    image = Image.open(image_path)
    image_pixel_access = image.load()
    image_pixels = []
    for x in range(image.width):
        for y in range(image.height):
            #add all the color values to the list, either rgb or hsl depending on hsl param
            image_pixels.append(RgbToHsl(image_pixel_access[x, y]) if to_hsl else image_pixel_access[x, y])

    return image_pixels


def HueExtremes(pixels):
    min_hue = min(pixel[0] for pixel in pixels)
    max_hue = max(pixel[0] for pixel in pixels)
    return min_hue, max_hue


def GetMostFrequent(pixels, RANGE_VAL:int = 12):
    #the amount of wanted colors not including dark and white

    #specyfies how big a range is for a color so 36 would be 10 deg in the hue 1/36 in sat and 1/36 in lum
    RANGE_SIZE = 1/RANGE_VAL

    # list of [hue[sat[lum],[lum]], [sat[lum],[lum]]]
    num_per_color = [[[[] for _ in range(RANGE_VAL)] for _ in range(RANGE_VAL)] for _ in range(RANGE_VAL)]

    num_pixels = 0
    num_allocated_pixels = 0
    for pixel in pixels:
        pixel_indexes = []
        num_pixels += 1
        for color_val in pixel:
            pixel_indexes.append(floor(RANGE_VAL * color_val) if color_val != 1 else RANGE_VAL - 1)
            
        num_allocated_pixels+=1
        # num_per_color[pixel_indexes[0]][pixel_indexes[1]][pixel_indexes[2]] += 1
        num_per_color[pixel_indexes[0]][pixel_indexes[1]][pixel_indexes[2]].append(pixel)

    return num_per_color, num_allocated_pixels



def MeanOfGroup(color_group: list) -> dict:
    colors = {}
    for color in color_group:
        if color not in colors.keys():
            colors[color] = 1
        else:
            colors[color] += 1

    return dict(sorted(colors.items(), key=lambda item: item[1], reverse=True), length=len(color_group))


def sort_colors(colors: list):
    scored = {}
    sorted_colors = {}
    
    for hue_group in colors:
        for sat_group in hue_group:
            for color_group in sat_group:
                group_info = MeanOfGroup(color_group)
                mean_color = next(iter(group_info.keys()))
                if group_info["length"] != 0:
                    sorted_colors[mean_color] = group_info[mean_color] + group_info["length"]*0.5

    sorted_colors = dict(sorted(sorted_colors.items(), key=lambda item: item[1], reverse=True))
    return sorted_colors


def choose_colors(color_dict:dict, dark_bgcolor: bool = True, dark_threshold:float = 0.25, min_lum:float = 0.45, lum_mult:float = 500, vibrancy_mult:float = 500, NUM_WANTED_COLORS:int = 18, reverse:bool = False):
    chosen_colors = {}
    for color in color_dict.keys():
        if color[2] < dark_threshold and dark_bgcolor:
            background_color = color
            break

        elif color[2] > min_lum and not dark_bgcolor:
            background_color = color
            break
    try:
        color_dict.pop(background_color)
        chosen_colors["background"] = background_color
    except:
        print(f"Found no color with less than {dark_threshold} lum (i.e no background color fitting your needs)") if dark_bgcolor else print(f"Found no color with more than {min_lum} lum (i.e no background color fitting your needs)")
        print(f"Choosing background color outside of colors in image...")
        most_frequent_color = color_dict.keys()[0]
        color_dict.pop(most_frequent_color)
        if dark_bgcolor:
            most_frequent_color[2] = dark_threshold

        else:
            most_frequent_color[2] = min_lum

        chosen_colors["background"] = most_frequent_color
    
    NUM_WANTED_COLORS - 1




    for color in list(color_dict.keys()):
        print(score_color(color_dict, color, lum_mult, vibrancy_mult))
        color_dict[color] += score_color(color_dict, color, lum_mult, vibrancy_mult)
        if dark_bgcolor:
            if color[2] < min_lum:
                color_dict.pop(color)

        else:
            if color[2] > dark_threshold:
                color_dict.pop(color)

    print(color_dict)

    chosen_colors["foreground"] = next(iter(color_dict.keys()))

    color_dict = dict(sorted(color_dict.items(), key=lambda item: item[1], reverse=True))
 
    if reverse == False:
        start = 0
        flip = 1
    else:
        start = 15
        flip = -1
    for color_num in range(NUM_WANTED_COLORS-2):

        color = next(iter(color_dict.keys()))

        chosen_colors[f"color{start+color_num*flip}"] = color
        color_dict.pop(color)




    return chosen_colors
#<summary>
#color: the color to score
#lum_mult: a multiplier for the luminosity value; its meant to favor brighter colors
#vibrancy_mult: a multiplier for the vibrancy, which here is defined as color[1]*(1-(abs(color[2] - 0.5)))*2; its meant to favor 
#more "fun" colors and push down greyish, really dark and really bright colors
#the *2 is just to even it out with lum mult since its 0-1.0 while vibrancy is 0-0.5 without it
#returns how many points should be added to the colors score
#</summary>
def score_color(color_dict:dict, color: tuple, lum_mult:float, vibrancy_mult:float):
    points_to_add = 0
    lum_points = color[2] * lum_mult

    vibrancy = color[1]*(1-(abs(color[2] - 0.5)))*2
    vibrancy_points = vibrancy * vibrancy_mult

    points_to_add += lum_points + vibrancy_points

    return points_to_add


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
    C1 = math.sqrt(a1 ** 2 + b1 ** 2)
    C2 = math.sqrt(a2 ** 2 + b2 ** 2)

    # Calculate average chroma
    C_avg = (C1 + C2) / 2

    # Calculate hue angles
    h1 = math.atan2(b1, a1)
    if h1 < 0:
        h1 += 2 * pi
    h2 = math.atan2(b2, a2)
    if h2 < 0:
        h2 += 2 * math.pi

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
    delta_H = 2 * math.sqrt(C1 * C2) * math.sin(delta_h / 2)

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


def main() -> None:
    config_text = ""
    pixels = get_pixels(IMAGE_PATH, True)
    most_common_main_colors, num_allocated = GetMostFrequent(pixels)
    sorted_colors = sort_colors(most_common_main_colors)
    i = 1

    #i'd recommend a negative lum_mult if you want a bright background
    chosen_colors = choose_colors(sorted_colors, dark_bgcolor=False, lum_mult=-50, vibrancy_mult=10, reverse=False, min_lum=0.4, dark_threshold=0.65)
    for color_type, color in chosen_colors.items():
        final_color = HslToHex(color)
        config_text += f"{color_type} {final_color} \n"
    config_text += f"background_opacity {0.8}"
    print(config_text)

    



if __name__ == "__main__":
    main()