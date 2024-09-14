config = {

    # What color distance function to use, options are "contrast", "delta_e_cie2000" (currently broken)
    "color_distance_function": "contrast",

    # The number of colors including background (color_background), foreground (color_0) and color_{1 - (num_colors-2)}
    "num_colors": 18,

    # How much colors should be rounded, standard is 32, since i felt like it
    "color_rounding": 48,

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

    # How the colors will be organised. Options are None, "pairs" and "pairs_reversed"
    # None doesnt do any kind of organisation
    # "Pairs" will in the case of 18 colors (background, foreground and color{1 - 16}) have a background a color_0 as forground and 16 colors split into pairs, for example 1 and 9, The two colors will be the same except that 1 will be darker
    # "Pairs-reversed" will be the same as "Pairs" but 1 would in the case mentioned before be the lighter color
    # Note that the colors generated when using one of the pair ooption are not compared to the background and may therefore be more difficult to diffirentiate. Because of that my recommendation is to not raise the "organisation_offset" to much
    "organisation": "pairs_reversed",

    # How much lighter the lighter color will be than the darker, based on the l in hsl (0 - 1), this option will only be used when organisation != None
    "organisation_offset": 0.07,


    ##### Currently unavailable
    # When there arent enough colors in the picture or they are too close, generate new colors. Will loop through all the options in the list, the same option can be repeated with different settings
    # Options are "blend", "triad", "like" and "monochromatic"
    # Blend will blend the different colors that it found to varying amounts
    # Triad will take color_0 and rotate 60 deg in both hue directions. Based on those 3 points it will vary hue, saturation and lightness a little to generate enough colors
    # Like will use color_0 as base and select colors by rotating hue a couple of degress in both directions
    # Monochromatic will vary lightness and saturation of color_0 to create different colors
    "generation_options": [
        # {
        #     "name": "triad",
        #     # Wether the triad colors in this option need to follow min distance to bg, this doesnt really matter since for the moment it only uses 120 degs in both directions, hence they should never be close enough
        #     "uses_bg_dist":True,
        #     # Wether the triad colors in this option need to follow min distance to other colors
        #     "uses_other_dist":True
        # },
        {
            "name": "like",
            # Wether the like colors in this option need to follow min distance to bg
            "uses_bg_dist": True,
            # Wether the like colors in this option need to follow min distance to other colors
            "uses_other_dist": True,
            # How much to rotate in each direction per iteration of generation on hsl color wheel
            "deg_incrementation": 20,
            # The biggest amount of rotation allowed in either direction on hsl color wheel
            "max_rotation": 150
        }
    ],

    # How far the color_dist should be from background color, calculated with color_distance_function function in the color_distance.py file
    #"min_dist_to_bg": 48, #Used with delta_e_cie2000 to moderate success
    "min_dist_to_bg": 3.23, # Used with "contrast"

    # Same as to_bg but for other colors
    #"min_dist_to_other": 6, #used with "delta_e_cie2000" to moderate success
    "min_dist_to_other": 0.7, # Used with "contrast"

    # All the options that will be used to prioritize colors in the theme
    "scoring_options":{
        # Will increase the score based on how vibrant a color is i.e how saturated it is and how close to 0.5 in lightness it is.
        "vibrancy": {
            # If it should be used
            "active": True,
            # In what way it will be applied, True for scoring var being used as an exponent and False for scroing var being used as an factor
            "exponential": True,
            "scoring_var": 2.5

        },
        # Scored on how close it is to the inverted background color
        "inverted_bg":{
            "active": False,

            # To get a multiplier to use the scroing_var on we take 1 over the dist to bg from color, but by using min and max builtins we limit what the multiplier can be
            # min_limit is the smallest value that the dist to bg from color can be
            "min_limit": 5,
            # max_limit is the biggest value that the dist to bg from color can be
            "max_limit": 10,

            "exponential": False,
            "scoring_var": 25
        }
    },

    # How big the increases should be on the x-axis when reading the pixels with PILLOW, helps shorted time but will give worse results the bigger it is. Must be int >= 1
    "x_skip": 2,
    # Same but for y axis. Must be int >= 1
    "y_skip": 2,

    # A list of what main.py will output
    "outputs": [
        {
            # Path to file to be outputed into, file will be overwritten
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
        },
        {
            "file_path": "~/Documents/projects/bg_dynamo_codium/themes/bg-dynamo.json",
            "config_text": """{{
    "name": "Bg Dynamo",
    "type": "dark",
    "colors": {{
      "editor.background": "{color_background}",
      "editor.foreground": "{color_0}",
      "editorCursor.foreground": "{color_1}",
      "editor.lineHighlightBackground": "{color_background}",
      "editorLineNumber.foreground": "{color_1}",
      "editor.selectionBackground": "{color_2}",
      "editor.selectionForeground": "{color_background}",
      "editor.inactiveSelectionBackground": "{color_10}",
      "window.activeBorder": "{color_7}",
      "window.inactiveBorder": "{color_15}" ,
      "terminal.background": "{color_background}",
      "terminal.foreground": "{color_0}",
      "statusBar.background": "{color_0}",
      "statusBar.foreground": "{color_background}",
      "sideBar.background": "{color_background}",
      "sideBar.foreground": "{color_0}",

      "tab.activeBackground": "{color_0}",
      "tab.activeForeground": "{color_background}",
      "tab.inactiveBackground": "{color_background}",
      "tab.inactiveForeground": "{color_0}",
      "titleBar.activeBackground": "{color_0}",
      "titleBar.activeForeground": "{color_background}",
      "titleBar.inactiveBackground": "{color_background}",
      "titleBar.inactiveForeground": "{color_0}",
      
      "menu.foreground": "{color_0}",
      "menu.background": "{color_background}",
      "menubar.selectionForeground": "{color_background}",
      "menubar.SelectionBackground": "{color_0}"


    }},
    "workbench.colorCustomizations": {{
      "activityBar.background": "{color_background}",
      "activityBar.foreground": "{color_0}"


    }},
    "tokenColors": [
      {{
        "scope": "comment",
        "settings": {{
          "foreground": "{color_15}",
          "fontStyle": "italic"
        }}
      }},
      {{
        "scope": "string",
        "settings": {{
          "foreground": "{color_3}"
        }}
      }},
      {{
        "scope": "keyword",
        "settings": {{
          "foreground": "{color_2}"
        }}
      }}
    ]
  }}
            
            """
        },
        {
          "file_path": "~/.config/cava/config",
          "config_text": """
[color]

# Gradient mode, only hex defined colors are supported,
# background must also be defined in hex or remain commented out. 1 = on, 0 = off.
# You can define as many as 8 different colors. They range from bottom to top of screen
 gradient = 1
 gradient_count = 8
 gradient_color_1 = '{color_0}'
 gradient_color_2 = '{color_1}'
 gradient_color_3 = '{color_2}'
 gradient_color_4 = '{color_3}'
 gradient_color_5 = '{color_4}'
 gradient_color_6 = '{color_5}'
 gradient_color_7 = '{color_6}'
 gradient_color_8 = '{color_7}'
          """
        }
    ]

}