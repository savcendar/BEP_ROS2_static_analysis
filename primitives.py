import os
import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import glob

#Get primitives (topics, services and actions) for each topic
def get_primitives(project_path):
    primitives = {
        'msg': 0,
        'srv': 0,
        'action': 0
    }
    #count all primitive files appearing per project
    primitives['msg'] = len(glob.glob(project_path + "/**/*.msg", recursive = True))
    primitives['srv'] = len(glob.glob(project_path + "/**/*.srv", recursive = True))
    primitives['action'] = len(glob.glob(project_path + "/**/*.action", recursive = True))
    
    return primitives

#Output results
def main():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../repos'))
    projects = os.listdir(base_path)
    data_frame = []

    for project in projects: #for each project, output primitive information and append it to dataframe
        path = os.path.join(base_path, project)
        project_primitives = get_primitives(path)
        print(f"{project} has: topics - {project_primitives['msg']}, services - {project_primitives['srv']}, actions - {project_primitives['action']}")
        data_frame.append({
            'Project': project,
            'Topics (.msg)': project_primitives['msg'],
            'Services (.srv)': project_primitives['srv'],
            'Actions (.action)': project_primitives['action']
        })

    #visualize
    df = pd.DataFrame(data_frame)
    df.set_index('Project')[['Topics (.msg)', 'Services (.srv)', 'Actions (.action)']].plot(
        kind='bar', 
        figsize=(12, 6),
        color=['#FF69B4', '#87CEEB', '#9370DB']
    )
    plt.title('ROS2 Primitive Comparison')
    plt.ylabel('Count')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
