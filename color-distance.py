from PIL import Image
import colorsys
from math import floor
from color_conversions import RgbToHsl, RgbToHex, HslToHex, HslToRgb, HueToRgb, RgbToLab

IMAGE_PATH = "images/purple-pink-sunset.jpg"

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


def choose_colors(color_dict:dict, dark_bgcolor: bool = True, dark_threshold:float = 0.25, min_lum:float = 0.45, lum_mult:float = 500, NUM_WANTED_COLORS:int = 18, reverse:bool = False):
    chosen_colors = {}
    if dark_bgcolor:
        background_color = next(iter(color_dict.keys()))
        while background_color[2] > dark_threshold:
            background_color = next(iter(color_dict.keys()))

        color_dict.pop(background_color)
        chosen_colors["background"] = background_color
        NUM_WANTED_COLORS - 1




    for color in list(color_dict.keys()):
        color_dict[color] += score_color(color_dict, color, lum_mult)
        if color[2] < min_lum:
            color_dict.pop(color)

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


def score_color(color_dict:dict, color: tuple, lum_mult:float):
    points_to_add = color[2] * lum_mult
    return points_to_add

def main() -> None:
    config_text = ""
    pixels = get_pixels(IMAGE_PATH, True)
    most_common_main_colors, num_allocated = GetMostFrequent(pixels)
    sorted_colors = sort_colors(most_common_main_colors)
    i = 1

    chosen_colors = choose_colors(sorted_colors, lum_mult=50, reverse=False, dark_threshold=0.3)
    for color_type, color in chosen_colors.items():
        final_color = HslToHex(color)
        config_text += f"{color_type} {final_color} \n"
    config_text += f"background_opacity {0.8}"
    print(config_text)

    



if __name__ == "__main__":
    main()