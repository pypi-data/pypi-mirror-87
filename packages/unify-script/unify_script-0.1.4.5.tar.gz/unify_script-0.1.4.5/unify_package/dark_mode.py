import os
import sys
from pathlib import Path

from find_gradle_file import get_mapper_all_colors
from utility.change_style_theme_with_unify_day_night import change_style_theme_with_unify_day_night
from utility.get_child_module import get_child_module
from utility.replace_color_with_all_dependency import replace_color_with_all_dependency
from utility.replace_hardcode_color_with_unify import replace_hardcode_color_with_unify
from utility.replace_neutral_with_unify import replace_color_with_neutral
from utility.replace_custom_color_with_unify import replace_custom_color_with_unify


def main(root_path, module_path):
    get_mapper_all_colors(root_path)
    change_style_theme_with_unify_day_night(root_path + os.sep + module_path)
    replace_color_with_all_dependency(root_path, module_path)


def process_arguments():
    root_path = ""
    module_path = ""

    try:
        root_path = sys.argv[1]
    except:
        print("Please provide android tokopedia root path")
        pass

    try:
        module_path = sys.argv[2]
    except:
        print("Please provide module absolute path")

    if root_path != "" and module_path != "":
        main(root_path, module_path)
    else:
        print("Failed...")


if __name__ == '__main__':
    process_arguments()
