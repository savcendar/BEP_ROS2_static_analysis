import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import glob

#Get dependencies for each project and their count
def get_dependencies(superfolder):
    #identify internal packages to later exclude from analysis
    internal_dependencies = set()
    xml_files = glob.glob(superfolder + "/**/package.xml", recursive = True)
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        name = tree.find('name')
        if name is not None:
            internal_dependencies.add(name.text.strip())

    project_dependencies = {} #dictionary for projects and their dependencies
    counts = {} #dictionary for projects and count of dependencies
    total_count = set()
    
    #get dependencies for each project and their count
    for project_directory in os.listdir(superfolder):
        project = os.path.join(superfolder, project_directory)
        project_counts = {} #dependency count per project
        project_xml_files = glob.glob(project + "/**/package.xml", recursive = True)

        for xml_file in project_xml_files:
            tree = ET.parse(xml_file)
            dependency_types = ['depend', 'build_depend', 'exec_depend', 'test_depend', 'build_export_depend']
            for type in dependency_types:
                for dependency in tree.getroot().findall(type):
                    if dependency.text:
                        dependency_name = dependency.text.strip()
                        #exclude internal dependencies
                        if dependency_name not in internal_dependencies:
                            if dependency_name not in project_counts:
                                project_counts[dependency_name] = 0
                            project_counts[dependency_name] += 1
                            total_count.add(dependency_name)
        
        project_dependencies[project_directory] = project_counts
        counts[project_directory] = len(project_counts)
        
    return project_dependencies, counts, len(total_count)

#Output results
def main():
    path_to_repos = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
    project_dependencies, counts, total_count = get_dependencies(path_to_repos)
    
    #terminal output
    print(f"total unique dependencies: {total_count}")
    for project in counts.keys():
        print(f"{project}:")
        print(f"External Dependencies: {counts[project]}")

    #visual output
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    colors = ['#FF69B4', '#87CEEB', '#9370DB']
    project_names = sorted(project_dependencies.keys())[:3]
    for i, name in enumerate(project_names):
        df = pd.DataFrame(project_dependencies[name].items(), columns=['Dep', 'Freq']).sort_values(by='Freq', ascending=False).head(5)
        axes[i].barh(df['Dep'], df['Freq'], color=colors[i], edgecolor='black')
        axes[i].set_title(f"{name}\nDependencies: {counts[name]} ", fontsize=11, fontweight='bold')
        axes[i].invert_yaxis()
        axes[i].grid(axis='x', linestyle='--', alpha=0.4)
    plt.suptitle('Top 5 External Dependencies per Project', fontsize=16)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == "__main__":
    main()
