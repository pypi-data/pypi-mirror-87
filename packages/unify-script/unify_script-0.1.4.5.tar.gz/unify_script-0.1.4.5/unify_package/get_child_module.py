import json
import os
import re


def get_child_module(project_path, module_path):
    dependency_graph = DependencyGraph(project_path)
    return dependency_graph.traverseAllChildDependencies(module_path)


class DependencyGraph:

    def __init__(self, project_path):
        self.results = {}
        self.project_path = project_path
        includes = self.findIncludedModules(project_path)
        self.ext = self.findProjectExt(project_path)
        for i in includes:
            slash = i.replace(':', '/')
            # for features/blabla/blabla
            normed = slash[1:] if os.path.isabs(slash) else slash
            full_path = os.path.join(project_path, normed)
            dep = self.findProjectDependency(full_path)
            dep_path = [self.ext[x] for x in dep]
            key = ":" + normed.replace("/", ":")
            self.results[key] = dep_path

    def findProjectDependency(self, path):
        """
        Return list of object representing the path and name of project dependency that a module implements
        Input path is the path of module we want to find out
        """
        build_path = path + "/build.gradle"
        d = []
        if os.path.exists(build_path):
            with open(build_path) as f:
                contents = f.read()
                pattern = re.compile(
                    r"[Ii]mplementation \(?project\(rootProject\.ext\.(\w+)\.(\w+)\)\)?")
                result = re.finditer(pattern, contents)
                for r in result:
                    d.append(r.group(1) + "/" + r.group(2))
        return d

    def findProjectExt(self, project_path):
        """
        """
        pattern = r"^\s+(\w+)\s*:\s*\"([\w:-]+)\""
        feature_path = project_path + "/buildconfig/dependencies/dependency-features.gradle"
        library_path = project_path + "/buildconfig/dependencies/dependency-libraries.gradle"
        d = {}
        with open(feature_path) as f:
            contents = f.read()
            results = re.finditer(pattern, contents, re.MULTILINE)
            for result in results:
                d["features/" + result.group(1)] = result.group(2)
        with open(library_path) as f:
            contents = f.read()
            results = re.finditer(pattern, contents, re.MULTILINE)
            for result in results:
                d["libraries/" + result.group(1)] = result.group(2)
        return d

    def findIncludedModules(self, path):
        pathList = [
            path + "/buildconfig/appcompile/compile-customerapp.gradle",
            path + "/buildconfig/appcompile/compile-sellerapp.gradle",
            path + "/buildconfig/appcompile/compile-libraries.gradle"
        ]
        pattern = r'^include [\'\"]([\w:\-_]+)[\'\"]'
        d = set()

        for p in pathList:
            with open(p) as f:
                contents = f.read()
                results = re.finditer(pattern, contents, re.MULTILINE)
                for result in results:
                    d.add(result.group(1))
        return list(d)

    def constructDependencyGraph(self):
        print(json.dumps(self.results, indent=4))

    def traverse(self, path, visited=[]):
        visited += [path]
        for neighbor in self.results[path]:
            if neighbor not in visited:
                visited = self.traverse(neighbor, visited)
        return visited

    def isCommented(self, line):
        comment_rgx = re.compile(r'\s*//')
        if re.search(comment_rgx, line):
            return True
        else:
            return False

    def traverseAllChildDependencies(self, module_path):
        module_key = ":" + module_path.replace("/", ":")
        result = self.traverse(module_key)
        return result
