import csv
import re
import os
import numpy as np
import webcolors
from scipy import spatial


# pt = [221, 182, 137, 255]  # = "burlywood","#DEB887"]
# pt = [0, 102, 109, 255]  # = "burlywood","#DEB887"]


def find_hex_color(hex_color):
    hex_color = hex_color.rstrip('\n')

    if hex_color == "#000000":
        return "Unify_N700"
    elif hex_color == "#8000":
        return "Unify_P500"
    elif hex_color == "#000000":
        return "Unify_N700"
    elif hex_color == "#00000000":
        return hex_color
    elif re.match("#(.*)000000", hex_color):
        if len(hex_color) == 9:
            hex_color = hex_color[:3] + "31353B"
        else:
            hex_color = hex_color[:2] + "31353B"
    hex_color = hex_color.replace(" ","")
    HexNameDict = {}
    script_dir = os.path.dirname(__file__)  # Script directory
    color_mapper_file = os.path.join(script_dir, 'dataset/rgb_dataset.csv')
    with open(color_mapper_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        rgb = []
        rgba = []
        for row in csv_reader:
            rgb.append([int(row[2]), int(row[3]), int(row[4])])
            rgba.append([int(row[2]), int(row[3]), int(row[4]), int(row[5])])
            HexNameDict[row[1]] = row[0]
        RGB = np.array(rgb)
    try:
        hex_color_rgb = webcolors.hex_to_rgb(hex_color)
        alpha = 255
    except ValueError:
        new_hex = "#" + format(hex_color[3:])
        alpha_hex = hex_color[1:3]
        hex_color_rgb = webcolors.hex_to_rgb(new_hex)
        alpha = int(alpha_hex, 16)

    pt = [hex_color_rgb.red, hex_color_rgb.green, hex_color_rgb.blue]
    # Lookup color name using Hex:ColorName dictionary:
    nearest = spatial.KDTree(RGB).query(pt)
    NearestRGB = (RGB[nearest[1]])

    if alpha != 255:
        # special case with alpha
        # find nearest alpha
        pt = [hex_color_rgb.red, hex_color_rgb.green, hex_color_rgb.blue, alpha]
        colors = []
        for row in rgba:
            if row[0] == pt[0] and row[1] == pt[1] and row[2] == pt[2]:
                colors.append(row)
        if len(colors) > 1:
            RGBA = np.array(colors)
            nearest_alpha = (RGBA[spatial.KDTree(RGBA).query(pt)[1]])
            if nearest_alpha[3] != 255:
                s = '#' \
                    + format(nearest_alpha[3], 'x').zfill(2) \
                    + format(nearest_alpha[0], 'x').zfill(2) \
                    + format(nearest_alpha[1], 'x').zfill(2) \
                    + format(nearest_alpha[2], 'x').zfill(2)
            else:
                s = '#' \
                    + format(nearest_alpha[0], 'x').zfill(2) \
                    + format(nearest_alpha[1], 'x').zfill(2) \
                    + format(nearest_alpha[2], 'x').zfill(2)
            ColorHex = s.upper()
            ColorDiff = \
                '(' + '{0:+d}'.format(nearest_alpha[3] - pt[3]) \
                + ',' + '{0:+d}'.format(nearest_alpha[0] - pt[0]) \
                + ',' + '{0:+d}'.format(nearest_alpha[1] - pt[1]) \
                + ',' + '{0:+d}'.format(nearest_alpha[2] - pt[2]) \
                + ')'
        else:
            s = '#' \
                + format(NearestRGB[0], 'x').zfill(2) \
                + format(NearestRGB[1], 'x').zfill(2) \
                + format(NearestRGB[2], 'x').zfill(2)
            ColorHex = s.upper()
            ColorDiff = \
                '(' + '{0:+d}'.format(NearestRGB[0] - pt[0]) \
                + ',' + '{0:+d}'.format(NearestRGB[1] - pt[1]) \
                + ',' + '{0:+d}'.format(NearestRGB[2] - pt[2]) \
                + ')'
            nearest_alpha = NearestRGB
        try:
            ColorName = HexNameDict[ColorHex]
        except:
            ColorName = ""

        # print('Nearest color name to input RGB '
        #       + str(pt)
        #       + '(' + hex_color + ')'
        #       + ' is "' + ColorName + '"'
        #       + ' ' + ColorHex
        #       + ' ' + str(nearest_alpha)
        #       + ', ' + ColorDiff
        #       + '.')
        return ColorName

    else:
        s = '#' \
            + format(NearestRGB[0], 'x').zfill(2) \
            + format(NearestRGB[1], 'x').zfill(2) \
            + format(NearestRGB[2], 'x').zfill(2)
        ColorHex = s.upper()
        ColorDiff = \
            '(' + '{0:+d}'.format(NearestRGB[0] - pt[0]) \
            + ',' + '{0:+d}'.format(NearestRGB[1] - pt[1]) \
            + ',' + '{0:+d}'.format(NearestRGB[2] - pt[2]) \
            + ')'
        try:
            ColorName = HexNameDict[ColorHex]
        except:
            ColorName = ""

        print('Nearest color name to input RGB '
              + str(pt)
              + '(' + hex_color + ')'
              + ' is "' + ColorName + '"'
              + ' ' + ColorHex
              + ' ' + str(NearestRGB)
              + ', ' + ColorDiff
              + '.')
        return ColorName

# print(find_hex_color("#AF3E14"))
find_hex_color("#009688")