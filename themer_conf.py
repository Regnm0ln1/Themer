config = {
    # The number of colors including background, foreground and color0-15
    "num_colors": 18,

    # How much colors should be rounded, standard is 32, since i felt like it
    "color_rounding": 32,
    # Can be "auto", hoping to add "light" and "dark" in future
    "mode": "auto",

    # How far the color_dist should be from background color, calculated with delta_e_cie2000 function
    "min_dist_to_bg": 35,

    # Same as to_bg but for other colors
    "min_dist_to_other": 0,

    # The power that is used in scoring function, higher scoring_pow means the function will prioritize more "vibrant" more when choosing colors
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
background_opacity 0.8"""
        }
    ]

}