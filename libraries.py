import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import glob

#Get libraries and their count for all projects
def get_libraries(repo_path):
    cpp_search = re.compile(r'#include\s*[<"](.+?)[>"]') #searching rules for c++ and hpp files
    py_search = re.compile(r'^(?:from\s+(\S+)|import\s+(\S+))', re.MULTILINE) #searching rules for python files
    cpp_libraries = set() 
    py_libraries = set()
    cpp_files = glob.glob(repo_path + "/**/*.cpp", recursive = True) + glob.glob(repo_path + "/**/*.hpp", recursive = True)
    py_files = glob.glob(repo_path + "/**/*.py", recursive = True)

    #find all libraries for c++ and hpp files
    for file in cpp_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for lib in cpp_search.findall(content):
                cpp_libraries.add(lib)

    #find all libraries for python files
    for file in py_files:
        with open(file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for imp in py_search.findall(content):
                name = imp[0] if imp[0] else imp[1]
                py_libraries.add(name.split('.')[0])

    return len(cpp_libraries), len(py_libraries)
  
#Output results
def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
    project_names = os.listdir(base_path)
    cpp_counts = []
    py_counts = []

    #for each project, make a terminal output 
    for name in project_names:
        project = os.path.join(base_path, name)
        cpp_count, py_count = get_libraries(project)
        cpp_counts.append(cpp_count)
        py_counts.append(py_count)
        print(f"{name}: C++ - {cpp_count}, Python - {py_count}, Total: {cpp_count + py_count}")
        
    #visual output
    x = np.arange(len(project_names))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, cpp_counts, width, label='C++ Libraries', color='#87CEEB', edgecolor='black')
    rects2 = ax.bar(x + width/2, py_counts, width, label='Python Libraries', color='#FF69B4', edgecolor='black')
    ax.set_ylabel('Count')
    ax.set_title('Libraries per project')
    ax.set_xticks(x)
    ax.set_xticklabels(project_names)
    ax.legend()
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    plt.tight_layout()
    plt.show()
    
if __name__ == "__main__":
    main()
