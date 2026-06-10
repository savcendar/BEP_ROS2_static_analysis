import os
import re
import glob

#Get libraries for eahc project
def get_common_libraries(repo_path):
    cpp_search = re.compile(r'#include\s*[<"](.+?)[>"]') #rule for libraries is c++ and hpp files
    py_search = re.compile(r'^(?:from\s+(\S+)|import\s+(\S+))', re.MULTILINE) #rule for libraries in python files
    cpp_libraries = set()
    py_libraries = set()

    for file in glob.glob(repo_path + "/**/*.cpp", recursive = True) + glob.glob(repo_path + "/**/*.hpp", recursive = True):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for lib in cpp_search.findall(f.read()):
                cpp_libraries.add(lib)

    for file in glob.glob(repo_path + "/**/*.py", recursive=True):
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            for imp in py_search.findall(f.read()):
                name = imp[0] if imp[0] else imp[1]
                py_libraries.add(name.split('.')[0])

    return cpp_libraries, py_libraries

#Output results
def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
    project_names = os.listdir(base_path)
    cpp_sets = {}
    py_sets = {}

    for name in project_names:
        project = os.path.join(base_path, name)
        cpp_sets[name], py_sets[name] = get_common_libraries(project)

    #derive common libraries
    common_cpp = set.intersection(*cpp_sets.values())
    common_py = set.intersection(*py_sets.values())

    #terminal output
    print(f"common C++ libraries ({len(common_cpp)}):")
    for lib in sorted(common_cpp):
        print(f"  #include <{lib}>")
    print(f"\ncommon Python libraries ({len(common_py)}):")
    for lib in sorted(common_py):
        print(f"  import {lib}")

if __name__ == "__main__":
    main()
