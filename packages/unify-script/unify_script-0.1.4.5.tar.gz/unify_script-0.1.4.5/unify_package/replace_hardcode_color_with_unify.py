import glob
import os
import re

from unify_package.find_nearest_hex_color import find_hex_color
from unify_package.utils import is_test_file, is_hidden_file, is_build_directory, is_strings_values, \
    ignoredFiles, is_manifest, is_model_directory, is_vector_file, is_colors_res


def find_color_in_line(file_to_refactor):
    file_changes = 0
    _hex_colour = re.compile(r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b')
    for file in file_to_refactor:
        if not is_file_ignored(file):
            with open(file) as f:
                data = f.read()
                target_data = data
                new_data = _hex_colour.sub(replace_with_color_mapper, target_data)
                is_new_data = 1 if new_data != data else 0
            f.close()

            if is_new_data == 1:
                file_changes += 1
                with open(file, 'wt') as f:
                    f.write(new_data)
                f.close()
    return file_changes


def replace_with_color_mapper(m):
    if m.group(0) == "#00000000":
        return m[0]
    replace = find_hex_color(m.group(0))
    if str(replace).startswith("R.color."):
        replace = "com.tokopedia.unifyprinciples.R." + replace
    else:
        replace = "@color/" + replace
    return replace


def is_dir_ignored(file_path):
    if (
            is_colors_res(file_path) or
            is_test_file(file_path) or
            is_hidden_file(file_path) or
            is_build_directory(file_path) or
            is_model_directory(file_path) or
            is_strings_values(file_path) or
            is_vector_file(file_path) or
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
    files = glob.glob(project_path + "/src/**/*.xml", recursive=True)
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


def replace_hardcode_color_with_unify(path):
    return find_color_in_line(traverse_folders(path))
