from unify_package.find_gradle_file import get_mapper_all_colors
from unify_package.ignore_module import ignoreModule
from unify_package.get_child_module import get_child_module
from unify_package.replace_custom_color_with_unify import replace_custom_color_with_unify
from unify_package.replace_hardcode_color_with_unify import replace_hardcode_color_with_unify
from unify_package.replace_neutral_to_unify_new import replace_neutral_with_unify


def replace_color(project_path, module_path):
    get_mapper_all_colors(project_path)
    result = get_child_module(project_path, module_path)
    filtered_result = (s for s in result if not any(e in s for e in ignoreModule))
    count = 0
    for r in filtered_result:
        p = project_path + r.replace(":", "/")
        count += replace_neutral_with_unify(p)
        count += replace_custom_color_with_unify(p)
        count += replace_hardcode_color_with_unify(p)
    print(module_path + ": " + str(count) + " file changes")


if __name__ == "__main__":
    # replace_color(sys.argv[1], sys.argv[2])
    replace_color('/Users/nakama/IdeaProjects/android-tokopedia-core', 'features/discovery/home_wishlist')