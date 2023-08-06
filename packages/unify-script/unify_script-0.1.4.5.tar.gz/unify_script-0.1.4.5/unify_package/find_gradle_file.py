import csv
import fileinput
import os
import re
import sys

from unify_package.find_nearest_hex_color import find_hex_color

ignoredFiles = ["pre_release_inspector"]
project_location = "/Users/nakama/android-tokopedia-core"
unify_principle_dependencies = "implementation rootProject.ext.unifyDependencies.principles"
color_mapper_file = os.path.dirname(__file__) + "/dataset/color-mapper.csv"

# class name starts with _ is a utility class
YOUR_DATA_MAPPER_STEP2_PATH = os.path.dirname(__file__) + "/dataset/"
raw_custom_color = YOUR_DATA_MAPPER_STEP2_PATH + "_RawCustomColor.txt"
unreference_custom_color = YOUR_DATA_MAPPER_STEP2_PATH + "_UnreferenceCustomColor.txt"
unique_custom_color = YOUR_DATA_MAPPER_STEP2_PATH + "_UniqueCustomColor.txt"
final_custom_color = YOUR_DATA_MAPPER_STEP2_PATH + "_FinalCustomColor.txt"
raw_colors_gradle_path = YOUR_DATA_MAPPER_STEP2_PATH + "_RawColorsGradlePath.txt"
# ================================================================================================================#

list_of_path_custom_colors = []

totalColorFound = 0
totalColorNotFound = 0
totalValueColorNotFound = 0
totalModuleScan = 0
totalGradleNotContainsPrinciple = 0


def is_root_folder(filePath):
    root_file = None
    if any(File.endswith(".gradle") for File in os.listdir(filePath)):
        root_file = filePath
    return root_file


def get_file_path(project_location, file):
    return project_location + "/" + file


def traverse_color_res(project_location, current_location):
    global totalModuleScan
    files = os.listdir(current_location)
    files.sort()
    for file in files:
        file_path = get_file_path(current_location, file)

        if os.path.isdir(file_path):
            root_path = is_root_folder(file_path)
            if root_path:
                totalModuleScan += 1
                # find_string_color(root_path)
                values_folder_found(root_path)
            else:
                traverse_color_res(project_location, file_path)


def find_string_color(root_path):
    global totalColorFound
    global totalColorNotFound
    global totalValueColorNotFound
    try:
        values_path = root_path + os.sep + 'src/main/res/values'
        colors_path_re = "strings.xml"

        if any(re.match(colors_path_re, File) for File in os.listdir(values_path)):
            for file_name in os.listdir(values_path):
                if re.match(colors_path_re, file_name):
                    path = values_path + "/" + file_name
                    new_color_target = []
                    new_file = []
                    with open(path, 'r+') as f:

                        for line in f:
                            no_space = line.replace(" ", "")
                            if no_space.startswith('<color'):
                                new_color_target.append(line)
                                totalColorFound += 1
                            else:
                                new_file.append(line)

                        f.seek(0)
                        for line in new_file:
                            f.write(line)
                        f.truncate()
                    f.close()

                    migrate_string_color_to_color_file(values_path, new_color_target)

                    list_of_path_custom_colors.append(file_name + os.sep + values_path)
        else:
            totalColorNotFound += 1
    except FileNotFoundError:
        totalValueColorNotFound += 1


def migrate_string_color_to_color_file(root_path, values):
    if len(values) == 0:
        return
    colors_path = root_path + "/" + "colors.xml"
    data = ""
    is_appended = False
    with open(colors_path) as file:
        for f in file:
            no_space = f.replace(" ", "")
            if no_space.startswith("<color") and not is_appended:
                for line in values:
                    data = data + line
                is_appended = True
                data = data + f
            else:
                data = data + f
    file.close()
    if data == "":
        data = data + '<?xml version="1.0" encoding="utf-8"?>'
        data = data + "<resources>"
        for line in values:
            data = data + line
        data = data + "</resources>"
    with open(colors_path, 'wt') as file:
        file.write(data)
    file.close()


def values_folder_found(rootPath):
    global totalColorFound
    global totalColorNotFound
    global totalValueColorNotFound
    if os.path.basename(os.path.normpath(rootPath)) in ignoredFiles:
        return
    try:
        colors_path = rootPath + os.sep + 'src/main/res/values'
        colors_path_re = "(.*?color.*?).xml"

        if any(re.match(colors_path_re, File) for File in os.listdir(colors_path)):
            is_gradle_contains_unify_principle(rootPath)
            for colorsFile in os.listdir(colors_path):
                if re.match(colors_path_re, colorsFile):
                    totalColorFound += 1
                    list_of_path_custom_colors.append(colors_path + os.sep + colorsFile)
        else:
            totalColorNotFound += 1
    except FileNotFoundError:
        totalValueColorNotFound += 1


def is_colors_xml_exist(colors_path_re, colors_path):
    any(re.match(colors_path_re, File) for File in os.listdir(colors_path))


def get_all_custom_color():
    with open(raw_custom_color, "w") as combineFile:
        for filePath in list_of_path_custom_colors:
            with open(filePath) as f:
                for line in f:
                    no_space = line.replace(" ", "")
                    if no_space.startswith('<color'):
                        color_name = re.findall('name="(.*)"', line.lstrip())
                        color_hex = re.findall('>(.*)</', line.lstrip())[0]

                        if color_hex.startswith("@android:color/"):
                            if color_hex == "@android:color/black":
                                change_color = "#000000"
                            elif color_hex == "@android:color/white":
                                change_color = "#ffffff"
                            elif color_hex == "@android:color/transparent":
                                change_color = "#00000000"

                            combineFile.write(color_name[0] + ',' + change_color + '\n')
                        else:
                            combineFile.write(color_name[0] + ',' + color_hex + '\n')
            f.close()
    combineFile.close()


def remove_transparent_and_dark_mode_support():
    for line in fileinput.input(raw_custom_color, inplace=1):
        hex_value = line.split(',')[1]
        color_name = line.split(',')[0]

        #If color in module is dark mode support custom color, remove from mapper
        if "dark_mode_support" in color_name:
            continue

        if "#00000000" not in hex_value:
            sys.stdout.write(line)


""
'Sometimes the color is reference to other colors eg: <color name=first_green>@color/medium_green</color>'
'Here we need to change the reference color into hex color like <color name=first_green>#42b549</color>'
""
def change_hardcoded_reference_color():
    uniqueColorFile = open(unreference_custom_color, 'w')
    for line in open(unique_custom_color, 'r'):
        line_split = line.split(',')
        color_hex = line_split[1]

        # color_red_main,@color/red_primary
        color_contains_another_reference = color_hex.startswith('@color')

        if color_contains_another_reference:
            hex_by_color_reference = find_reference_color(color_hex)
            if hex_by_color_reference:
                uniqueColorFile.write(line.replace(color_hex, hex_by_color_reference))
            else:
                # maybe the color is already unify reference
                color_unify = find_reference_in_unify_principle(color_hex)
                if color_unify:
                    uniqueColorFile.write(line.replace(color_hex, color_unify))
                else:
                    uniqueColorFile.write(line)
        else:
            uniqueColorFile.write(line)


def generate_color_resource():
    # _RawCustomColor.txt
    get_all_custom_color()
    remove_transparent_and_dark_mode_support()

    # _RawColorsGradlePath
    create_color_path()

    # _UniqueCustomColor
    remove_duplicate()

    # _UnreferenceCustomColor
    change_hardcoded_reference_color()

    # _FinalCustomColor
    change_value_hex_to_unify()
    remove_null_value()
    adjustUnifyAttribute()

    # FinalCustomColor
    convertFinalColorToCsv()


def remove_null_value():
    for line in fileinput.input(final_custom_color, inplace=1):
        if "null" not in line:
            sys.stdout.write(line)


def convertFinalColorToCsv():
    with open(final_custom_color, 'r') as infile, open(
            YOUR_DATA_MAPPER_STEP2_PATH + "FinalCustomColor.csv", 'w') as outfile:
        stripped = (line.strip() for line in infile)
        lines = (line.split(",") for line in stripped if line)
        writer = csv.writer(outfile)
        writer.writerows(lines)


# Change to R.color.white, Unify_n0
# Into R.color.white, R.color.Unify_n0
def adjustUnifyAttribute():
    for line in fileinput.input(final_custom_color, inplace=1):
        split_line = line.split(',')
        color_name = split_line[0]
        color_unify = split_line[1]

        if "@color/" not in color_unify:
            sys.stdout.write('R.color.' + color_name + ',R.color.' + color_unify)
            sys.stdout.write('@color/' + color_name + ',@color/' + color_unify)
        else:
            sys.stdout.write('R.color.' + color_name + ',R.color.' + color_unify.split("/")[1])
            sys.stdout.write('@color/' + color_name + ',' + color_unify)

    fileinput.close()


def create_color_path():
    with open(raw_colors_gradle_path, "w") as colorsPath:
        for idx, line in enumerate(list_of_path_custom_colors):
            if idx != 0 & idx != len(list_of_path_custom_colors):
                colorsPath.write("\n")
            colorsPath.write(line)
    colorsPath.close()


def remove_duplicate():
    lines_seen = set()  # holds lines already seen
    outfile = open(unique_custom_color, "w")
    for line in open(raw_custom_color, "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()


def change_value_hex_to_unify():
    finalFile = open(final_custom_color, "w")
    for line in open(unreference_custom_color, "r"):
        line_split = line.split(',')
        try:
            finalFile.write(line_split[0] + ',' + find_hex_color(line_split[1]) + '\n')
        except:
            finalFile.write(line)


def find_reference_in_unify_principle(color_hex):
    color_hex = color_hex.rstrip("\n")
    with open(color_mapper_file) as mapping_classes:
        csv_reader = csv.reader(mapping_classes)
        for class_map in csv_reader:
            if color_hex == class_map[0]:
                return class_map[1]
    mapping_classes.close()


def find_reference_color(color_match):
    with open(unique_custom_color, 'r') as f:
        lines = f.readlines()
        color_match = color_match.rstrip('\n')
        for line in lines:
            color_name = line.split(',')[0]
            color_without_attribute = color_match.replace('@color/', '')

            if color_without_attribute == color_name:
                color_hex = line.split(',')[1]
                return color_hex


def is_gradle_contains_unify_principle(rootPath):
    global totalGradleNotContainsPrinciple
    gradle_path = rootPath + os.sep + "build.gradle"
    with open(gradle_path, "r") as f:
        if unify_principle_dependencies in f.read():
            totalGradleNotContainsPrinciple += 0
        else:
            totalGradleNotContainsPrinciple += 1
    f.close()


def get_unify_resource():
    for line in fileinput.input(color_mapper_file, inplace=1):
        color_name = re.findall('name="(.*)"', line.lstrip())
        color_hex = re.findall('>(.*)</', line.lstrip())
        sys.stdout.write(color_name[0] + ',' + color_hex[0] + '\n')


def get_mapper_all_colors(root_tokped_path):
    traverse_color_res(root_tokped_path, root_tokped_path)
    generate_color_resource()

