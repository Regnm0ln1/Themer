from PIL import Image
from sys import argv
from os.path import expanduser
from collections import defaultdict
from color_distance import round_color, score_colors, choose_colors
from color_conversions import RgbToHex, RgbToHsl
from themer_conf import config

def main() -> None:
    # Image to load from first arg when running script
    IMAGE_PATH = argv[1]


    # Configs
    num_colors = config["num_colors"]
    color_rounding = config["color_rounding"]
    mode = config["mode"]
    dark_bound = config["dark_bound"]
    light_bound = config["light_bound"]
    min_dist_to_bg = config["min_dist_to_bg"]
    min_dist_to_other = config["min_dist_to_other"]
    scoring_pow = config["scoring_pow"]
    outputs = config["outputs"]
    x_skip = config["x_skip"]
    y_skip = config["y_skip"]


    # Loads image
    image = Image.open(IMAGE_PATH)
    image_pixel_access = image.load()

    # Dict of colors with rgb value as key and number of pixels with that color as the value
    colors = {}
    chosen_colors = {
        "color_background": None
    }

    for x in range(0, image.width, x_skip):
        for y in range(0, image.height, y_skip):
            # Adds one to instances of color in colors dict or creates it if it doesnt exist 
            try:
                colors[round_color(image_pixel_access[x, y], color_rounding)] += 1
            except:
                colors[round_color(image_pixel_access[x, y], color_rounding)] = 1


    # Sorts dict to choose the most occuring color as the background
    colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))
    for color in colors.keys():
        hue, saturation, lightness = RgbToHsl(color)
        match mode:
            case "auto":
                chosen_colors["color_background"] = color
                break
            case "dark":
                if lightness < dark_bound:
                    chosen_colors["color_background"] = color
                    break
            case "light":
                if lightness > light_bound:
                    chosen_colors["color_background"] = color
                    break

    if chosen_colors["color_background"] == None:
        chosen_colors["color_background"] = next(iter(colors))


    for color_to_choose in range(num_colors - 1):
        chosen_colors[f"color_{color_to_choose}"] = None

    # Assigns score to each color according to brightness and saturation before again sorting it
    score_colors(colors, scoring_pow)
    colors = dict(sorted(colors.items(), key=lambda item: item[1], reverse=True))

    # Chooses colors to be used in theme
    chosen_colors = choose_colors(chosen_colors, colors, min_dist_to_bg, min_dist_to_other)

    for output in outputs:
        color_variables = defaultdict(str, chosen_colors)
        output_text = output["config_text"]

        formatted_output = output_text.format_map(color_variables)

        with open(expanduser(output["file_path"]), "w") as output_file:
            output_file.write(formatted_output)


if __name__ == "__main__":
    main()