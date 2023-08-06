import csv
import glob
import os
import re

from unify_package.utils import is_test_file, is_hidden_file, is_build_directory, is_strings_values, \
    ignoredFiles, is_manifest

color_mapper = {}
script_dir = os.path.dirname(__file__)  # Script directory
custom_color_mapper_path = os.path.join(script_dir, 'dataset/FinalCustomColor.csv')


def find_color_in_line(file_to_refactor):
    file_changes = 0
    p = re.compile(
        'com\.[\w_]+\.[\w_]+\.R\.color\.[\w_]+|R\.color\.\w+|@color/\w+|android.R.color.\w+|@android:color/\w+')
    for file in file_to_refactor:
        if not is_file_ignored(file):
            with open(file) as f:
                data = f.read()
                target_data = data
                new_data = p.sub(replace_with_color_mapper, target_data)
                is_new_data = 1 if new_data != data else 0
            f.close()

            if is_new_data == 1:
                file_changes += 1
                with open(file, 'wt') as f:
                    f.write(new_data)
                f.close()
    return file_changes


def regex_find_color(color):
    if color.startswith("@color/"):
        return color
    else:
        return r'com.*' + color + '\b|' + color + '\b'


def replace_with_color_mapper(m):
    replace = m.group(0)
    color_except_full_path = replace
    should_append_full_path = False

    if str(replace).startswith("com.") or str(replace).startswith("android."):
        color_except_full_path = re.findall('R.color.\w+', replace)[0]
        should_append_full_path = True
    elif str(replace).startswith("R.color."):
        should_append_full_path = True

    if should_append_full_path:
        try:
            replace = color_mapper[color_except_full_path]
            replace = "com.tokopedia.unifyprinciples." + replace
        except Exception as e:
            e
    else:
        try:
            replace = color_mapper[m.group(0)]
        except:
            pass

    return replace


def get_color_map():
    colors = {}
    with open(custom_color_mapper_path) as mapping_classes:
        csv_reader = csv.reader(mapping_classes)
        for idx, class_map in enumerate(csv_reader):
            old_color = class_map[0]
            new_color = class_map[1]
            colors[old_color] = new_color
    return colors


def is_dir_ignored(file_path):
    if (
            is_test_file(file_path) or
            is_hidden_file(file_path) or
            is_build_directory(file_path) or
            is_strings_values(file_path) or
            is_manifest(file_path)
    ):
        return True
    for ignored_file in ignoredFiles:
        if file_path.endswith(ignored_file):
            return True
    return False


def get_file_path(project_path, file):
    return project_path + "/" + file


def is_file_ignored(file_path):
    return is_dir_ignored(file_path)


def traverse_folders(project_path):
    files = glob.glob(project_path + "/src/**/*.xml", recursive=True) + glob.glob(project_path + "/src/**/*.kt", recursive=True) + glob.glob(
        project_path + "/src/**/*.java", recursive=True)
    return files


def is_gradle_contains_unify_principle(rootPath):
    try:
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
            with open(gradle_path, 'wt') as file:
                file.write(data)
            file.close()
    except FileNotFoundError:
        return


def replace_custom_color_with_unify(path):
    global color_mapper
    color_mapper = get_color_map()
    return find_color_in_line(traverse_folders(path))
