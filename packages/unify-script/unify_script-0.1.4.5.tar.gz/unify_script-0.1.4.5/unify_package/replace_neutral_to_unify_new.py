import csv
import glob
import os
import re

from unify_package.utils import is_test_file, is_hidden_file, is_build_directory, is_strings_values, \
    ignoredFiles, is_manifest, is_gradle_contains_unify_principle

color_mapper = {}
file = [
    "/Users/nakama/android-tokopedia-core/tkpdseller/src/main/java/com/tokopedia/seller/base/view/activity/BaseToolbarActivity.java"]
re_color_android_compat = 'Color\.WHITE|Color\.BLACK|Color\.LTGRAY|Color\.GRAY|Color\.TRANSPARENT|Color\.BLUE|Color\.RED|Color\.GREEN'
script_dir = os.path.dirname(__file__)  # Script directory
custom_color_mapper_path = os.path.join(script_dir, 'dataset/neutral_to_unify.csv')
current_file = "test"


def find_color_in_line(file_to_refactor):
    file_changes = 0
    p = re.compile(
        'com\.[\w_]+\.[\w_]+\.R\.color\.[\w_]+|R\.color\.\w+|\.color\.\w+|@color/\w+|android.R.color.\w+|@android:color/\w+|Color\.WHITE|Color\.BLACK|Color\.LTGRAY|Color\.GRAY|Color\.TRANSPARENT|Color\.BLUE|Color\.RED|Color\.GREEN')
    for file in file_to_refactor:
        if not is_file_ignored(file):
            global current_file
            current_file = file

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


def replace_with_color_mapper(m):
    global current_file
    replace = m.group(0)
    color_except_full_path = replace
    should_append_full_path = False

    androidColorCompat = re.search(re_color_android_compat, replace)

    if str(replace).startswith("com.") or str(replace).startswith("android."):
        # color_except_full_path -> from com.tokopedia.*.R.color.Unify_N700 to R.color.Unify_N700
        color_except_full_path = re.findall('R.color.\w+', replace)[0]
        should_append_full_path = True
    elif str(replace).startswith("R.color."):
        should_append_full_path = False

    if should_append_full_path:
        try:
            replace = color_mapper[color_except_full_path]
            replace = "com.tokopedia.unifyprinciples." + replace
        except Exception as e:
            e
    elif androidColorCompat:
        # Color.WHITE/Color.BLACK/etcetc
        try:
            if current_file.endswith('Activity.java') or current_file.endswith('Activity.kt'):
                replace = 'androidx.core.content.ContextCompat.getColor(this,' + 'com.tokopedia.unifyprinciples.' + \
                          color_mapper[m.group(0)] + ')'
            else:
                replace = 'androidx.core.content.ContextCompat.getColor(context,' + 'com.tokopedia.unifyprinciples.' + \
                          color_mapper[m.group(0)] + ')'
        except Exception as e:
            pass
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


def replace_neutral_with_unify(path):
    localCount = 0
    localCount += is_gradle_contains_unify_principle(path)
    global color_mapper
    color_mapper = get_color_map()
    localCount += find_color_in_line(traverse_folders(path))
    if localCount > 0:
        is_gradle_contains_unify_principle(path)
    return localCount
