import os

def get_file_path(sub_folder, file_name):
    folder_path = get_folder_path(sub_folder)
    return os.path.join(folder_path, file_name)

def get_folder_path(sub_folder):
    cwd = os.getcwd()
    sub_folder_path = os.path.join('graphs', sub_folder)
    return os.path.join(cwd, sub_folder_path)