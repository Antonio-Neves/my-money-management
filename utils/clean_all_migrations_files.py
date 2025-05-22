import os

def delete_initial_files(project_path, file_name):

    for root, dirs, files in os.walk(project_path):
        if '.venv' not in root:
            for file in files:
                if file.endswith(file_name):
                    os.remove(os.path.join(root, file))
                    print(f"Arquivo {file} deletado em {root}")


project_path = '..'

delete_initial_files(project_path, '_initial.py')
