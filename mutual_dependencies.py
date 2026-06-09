import os
import xml.etree.ElementTree as ET
import pandas as pd
import glob
import matplotlib.pyplot as plt
from collections import Counter

#Get shaped dependencies across 3 projects
def get_shared_dependencies(superfolder):
    #identify internal packages to later exclude from analysis
    internal_dependencies = set()
    xml_files = glob.glob(superfolder + "/**/package.xml", recursive = True)
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        name = tree.find('name')
        if name is not None:
            internal_dependencies.add(name.text.strip())

    project_dependencies = {} #dictionary for projects and their dependencies

    #for each project, find external dependencies 
    for project_directory in os.listdir(superfolder):
        project = os.path.join(superfolder, project_directory)
        project_xml_files = glob.glob(project + "/**/package.xml", recursive = True)
        external_dependencies = set()
        dependency_types = ['depend', 'build_depend', 'exec_depend', 'test_depend', 'build_export_depend']
        
        for xml_file in project_xml_files:
            tree = ET.parse(xml_file)
            for dependency_type in dependency_types:
                for dependency in tree.getroot().findall(dependency_type):
                    if dependency.text:
                        dependency_name = dependency.text.strip()
                        if dependency_name not in internal_dependencies: 
                            external_dependencies.add(dependency_name) #add only if dependency is not found in internal
        project_dependencies[project] = external_dependencies

    #find dependencies in common and count them
    #find dependencies in common and count them
    shared_dependencies = set.intersection(*project_dependencies.values()) 
    counts = {}
    for xml_file in xml_files:
        tree = ET.parse(xml_file)
        for type in dependency_types:
            for dependency in tree.getroot().findall(type):
                if dependency.text:
                    name = dependency.text.strip()
                    if name in shared_dependencies:
                        if name not in counts:
                            counts[name] = 0
                        counts[name] += 1

    return counts, sorted(list(shared_dependencies))

#Output results
def main():
    repos_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
    counts, shared_dependencies = get_shared_dependencies(repos_path)
    
    #terminal output
    print(f"dependencies across all 3 projects:")
    for dep in shared_dependencies:
        print(f"{dep}")

    #visual output
    df = pd.DataFrame(counts.items(), columns=['Dependency', 'Count']).sort_values(by='Count', ascending=False)
    num_total_deps = len(df)
    plt_height = max(6, num_total_deps * 0.5)
    plt.figure(figsize=(14, plt_height))
    plt.barh(df['Dependency'], df['Count'], color='#87CEEB', edgecolor='black')
    plt.xlabel('Total occurence')
    plt.title(f'Mutual dependencies across Franka, UR, and MoveIt2 projects')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    for i, v in enumerate(df['Count']):
        plt.text(v + 0.1, i, str(v), va='center', fontweight='bold')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
