import os

def get_files_info(working_directory, directory="."):
    file_info_list = []
    try:
        joined_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(joined_path)
        if not absolute_path.startswith(os.path.abspath(".")):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(directory):
            return f'Error: "{directory}" is not a directory'
        for item in os.listdir(absolute_path):
            file_info_list.append(f'- {item}: file_size={os.path.getsize(item)} is_dir={os.path.isdir(item)}')
    except Exception as e:
        print(f"Error: {e}")    
    file_info = "\n".join(file_info_list)
    return file_info