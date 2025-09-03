import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    file_info_list = []
    print(f"checking: {working_directory} & {directory}")
    
    try:
        joined_path = os.path.join(working_directory, directory)
        absolute_path = os.path.abspath(joined_path)
        if not absolute_path.startswith(os.path.abspath(working_directory)):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(absolute_path):
            return f'Error: "{directory}" is not a directory'
        for item in os.listdir(absolute_path):
            item_abspath = os.path.abspath(os.path.join(absolute_path, item))
            file_info_list.append(f'- {item}: file_size={os.path.getsize(item_abspath)} is_dir={os.path.isdir(item_abspath)}')
            
    except Exception as e:
        print(f"Error: {e}")  
         
    file_info = "\n".join(file_info_list)
    
    return file_info