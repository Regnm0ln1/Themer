config = {
    # The number of colors including background, foreground and color0-15
    "num_colors": 18,

    # How much colors should be rounded, standard is 32, since i felt like it
    "color_rounding": 32,


    # Can be "auto", "dark" or "light"
    # Will determine if "color_background" will be dark, light or whatever appears the most in the image
    # Whether a color is light or dark is determined by "light_bound" and "dark_bound". If no color is found within the wanted lightness "color_background" will be set to whatever color appears the most
    "mode": "dark",


    # Following two options are used in order to choose a "color_background", when "light" or "dark" has been specified for "mode" 

    # What lightness value (0 - 1) and below is considered dark
    # So if it is 0.2 all colors with a lightness below or at 0.2 are dark
    "dark_bound": 0.2,

    # What lightness value (0 - 1) and above is considered light
    # So if it is 0.7 all colors with lightness values above or at 0.7 are light
    "light_bound": 0.7,

    # When there arent enough colors in the picture or they are too close, generate new colors
    # Options are Blend, Triad, Like and Monochromatic
    # Blend will blend the different colors that it found to varying amounts
    # Triad will take color_0 and rotate 60 deg in both hue directions. Based on those 3 points it will vary hue, saturation and lightness a little to generate enough colors
    # Like will use color_0 as base and select colors by rotating hue a couple of degress in both directions
    # Monochromatic will vary lightness and saturation of color_0 to create different colors
    "generation": None,

    # How far the color_dist should be from background color, calculated with delta_e_cie2000 function
    "min_dist_to_bg": 35,

    # Same as to_bg but for other colors
    "min_dist_to_other": 0,

    # The power that is used in scoring function, higher scoring_pow means the function will prioritize more "vibrant", i.e those that have higher saturation and a brightness closer to 50%, more when choosing colors
    "scoring_pow": 2,

    # How big the increases should be on the x-axis when reading the pixels with PILLOW, helps shorted time but will give worse results the bigger it is
    "x_skip": 1,
    # Same but for y axis,
    "y_skip": 1,

    # A list of what main.py will output
    "outputs": [
        {
            # Path to file to be outputed into
            "file_path": "~/.config/kitty/current-theme.conf",

            # What will be outputed into the file above, you can use "color_background" and color_{0-num_colors-2}
            "config_text": """background {color_background} 
foreground {color_0}
color0 {color_1}
color1 {color_2} 
color2 {color_3} 
color3 {color_4} 
color4 {color_5} 
color5 {color_6} 
color6 {color_7} 
color7 {color_8} 
color8 {color_9} 
color9 {color_10} 
color10 {color_11} 
color11 {color_12}
color12 {color_13} 
color13 {color_14} 
color14 {color_15} 
color15 {color_16} 

cursor {color_3}

active_border_color {color_1}
inactive_border_color {color_background}

selection_foreground {color_background}
selection_background {color_0}

background_opacity 0.8"""
        }
    ]

}