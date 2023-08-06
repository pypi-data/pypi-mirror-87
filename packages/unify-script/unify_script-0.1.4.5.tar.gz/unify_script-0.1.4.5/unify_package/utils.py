import csv
import fileinput
import os
import re
import sys
from pathlib import Path

ignoredFiles = [
    ".iml",
    ".pro",
    ".jar",
    ".bat",
    ".js",
    ".yml",
    ".txt",
    ".so",
    ".bundle",
    ".meta",
    ".properties",
    ".json",
    ".apk",
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".aar",
    ".class",
    ".textClipping",
    ".keystore",
    ".lock",
    ".ttf",
    ".py",
    ".hprof",
    "yarn",
    "/raw",
    "BUCK",
    "gradlew",
    "buck-out",
    "CODEOWNERS",
    "aars",
    "buckhelper",
    "buckw",
    "build.gradle",
    "gradle",
    ".webp",
    "dimens.xml",
    "styles.xml"
]

path = Path(os.getcwd())
color_mapper_file = path.parent.__str__() + "/color+moveresource/dataset/neutral_to_unify.csv"
color_custom_mapper_file = path.parent.__str__() + "/dataset/color_util_dataset/FinalCustomColor.csv"


def is_colors_res(file_path):
    return file_path.endswith("colors.xml")


def is_hidden_file(relative_path):
    file_name = os.path.basename(relative_path)
    return file_name.startswith(".")


def is_test_file(file_path):
    return file_path.endswith("androidTest")


def is_build_directory(relative_path):
    return relative_path.find("/androidTest/") != -1 or relative_path.find("/test/") != -1


def is_model_directory(relative_path):
    return relative_path.find("/model/") != -1 or relative_path.find("/models/") != -1


def is_drawable_file(relative_path):
    return re.search(r"/res/drawable", relative_path)


def is_colors_values(relative_path):
    return re.search(r"/res/values.+colors", relative_path)
    pass


def is_strings_values(relative_path):
    return re.search(r"/res/values.+strings", relative_path)
    pass


def is_manifest(relative_path):
    return re.search(r"AndroidManifest.xml", relative_path)
    pass


def is_vector_file(relative_path):
    with open(relative_path) as file:
        is_need_to_append = '</vector>' in file.read()
    return is_need_to_append


def is_dir_ignored(project_path, file_path):
    relative_path = file_path.replace(project_path, "")
    if (
            is_test_file(file_path) or
            is_hidden_file(relative_path) or
            is_build_directory(relative_path) or
            is_strings_values(relative_path)
    ):
        return True
    for ignored_file in ignoredFiles:
        if relative_path.endswith(ignored_file):
            return True
    return False


def get_file_path(project_path, file):
    return project_path + "/" + file


def is_file_ignored(project_path, file_path):
    return is_dir_ignored(project_path, file_path)


def generateCompleteColorMap(source_csv_file, new_csv_file):
    print("asd")
    with open(new_csv_file, 'w',
              newline='') as myfile:
        for line in open(source_csv_file):
            print(line)
            split_line = line.split(',')
            color_key = 'R.color.' + split_line[0]
            color_key_value = 'R.color.' + split_line[1].strip()
            color_key_xml = '@color/' + split_line[0]
            color_key_xml_value = '@color/' + split_line[1].strip()

            writer = csv.writer(myfile)
            writer.writerow([color_key, color_key_value])
            writer.writerow([color_key_xml, color_key_xml_value])


def is_gradle_contains_unify_principle(rootPath):
    try:
        count = 0
        unify_principle_dependencies = "implementation rootProject.ext.unifyDependencies.principles"
        gradle_path = rootPath + os.sep + "build.gradle"
        is_appended = False
        with open(gradle_path) as file:
            is_need_to_append = unify_principle_dependencies not in file.read()

        data = ""
        with open(gradle_path) as file:
            for f in file:
                no_space = f.replace(" ", "")
                if no_space.startswith("implementation") and not is_appended and is_need_to_append:
                    data = data + "\t" + unify_principle_dependencies + os.linesep
                    is_appended = True
                data = data + f
        file.close()

        if is_appended:
            count += 1
            with open(gradle_path, 'wt') as file:
                file.write(data)
            file.close()
        return count
    except FileNotFoundError:
        return

# generateCompleteColorMap()
